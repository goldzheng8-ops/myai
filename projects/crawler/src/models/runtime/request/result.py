
from dataclasses import dataclass

from models.runtime.base import BaseResult
from models.runtime.response.base import ResponseAdapter


@dataclass(slots=True)
class RequestResult(BaseResult):

    response: ResponseAdapter | None = None