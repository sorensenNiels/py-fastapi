import logging

from langchain.embeddings.openai import OpenAIEmbeddings


def embedding_selector(emb_name: str):
    if emb_name == "OpenAIEmbeddings":
        embeddings = OpenAIEmbeddings
    else:
        logging.error("emb_name not in the list of available embeddings")
    return embeddings
