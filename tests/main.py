from loggerV.logger import Logger, funcLogger


class Example:
    def __init__(self, one, two) -> None:
        self.one = one
        self.two = two


logger = Logger(name="Logger")

logger.loadCustom(
    names=["fieldOne", "fieldTwo"],
    printValues=["One", "Two"],
    defaults=None,
    dontPrintIf=None,
)


@funcLogger(logger)
def convert(string, run=0, fail=None):
    return int(string)


logger.addPartition("before", 1)


logger.append(
    step="First Log",
    message="Testing",
    custom=Example(one="Hello", two="World"),
    success=True,
    partition="after",
)
logger.append("Second Log", "Testing", success=False, partition="before")
logger.append("Third Log")

print(logger)
