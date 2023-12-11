import pytest
from ..utilities.format_responses import ResponderWithScore, ResponderWithDocument
from ..utilities.retriever import document_retrieval, get_scores, chatbot_answer_with_history
from ..utilities.retriever_utils.settings import RAGRetrieverSettings
from ..utilities.retriever_utils.vectorstore_methods import get_vectorstore_connector

@pytest.fixture
def set_RAGSettings_postgres(monkeypatch):
    #retriever settings
    monkeypatch.setenv("RETRIEVER_DATABASE_TYPE", "postgres")
    monkeypatch.setenv("RETRIEVER_EMBEDDINGS", "OpenAIEmbeddings")
    monkeypatch.setenv("RETRIEVER_SIMILARITY", "0.5")
    monkeypatch.setenv("RETRIEVER_TOP_K", "4")
    monkeypatch.setenv("RETRIEVER_SESSION_ID", "test_new")
    monkeypatch.setenv("RETRIEVER_MEMORY_URL", "redis://172.21.0.1:6379")
    monkeypatch.setenv("RETRIEVER_DATABASE_HOST", "172.21.0.1")
    monkeypatch.setenv("RETRIEVER_DATABASE_PORT", "5432")
    monkeypatch.setenv("RETRIEVER_DATABASE_USERNAME", "postgres")
    monkeypatch.setenv("RETRIEVER_DATABASE_PASSWORD", "postgres")
    monkeypatch.setenv("RETRIEVER_DATABASE_TABLE", "TestVectors")
    monkeypatch.setenv("RETRIEVER_DATABASE_NAME", "vectors")
    settings = RAGRetrieverSettings()
    return settings

def test_settings_import(set_RAGSettings_postgres):
    assert set_RAGSettings_postgres.database_host == '172.21.0.1'