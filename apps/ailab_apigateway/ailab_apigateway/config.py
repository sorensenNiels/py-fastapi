import logging
import os

from dynaconf import Dynaconf, Validator

from .utilities.read_text_file import readTextFile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_FOLDER = os.path.dirname(HERE)

description = """
The AI Lab API Gateway helps you do awesome stuff. 🚀
"""

settings = Dynaconf(
    envvar_prefix="PYTHON",
    root_path=ROOT_FOLDER,
    preload=["config/default.toml"],
    settings_files=[
        "config/settings.toml",
        "config/.secrets.toml",
    ],
    environments=["development", "production", "testing"],
    env_switcher="PYTHON_ENV",
    load_dotenv=False,
    validators=[
        Validator("DATABASE_TYPE", must_exist=True, is_in=["postgres", "FAISS"]),
        Validator("EMBEDDINGS_NAME", must_exist=True, is_in=["OpenAIEmbeddings"]),
        Validator("TOP_K", must_exist=True, is_type_of=int),
        Validator("SIMILARITY_THRESHOLD", is_type_of=float, default=0.5),
    ],
)


def setLogBasicConfig():
    logLevel = settings.LOG_LEVEL
    logging.basicConfig(
        level=logLevel,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def getAPIVersion():
    version = readTextFile(os.path.join(ROOT_FOLDER, "config", "VERSION"))
    logging.info("API version: %s", version)
    return version


"""
# How to use this application settings

```
from ailab_apigateway.config import settings
```

## Acessing variables

```
settings.get("SECRET_KEY", default="sdnfjbnfsdf")
settings["SECRET_KEY"]
settings.SECRET_KEY
settings.db.uri
settings["db"]["uri"]
settings["db.uri"]
settings.DB__uri
```

## Modifying variables

### On files

settings.toml
```
[development]
KEY=value
```

### As environment variables
```
export fastapi_example_KEY=value
export fastapi_example_KEY="@int 42"
export fastapi_example_KEY="@jinja {{ this.db.uri }}"
export fastapi_example_DB__uri="@jinja {{ this.db.uri | replace('db', 'data') }}"
```

### Switching environments
```
fastapi_example_ENV=production ailab_apigateway run
```

Read more on https://dynaconf.com
"""
