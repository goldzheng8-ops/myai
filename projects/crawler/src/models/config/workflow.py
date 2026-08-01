

from pydantic import BaseModel, Field


class WorkflowConfig(BaseModel):

    task_name:str=""

    description:str=""

    tags:list[str]=Field(default_factory=list)

    cron:str|None=None

    callback_url:str|None=None
