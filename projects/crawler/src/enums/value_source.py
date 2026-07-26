from enum import Enum


class ValueSource(str, Enum):

    SELECTOR = "selector"

    CONTEXT = "context"

    CONSTANT = "constant"

    TEMPLATE = "template"

    EXPRESSION = "expression"