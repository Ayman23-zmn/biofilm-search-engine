import pandas as pd
import numpy as np
import streamlit as st
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity
# import plotly.express as px
# import random
# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from collections import Counter


# Title name
st.title('Biofilm Semantic Search engine app')

st.header("**How to obtain an API key**")

# Points
st.write("**1.**  Go to [OpenAI](https://platform.openai.com/) and sign up using your gmail/academic email.") 
st.markdown("**2.**  After signing up, go to your profile on the top right corner and choose **'View API keys'**. ")
st.markdown("**3.**  Create a new api key by clicking on '**Create new secret key**' button. Secret key is unique and sharing with multiple users is not recommended.")
st.markdown("**4.**  To use the search engine, paste your **API key** first and then start searching. ")
st.markdown("**5.**  You will get **$5** credit from openAI account as a new user. Once it finishes you can keep on using the api key by setting up a payment method.")


# Load the embeddings
@st.cache_data
def load_data():
    data = pd.read_csv(r'embeddings_165.csv')
    return data

df = load_data()
    



st.title("Search papers")

# Creating placeholder for the API key
user_secret = st.text_input(label = ':blue[API key]',
                            placeholder= 'Paste your API key here',
                            type = 'password')

# store it in a variable
if user_secret:
    openai.api_key = user_secret

# # Load the data
# @st.cache_data
# def load_data():
#     data = pd.read_csv(r'embeddings_165.csv')
#     return data

# df = load_data()
# st.dataframe(df) #view the dataframe in app

def search_notebook(df, search_term, n=10, pprint=True):
    """
    Search for the most relevant abstracts from the 'df' embeddings based on 'search term'  

    Args:
        df (pandas dataframe): Dataframe containing the biofilm abstract embeddings
        search_term (str): The user search term
        n (int, optional): Number of results to return. Defaults to 3.
        pprint (bool, optional): Whether to print results. Defaults to True.
        
    Returns:
        pandas dataframe: dataframe containing most relevant abstracts based on 'search term', computed by cosine similarity 
    """
    
    # Convert 'embeddings' to numpy array
    df['embedding'] = df['embedding'].apply(eval).apply(np.array)
    
    # Get embedding for the 'search term' uisng 'text-embedding-ada-002'engine.
    search_embeddings = get_embedding(search_term, engine = 'text-embedding-ada-002')
    
    # Calculate cosine similarity between abstract embeddings and 'search term' embeddings
    df["similarity"] = df['embedding'].apply(lambda x: cosine_similarity(x,search_embeddings))
    
    # Sort the retreived abtracts in descending order. (Highest cosine score being displayed at the top)
    results = (
        df.sort_values("similarity", ascending = False).head(n)
    )
    
    # if pprint: 
    #     print(results)
    
    return results


# Creating a search bar that includes search box, search caption and a placeholder text

search_term = st.text_input(
    label = ":blue[Enter your search term]",
    placeholder= "Example: Biofilm growth mechanisms..." 
)

# if search_term:
#     if st.button(label="Run",type = 'primary'):
#         answer = search_notebook(df, search_term, 3, True)
#         for index,row in answer.iterrows():
#             st.write(row['similarity'], row['Abstract'])

# results to display
if search_term:
    if st.button(label="Run", type='primary'):
        answer = search_notebook(df, search_term, 5, True)
        for index, row in answer.iterrows():
            st.write("**Relevancy score:**", row['similarity'])
            st.write("**PMID:**", row['PMID'])
            st.write("**Title:**", row['Title'])
            st.write("**Abstract:**", row['Abstract'])



