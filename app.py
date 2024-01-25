#!/usr/bin/env python3
import os
# import openai
from github import Github
# import openai
from github import Auth
from transformers import BertTokenizer
from sentence_transformers import SentenceTransformer
import nltk
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from pymongo import MongoClient

# initialize MongoDB python client


def build_mongo_client():
    host, user, pswd = os.environ['ATLAS_HOST'], os.environ['MONGODB_USERNAME'], os.environ['MONGODB_PASSWORD']
    url = f"mongodb+srv://{user}:{pswd}@{host}/?retryWrites=true&w=majority"
    return MongoClient(url)


client = build_mongo_client()

DB_NAME = "default"
COLLECTION_NAME = "test"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "default_index"
MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]


# initialize the Github API client
auth = Auth.Token(os.getenv("GITHUB_PAT"))
g = Github(auth=auth)

# initialize the Embeddings Model
model = SentenceTransformer('intfloat/e5-large-v2')
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
try:
    nltk.download("punkt")
    print("Punkt dataset downloaded")
except Exception as e:
    print(f"Error downloading NLTK punkt: {e}")
    sys.exit(1)


# Retrieve the README.md file from all repos for a given user
def get_file_from_repos(username, filename):
    user = g.get_user(username)
    file_contents = {}
    for repo in user.get_repos():
        try:
            file_content = repo.get_contents(filename)
            file_contents[
                f"{username}/{repo.name}"
            ] = file_content.decoded_content.decode()
        except Exception as e:
            print(f"Unable to retrieve {filename} for {repo.name}")
    return file_contents


# Split a provided file into sections based on the headers provided
def split_md_file(contents):
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on
    )
    md_header_splits = markdown_splitter.split_text(contents)
    return md_header_splits


# Generate a vector for a given query
def vector_embedding(query):
    try:
        instruction = "query:"
        query_string = f"{instruction} {query}"
        query_vector = model.encode([query_string])[0].tolist()
        return query_vector
    except Exception as e:
        print(f"An error occurred while querying the database: {e}")
        return str(e)


try:
    contents = get_file_from_repos("traingrc", "README.md")
    first_key = list(contents.keys())[0]
    first_content = contents[first_key]
    splits = split_md_file(first_content)
    for doc in splits:
        page_content = doc.page_content
        metadata = doc.metadata
        embedding_vector = vector_embedding(page_content)
        pymongo_doc = {
            "text": page_content,
            "metadata": metadata,
            "default_index": embedding_vector,
        }
        MONGODB_COLLECTION.insert_one(pymongo_doc)

except Exception as e:
    print(f"Error: {e}")

g.close()
