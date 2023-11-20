import os
import json
import urllib.request
import time
import datetime
# import spacy
import xml.etree.ElementTree as ET
from tqdm import tqdm
import re

class e_utility():
    
    def __init__(self):
        self.sleep_minutes = 0.2
        self.base_url_esearch = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'
        self.base_url_efetch = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?'
        self.output_file_path = './Pubmed_abstracts/'
        # self.nlp = spacy.load(r"C:\Users\15312\OneDrive - University of Nebraska at Omaha\Ayman_desktop\vs codes\highlighted pdfsss\Graphene PDFs\CHEMDNER\model_1_0\model-best")
    
    
    
    # Search for articles using esearch    
    def search(self, search_term, num_papers):
        id_list = []
        search_term = search_term.replace(' ', '+')
        url = self.base_url_esearch + 'db=pubmed&term=' + search_term + '&retmode=json&retmax=' + str(num_papers) + '&usehistory=y'

        while True:
            date_filter = input("Do you want to filter your search by date published? (yes or no): ")
            if date_filter.lower() not in ["yes", "no"]:
                print("Invalid input. Please enter either 'yes' or 'no'.")
            else:
                break

        if date_filter.lower() == "yes":
            while True:
                year_range = input("Enter the range of years you want (e.g. 2021-2022) or enter 'no': ")
                if year_range.lower() == "no":
                    break
                elif not re.match(r"\d{4}-\d{4}", year_range):
                    print("Invalid input. Please enter a valid year range (e.g. 2021-2022) or enter 'no'.")
                else:                               
                    start_year, end_year = map(int, year_range.split("-"))
                    url += f"&mindate={start_year}&maxdate={end_year}"
                    break

            while True:
                author_name = input("Enter author name or enter 'no': ")
                if author_name.lower() == "no":
                    break
                elif not re.match(r"^[a-zA-Z\s]*$", author_name):
                    print("Invalid input. Please enter a valid author name or enter 'no'.")
                else:
                    url += f"&au={author_name}"
                    break

        with urllib.request.urlopen(url) as result:
            text = result.read().decode('utf-8')
                
        json_text = json.loads(text)
        webenv = json_text['esearchresult']['webenv']
        id_list = json_text['esearchresult']['idlist']

        # Check if any IDs have already been downloaded and remove them from the list
        try:
            with open("downloaded_ids.txt", "r") as f:
                downloaded_ids = [line.strip() for line in f.readlines()]
                id_list = list(set(id_list) - set(downloaded_ids))
        except FileNotFoundError:
            pass

        # Download the remaining IDs and save their IDs to the text file
        print("Downloading abstracts...\n")
        with tqdm(total=len(id_list)) as pbar:
            for uid in id_list:
                self.retrieve_abstract(uid, webenv)
                with open("downloaded_ids.txt", "a") as f:
                    f.write(uid + "\n")
                pbar.update(1)

        return id_list



    # use efetch to open the list of articles and write out the raw xml files
    def retrieve_abstract(self,uid,webenv):
        url = self.base_url_efetch + 'db=pubmed&retmode=xml&id=' + \
            uid + '&webenv=' + webenv 
        result = urllib.request.urlopen(url)   
        xml_text = result.read().decode('utf-8')
        file_name = self.output_file_path + uid + '.xml'
        file_out = open(file_name,'w',encoding = 'utf-8')
        file_out.write(xml_text)
        file_out.close()
        time.sleep(self.sleep_minutes * 60)
        
    
    
    
    
    #Use model 1.0 to make annotations on downloaded articles
    # def make_predictions(self, abstract_folder_path):
    #     json_output_dir = abstract_folder_path + "/JSON_results/"
    #     text_output_dir = abstract_folder_path + "/text_results/"
    #     if not os.path.exists(json_output_dir):
    #         os.makedirs(json_output_dir)
    #     if not os.path.exists(text_output_dir):
    #         os.makedirs(text_output_dir)
    #     for filename in os.listdir(abstract_folder_path):
    #         if filename.endswith(".xml"):
    #             file_path = abstract_folder_path + "/" + filename
    #             tree = ET.parse(file_path)
    #             root = tree.getroot()
    #             for abstract in root.findall(".//AbstractText"):
    #                 abstract_text = abstract.text
    #                 if abstract_text is not None:
    #                     abstract_text = re.sub(r"<.*?>", "", abstract_text)

    #                     doc = self.nlp(abstract_text)
    #                     entities = [(ent.text, ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
    #                     pmid = filename[:-4]

    #                     json_output = [(abstract_text, {"entities": entities})]
    #                     json_file_name = json_output_dir + pmid + ".json"
    #                     with open(json_file_name, "w", encoding="utf-8") as f:
    #                         json.dump(json_output, f, ensure_ascii=False)

    #                     text_output = abstract_text + "\n\n" + "Entities:\n"
    #                     for ent in entities:
    #                         text_output += f"{ent[0]} ({ent[1]}, {ent[2]}, {ent[3]})\n"
    #                     text_file_name = text_output_dir + pmid + ".txt"
    #                     with open(text_file_name, "w", encoding="utf-8") as f:
    #                         f.write(text_output)
    #                 else:
    #                     print(f"No predictions made for PMID {pmid}: no abstract found")








#Initializing the instances

e_util = e_utility()

option = input("What would you like to do?\n1. Download papers\nEnter option number: ")

if option == "1":
    search_term = input("Enter the search term: ")
    while True:
        try:
            num_papers = int(input("How many papers do you want to search? (Max 10 papers): "))
            if num_papers > 10:
                print("Please enter a number less than or equal to 10.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    start = datetime.datetime.now()
    id_list = e_util.search(search_term, num_papers)
    end = datetime.datetime.now()
    print(f"\n{len(id_list)} abstracts have been downloaded.")
    print(f"Time taken to download all the xml files: {end - start}")
# elif option == "2":
#     while True:
#         abstract_folder_path = input("Enter abstract folder path: ")
#         if os.path.exists(abstract_folder_path):
#             break
#         print("Invalid folder path. Please enter a valid folder path.")
#     start = datetime.datetime.now()
#     e_util.make_predictions(abstract_folder_path)
#     end = datetime.datetime.now()
#     print(f"\nPredictions have been saved in the folder.")
#     print(f"Time taken to make predictions: {end - start}")
else:
    print("Invalid option. Please enter a valid option number.")  



