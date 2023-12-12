import logging
import os

from dotenv import load_dotenv

load_dotenv()
logging.getLogger().setLevel(logging.INFO)


class IndexerSettings:
    _instance = None

    def __new__(cls, *args, **kwarg):
        if cls._instance is None:
            cls._instance = super(IndexerSettings, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, config: dict = {}) -> None:
        if self.__initialized:
            return
        self.__initialized = True

        self.embeddings_name = (
            config.get("embeddings_name")
            if config.get("embeddings_name")
            else os.getenv("INDEXER_EMBEDDINGS")
        )
        if not self.embeddings_name:
            raise ValueError("embeddings_name is required")

        self.database_type = (
            config.get("database_type")
            if config.get("database_type")
            else os.getenv("INDEXER_DB_TYPE")
        )
        if not self.database_type:
            raise ValueError("database_type is required")

        self.chunk_size = (
            config.get("chunk_size")
            if config.get("chunk_size")
            else os.getenv("INDEXER_CHUNK_SIZE")
        )
        if not self.chunk_size:
            raise ValueError("chunk_size is required")
        elif not self.chunk_size.isdigit():
            raise ValueError("chunk_size must be an integer number")
        self.chunk_size = int(self.chunk_size)

        self.overlap = (
            config.get("overlap")
            if config.get("overlap")
            else os.getenv("INDEXER_OVERLAP")
        )
        if not self.overlap:
            raise ValueError("overlap is required")
        elif not self.overlap.isdigit():
            raise ValueError("overlap must be an integer number")
        self.overlap = int(self.overlap)

        self.document_path = (
            config.get("document_path")
            if config.get("document_path")
            else os.getenv("INDEXER_DOCUMENT_PATH")
        )
        if not self.document_path:
            raise ValueError("document_path is required")
        elif not os.path.isfile(self.document_path):
            raise ValueError("document_path must point to an existing file")

        # database-specific settings

        self.database_path = (
            config.get("database_path")
            if config.get("database_path")
            else os.getenv("INDEXER_DATABASE_PATH")
        )
        if not os.path.isfile(self.document_path):
            raise ValueError("database_path must point to an existing file")

        self.database_host = (
            config.get("database_host")
            if config.get("database_host")
            else os.getenv("INDEXER_DATABASE_HOST")
        )
        self.database_port = (
            config.get("database_port")
            if config.get("database_port")
            else os.getenv("INDEXER_DATABASE_PORT")
        )
        self.database_username = (
            config.get("database_username")
            if config.get("database_username")
            else os.getenv("INDEXER_DATABASE_USERNAME")
        )
        self.database_password = (
            config.get("database_password")
            if config.get("database_password")
            else os.getenv("INDEXER_DATABASE_PASSWORD")
        )
        self.database_name = (
            config.get("database_name")
            if config.get("database_name")
            else os.getenv("INDEXER_DATABASE_NAME")
        )
        self.database_table = (
            config.get("database_table")
            if config.get("database_table")
            else os.getenv("INDEXER_DATABASE_TABLE")
        )

        indexer_override = (
            config.get("indexer_override")
            if config.get("indexer_override")
            else os.getenv("INDEXER_OVERRIDE")
        )
        if not indexer_override in ("True", "False"):
            self.indexer_override = False
            logging.warning(
                "INDEXER_OVERRIDE environment variable was left undefined or not correctly set, defaults to False"
            )
        else:
            if indexer_override == "True":
                self.indexer_override = True
            else:
                self.indexer_override = False
