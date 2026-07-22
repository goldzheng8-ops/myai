from config.config import OutputFormat
from pydantic import BaseModel

class OutputConfig(BaseModel):

    format:OutputFormat=OutputFormat.JSON

    callback_url:str|None=None

    encoding:str="utf-8"