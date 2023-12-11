import logging
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, RedisChatMessageHistory
from langchain.prompts import ChatPromptTemplate
from langchain.schema.document import Document
from pydantic import BaseModel

from .utilities.format_responses import ResponderWithDocument
from .utilities.prompt_variables import template_history_prompt
from .utilities.retriever import (
    chatbot_answer_with_history,
    document_retrieval,
    get_scores,
)
from .utilities.retriever_utils.settings import RAGRetrieverSettings
from .utilities.retriever_utils.vectorstore_methods import get_vectorstore_connector

load_dotenv()
logging.getLogger().setLevel(logging.INFO)

app = FastAPI()


class Request(BaseModel):
    """
    Request class for handling requests.

    Attributes
    ----------
    question : str
        The question asked in the request.
    """

    question: str


settings = RAGRetrieverSettings()


def retrieve_docs_similar_to_question(
    question: str, settings: RAGRetrieverSettings
) -> List[Document]:
    """
    Return document chunks from vector database specified in the settings, based on similarity search with the question
    """
    vectorstore = get_vectorstore_connector(settings)
    retrieved_documents = document_retrieval(
        vectorstore,
        question,
        top_k=settings.top_k,
        similarity_threshold=settings.similarity_threshold,
    )
    return retrieved_documents


@app.post("/ask")
async def ask_question(request: Request) -> dict:
    """
    Ask a question to a chatbot and get an answer.

    Parameters
    ----------
    request : Request
        The request object.

    Returns
    -------
    dict
        A dictionary containing the answer, documents, and scores.
    """
    question = request.question
    retrieved_documents = retrieve_docs_similar_to_question(question, settings)
    logging.info(f"Retrieved documents: {retrieved_documents}")
    prompt = ChatPromptTemplate.from_template(template_history_prompt)
    model = ChatOpenAI()
    # set up message history and conversation memory
    message_history = RedisChatMessageHistory(
        url=settings.memory_url, session_id=settings.session_id
    )
    memory = ConversationBufferMemory(chat_memory=message_history)
    # get chatbot answer
    answer = chatbot_answer_with_history(
        question, retrieved_documents, memory, prompt, model
    )
    # update memory entries
    message_history.add_user_message(question)
    message_history.add_ai_message(answer)
    responder = ResponderWithDocument(
        {
            "answer": answer,
            "documents": retrieved_documents,
            "scores": get_scores(retrieved_documents),
        }
    )
    return responder.produce_response()
