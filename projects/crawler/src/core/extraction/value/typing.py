from enum import StrEnum


class ValueType(StrEnum):

    CONSTANT = "constant"

    CONTEXT = "context"

    EXPRESSION = "expression"

    SELECTOR = "selector"

    TEMPLATE = "template"

    # ENV="env"
    # FILE="file"
    # DATABASE="database"
    # SECRET="secret"
    # AI="ai"