from logger import Logger, funcLogger


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
def divideByZero(num, run=1, fail=None):
    return 10 / num


@funcLogger(logger)
def otherFunc(string, run=1, fail=None):
    return int(string)


# logger.addPartition("before", 1)
# logger.addPartition("after", 4)
# logger.append(
#     "First Log", message="Testing", custom=temp(), success=True, partition="after"
# )
# logger.append("Second Log", "Testing", success=False, partition="before")
# logger.append("Third Log")
for i in range(10):
    i = i if i % 2 != 0 else "f"
    try:
        divideByZero(i)
    except Exception as ex:
        pass
    # try:
    #     otherFunc(i, fail=4)
    # except Exception as ex:
    #     pass
print(logger)
