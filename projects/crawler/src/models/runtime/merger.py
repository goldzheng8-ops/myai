from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic
from dataclasses import dataclass


from models.config.request import RequestConfig
from request.defaults import RequestMergeConfig
from models.enums.merge_policy import MergePolicy
from models.runtime.request.descriptor import RequestDescriptor


from copy import deepcopy



T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")








