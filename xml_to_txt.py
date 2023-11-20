import os
import xml.etree.ElementTree as ET

def convert_xml_to_txt(xml_file, output_folder):
    # parse xml tree
    try:
        tree = ET.parse(xml_file)
    except ET.ParseError as e:
        print(f"Error parsing XML file {xml_file}: {e}")
        return

    root = tree.getroot()
    
    # get article title and abstract text
    title = root.find(".//ArticleTitle").text
    abstract = "".join([t.text for t in root.findall(".//AbstractText")])
    
    # save as text file
    pmid = root.find(".//PMID").text
    txt_file = os.path.join(output_folder, f"{pmid}.txt")
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(f"Title: {title}\n\nAbstract: {abstract}".strip())




def main():
    # prompt for folder path and output folder path
    while True:
        xml_folder = input("Enter folder path for xml files: ")
        if not os.path.isdir(xml_folder):
            print("Folder path is incorrect or doesn't exist. Please try again.")
        elif not any(file.endswith(".xml") for file in os.listdir(xml_folder)):
            print("No xml files found in folder. Please try again.")
        else:
            break
    output_folder = input("Enter folder path where you want to save your outputs: ")
    os.makedirs(output_folder, exist_ok=True)

    # convert xml files to txt files
    count = 0
    for xml_file in os.listdir(xml_folder):
        if xml_file.endswith(".xml"):
            xml_file_path = os.path.join(xml_folder, xml_file)
            convert_xml_to_txt(xml_file_path, output_folder)
            count += 1

    # print message indicating completion
    print(f"\n{'='*50} Done {'='*50}\n")
    # print message indicating number of files converted
    print(f"{count} files have been converted to .txt files in folder: {output_folder}")


if __name__ == "__main__":
    main()

