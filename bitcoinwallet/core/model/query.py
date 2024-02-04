from enum import Enum


class Operator(Enum):
    EQUALS = "="
    NOT_EQUALS = "!="
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL = ">="
    LIKE = "LIKE"
    IN = "IN"


class Logical(Enum):
    NOT = "NOT"
    AND = "AND"
    OR = "OR"
    OPEN = "("
    CLOSE = ")"
