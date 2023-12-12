import logging

from langchain.embeddings.openai import OpenAIEmbeddings


def embedding_selector(emb_name: str):
    embeddings = None  # Initialize the embeddings variable with a default value
    if emb_name == "OpenAIEmbeddings":
        embeddings = OpenAIEmbeddings
    else:
        logging.error("emb_name not in the list of available embeddings")
    return embeddings
