from pydantic import BaseModel


class AskDto(BaseModel):
    """
    Request class for handling requests.

    Attributes
    ----------
    question : str
        The question asked in the request.
    """

    question: str
