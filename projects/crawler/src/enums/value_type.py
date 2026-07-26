from enum import Enum


class ValueType(str, Enum):

    SELECTOR = "selector"

    CONTEXT = "context"

    CONSTANT = "constant"

    TEMPLATE = "template"

    EXPRESSION = "expression"

    ENV="env"
    FILE="file"
    DATABASE="database"
    SECRET="secret"
    AI="ai"