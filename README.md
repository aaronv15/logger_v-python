# loggerV
A logger class, and a decorator that works with that class for python
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install loggerV.

```bash
pip install loggerV
```

## Basic Usage

```python
from loggerV.logger import Logger


# Creates an instance of class Logger
logger = Logger("Logger")

logger.append(
    step="First Log",
    message="Testing",
    success=True,
)
```

## Advanced Usage

```python
from loggerV.logger import Logger
from loggerV.logger import funcLogger


# Create a custom dataclass to use in the logger
class Example:
    def __init__(self, one, two) -> None:
        self.one = one
        self.two = two


# Create a new instance of the Logger class
logger = Logger(name="Logger")


# A method decorated with the funcLogger method. It accepts the logger as an argument.
# fail is what precedence the logger should use if the decorated functions fails. (Optional)
# success is what precedence the logger should use if the decorated function succeeds. (Optional)
# run is what level of logging to use. 0: no loging, even if it fails. 1: log if the function fails. 2: log whether it failsor succeeds
@funcLogger(logger)
def convert(string, run=0, fail=None, success=None):
    return int(string)


# Load the custom class so that it can be used in the logger
logger.loadCustom(
    names=["fieldOne", "fieldTwo"],
    printValues=["One", "Two"],
    defaults=None,
    dontPrintIf=None,
)

# The way partitions work is that each partition has a precedence. There are two partitions by default. main with a precedence of 3 and footer with a precedence of ten.
# Partitions and precedence can be created through the below method, and can be used in the append function. by default append uses partition main (3). 
# Logs in the same partition are ordered by first come first serve
logger.addPartition(name="first", precedence=1)


# Create a new Log
logger.append(
    step="First Log",
    message="Testing",
    custom=Example(
        one="Hello", two="World"
        ),
    success=True,
    partition="main",
)
logger.append("Second Log", "Testing", success=False, partition=1)
logger.append("Third Log")

print(logger)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
