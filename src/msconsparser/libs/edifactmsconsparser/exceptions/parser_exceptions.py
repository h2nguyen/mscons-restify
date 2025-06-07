# coding: utf-8

class MSCONSParserException(Exception):
    def __init__(self, message: str = "Parser error", value: str = None):
        self.message = message
        self.value = value
        super().__init__(f"{message}{': ' + value if value else ''}")
