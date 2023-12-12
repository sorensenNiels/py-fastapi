from operator import itemgetter
from typing import List, Optional

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.schema.document import Document
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.retriever import BaseRetriever
from langchain.schema.runnable import RunnableLambda
from langchain.schema.vectorstore import VectorStore


class FAISSVectorStoreRetrieverWithScore(BaseRetriever):
    """
    A class used to retrieve documents from a FAISS vector store with their similarity scores.

    Attributes
    ----------
    vectorstore : VectorStore
        An instance of VectorStore class which represents the vector store to be used for document retrieval.
    search_kwargs : dict
        A dictionary of search parameters to be used in the similarity search.

    Methods
    -------
    get_relevant_documents(query: str, threshold: Optional[float] = None) -> List[Document]
        Retrieves relevant documents from the vector store based on the given query and threshold.
    """

    vectorstore: VectorStore
    search_kwargs: dict

    def _get_relevant_documents(
        self, query: str, threshold: Optional[float] = None
    ) -> List[Document]:
        """
        Retrieves relevant documents from the vector store based on the given query and threshold.

        Parameters
        ----------
        query : str
            The query string based on which relevant documents are to be retrieved.
        threshold : float, optional
            The similarity score threshold. Only documents with a score less than this threshold are returned.
            If no threshold is provided, all documents are returned.

        Returns
        -------
        list
            A list of Document objects that are relevant to the given query.
        """
        docs_and_scores = self.vectorstore.similarity_search_with_score(
            query, k=self.search_kwargs["k"]
        )
        return_list = []
        for doc, score in docs_and_scores:
            doc.metadata = {**doc.metadata, **{"score": score}}
            if threshold is None or score < threshold:
                return_list.append(doc)
        return return_list


def get_scores(docs: List[Document]) -> List[float]:
    """
    Extracts the 'score' metadata from each document in the provided list.

    Parameters
    ----------
    docs : List[Document]
        A list of Document objects.

    Returns
    -------
    List[float]
        A list of scores extracted from the metadata of each Document object.
    """
    return [float(doc.metadata["score"]) for doc in docs]


def document_retrieval(
    vectorstore: VectorStore,
    question: str,
    top_k: int = 4,
    similarity_threshold: Optional[float] = None,
) -> List[Document]:
    """
    Retrieve relevant documents from a VectorStore based on a given question.

    Parameters
    ----------
    vectorstore : VectorStore
        An instance of VectorStore containing document vectors.

    question : str
        The query or question for which relevant documents are to be retrieved.

    top_k : int, optional
        The number of top documents to retrieve (default is 4).

    similarity_threshold : float or None, optional
        A threshold for similarity scores. If provided, only documents with similarity
        scores above this threshold will be returned (default is None).

    Returns
    -------
    List[Document]
        A list of Document objects retrieved based on the query.

    Notes
    -----
    This function retrieves relevant documents from the VectorStore using a specified retriever
    (FAISSVectorStoreRetrieverWithScore). It uses the provided question to find similar documents
    and returns them based on the specified parameters.
    """
    retriever = FAISSVectorStoreRetrieverWithScore(
        vectorstore=vectorstore, search_kwargs={"k": top_k}
    )
    retrieved_documents = retriever.get_relevant_documents(
        question, threshold=similarity_threshold
    )
    return retrieved_documents


def chatbot_answer_with_history(
    question: str,
    documents: List[Document],
    memory: ConversationBufferMemory,
    prompt: ChatPromptTemplate,
    model: ChatOpenAI,
) -> str:
    """
    Generates a chatbot answer based on a given question and a set of documents,
    while also taking into account the chat history.

    Parameters
    ----------
    question : str
        The question to which the chatbot should respond.

    documents : List[Document]
        A list of Document objects that the chatbot can use to generate its response.

    memory : ConversationBufferMemory
        An instance of ConversationBufferMemory that contains the chat history.

    prompt : ChatPromptTemplate
        An instance of ChatPromptTemplate that defines the structure of the chat prompt.

    model : ChatOpenAI
        An instance of ChatOpenAI that is used to generate the chatbot's response.

    Returns
    -------
    str
        The chatbot's response to the given question.

    Notes
    -----
    The function first formats the documents into a string, then it creates a chain of operations
    that includes the context (formatted documents), the question, the history (loaded from memory),
    the prompt, the model, and a parser for the output. The chain is then invoked with the question
    and the formatted documents as inputs. The answer from the chain is returned as the chatbot's response.
    """

    def format_docs(docs: List[Document]) -> str:
        """
        Formats a list of Document objects into a string.

        Parameters
        ----------
        docs : List[Document]
            A list of Document objects.

        Returns
        -------
        str
            A string that contains the page content of each Document object, separated by two newline characters.
        """
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {
            "context": itemgetter("documents") | RunnableLambda(format_docs),
            "question": itemgetter("question"),
            "history": RunnableLambda(memory.load_memory_variables)
            | itemgetter("history"),
        }
        | prompt
        | model
        | StrOutputParser()
    )
    answer = chain.invoke({"documents": documents, "question": question})
    return answer


if __name__ == "__main__":
    print("Module to use custom Langchain retriever functions")
