from langchain.vectorstores.faiss import FAISS
from langchain.vectorstores.pgvector import PGVector

from ...config import settings
from ..embedding_selector import embedding_selector


def get_vectorstore_connector() -> PGVector | FAISS:
    embeddings_function = embedding_selector(settings.embeddings_name)
    if embeddings_function is None:
        raise ValueError(
            f"Embeddings name {settings.embeddings_name} is not valid. Please check the config file."
        )

    vectorstore = None

    if settings.database_type == "postgres":
        connection_string = PGVector.connection_string_from_db_params(
            driver="psycopg2",
            host=settings.database_host,
            port=settings.database_port,
            database=settings.database_name,
            user=settings.database_username,
            password=settings.database_password,
        )
        vectorstore = PGVector(
            embedding_function=embeddings_function(),
            collection_name=settings.database_table,
            connection_string=connection_string,
        )
    elif settings.database_type == "FAISS":
        vectorstore = FAISS.load_local(
            embeddings=embeddings_function(), folder_path=settings.database_path
        )

    if vectorstore is None:
        raise ValueError(
            f"Database type {settings.database_type} is not valid. Please check the config file."
        )

    return vectorstore
