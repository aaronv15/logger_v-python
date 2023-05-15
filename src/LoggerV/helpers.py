from dataclasses import dataclass
from traceback import extract_stack


@dataclass
class BaseLoggerError(Exception):
    code: int
    msg: str

    def extract(self) -> str:
        builder = f"Failed with error code {self.code}\n"
        builder += f"Message: {self.msg}\n"
        return builder

    def __str__(self) -> str:
        return super().__str__()
