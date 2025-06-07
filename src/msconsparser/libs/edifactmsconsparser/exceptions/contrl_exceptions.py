# coding: utf-8

class CONTRLException(Exception):
    def __init__(self, message: str = "CONTRL – Syntax-Check - Message contains syntax error", value: str = None):
        self.message = message
        self.value = value
        super().__init__(f"{message}{': '+value if value else ''}")
