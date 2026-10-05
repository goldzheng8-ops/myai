from dataclasses import dataclass


@dataclass(slots=True)
class DotPathOptions:

    separator: str = "."

    ignore_missing: bool = False

    cache_enabled: bool = True

'''
case_sensitive

strict

escape_char
'''