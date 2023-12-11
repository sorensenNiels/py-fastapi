import logging
import os

from dynaconf import Dynaconf

from src.utils.read_text_file import readTextFile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_FOLDER = os.path.dirname(HERE)
CONFIG_FOLDER = os.path.join(ROOT_FOLDER, "config")

logger = logging.getLogger(__name__)

settings = Dynaconf(
    envvar_prefix="PYTHON",
    # preload=[os.path.join(HERE, "default.toml")],
    preload=["config/default.toml"],
    settings_files=["config/settings.toml", "config/.secrets.toml"],
    environments=["development", "production", "testing"],
    env_switcher="PYTHON_ENV",
    load_dotenv=False,
)


def getAPIVersion():
    version = readTextFile(os.path.join(CONFIG_FOLDER, "VERSION"))
    logger.info("API version: %s", version)
    return version


def setLogBasicConfig():
    logLevel = settings.LOG_LEVEL
    logging.basicConfig(
        level=logLevel,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


"""
# How to use this application settings

```
from fastapi_example.config import settings
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
fastapi_example_ENV=production fastapi_example run
```

Read more on https://dynaconf.com
"""
