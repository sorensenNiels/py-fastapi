from langserve import RemoteRunnable

"""
Minimal example for connecting to a chain
"""


def connect_chain(chain_URL):
    """
    function returning an interface to a remote chain, returning a Langchain Runnable object
    """
    remote_chain = RemoteRunnable(chain_URL)
    return remote_chain


if __name__ == "__main__":
    chain = connect_chain("http://localhost:8000/category_chain/")
    text = remote_chain.invoke({"text": "Nations"})
    print(text)
