import os

from dotenv import load_dotenv

load_dotenv()


class RAGRetrieverSettings:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RAGRetrieverSettings, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, config: dict = {}) -> None:
        if self.__initialized:
            return
        self.__initialized = True

        self.embeddings_name = (
            config.get("embeddings_name")
            if config.get("embeddings_name")
            else os.getenv("RETRIEVER_EMBEDDINGS")
        )
        if not self.embeddings_name:
            raise ValueError("embeddings_name is required")

        self.database_type = (
            config.get("database_type")
            if config.get("database_type")
            else os.getenv("RETRIEVER_DATABASE_TYPE")
        )
        if not self.database_type:
            raise ValueError("database_type is required")

        similarity_threshold = (
            config.get("similarity_threshold")
            if config.get("similarity_threshold")
            else os.getenv("RETRIEVER_SIMILARITY")
        )
        if similarity_threshold:
            try:
                self.similarity_threshold = float(similarity_threshold)
            except ValueError:
                raise ValueError("similarity_threshold needs to be a float")

        self.top_k = (
            config.get("top_k") if config.get("top_k") else os.getenv("RETRIEVER_TOP_K")
        )
        if not self.top_k:
            raise ValueError("top_k is required")
        elif not self.top_k.isdigit():
            raise ValueError("top_k must be an integer number")
        self.top_k = int(self.top_k)

        self.session_id = (
            config.get("session_id")
            if config.get("session_id")
            else os.getenv("RETRIEVER_SESSION_ID")
        )
        if not self.session_id:
            raise ValueError("session_id is required")

        self.memory_url = (
            config.get("memory_url")
            if config.get("memory_url")
            else os.getenv("RETRIEVER_MEMORY_URL")
        )
        if not self.memory_url:
            raise ValueError("database_url is required")

        # database-specific settings

        self.database_path = (
            config.get("database_path")
            if config.get("database_path")
            else os.getenv("RETRIEVER_DATABASE_PATH")
        )

        self.database_name = (
            config.get("database_name")
            if config.get("database_name")
            else os.getenv("RETRIEVER_DATABASE_NAME")
        )
        self.database_table = (
            config.get("database_table")
            if config.get("database_table")
            else os.getenv("RETRIEVER_DATABASE_TABLE")
        )
        self.database_host = (
            config.get("database_host")
            if config.get("database_host")
            else os.getenv("RETRIEVER_DATABASE_HOST")
        )
        self.database_port = (
            config.get("database_port")
            if config.get("database_port")
            else os.getenv("RETRIEVER_DATABASE_PORT")
        )
        self.database_username = (
            config.get("database_username")
            if config.get("database_username")
            else os.getenv("RETRIEVER_DATABASE_USERNAME")
        )
        self.database_password = (
            config.get("database_password")
            if config.get("database_password")
            else os.getenv("RETRIEVER_DATABASE_PASSWORD")
        )
