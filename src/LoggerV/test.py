from logger import *
from loggerExceptions import *


@preformer
def run():
    # a = [i for i in range(1000000)]
    for i in range(1000000):
        pass


@funcLogger("Hello")
def a():
    print("In a")


class temp:
    def __init__(self) -> None:
        self.fieldOne = "Hello"
        self.fieldTwo = "World"


logger = Logger()
logger.loadCustom(
    names=["fieldOne", "fieldTwo"],
    printValues=["One", "Two"],
    defaults=["Oh", "Yeah"],
    dontPrintIf=None,
)


@funcLogger(logger)
def divideByZero(num, run):
    return 10 / num


@funcLogger(logger)
def otherFunc(string, run):
    return int(string)


logger.append("Starting", message="Testing", custom=temp(), success=True)
logger.append("Test", "Testing", success=False)
logger.append("Nothing")
for i in range(10):
    i = i if i % 2 != 0 else "f"
    try:
        divideByZero(i)
    except Exception as ex:
        pass
    try:
        otherFunc(i)
    except Exception as ex:
        pass
print(logger)
