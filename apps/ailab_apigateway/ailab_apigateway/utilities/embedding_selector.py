import logging
from enum import Enum

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_core.embeddings import Embeddings

EmbeddingTypes = Enum("EmbeddingTypes", ["OpenAIEmbeddings"])


def embedding_selector(emb_name: EmbeddingTypes) -> type[Embeddings] | None:
    embeddings = None  # Initialize the embeddings variable with a default value
    if emb_name == EmbeddingTypes.OpenAIEmbeddings.name:
        embeddings = OpenAIEmbeddings
    else:
        logging.error("emb_name not in the list of available embeddings")
    return embeddings
