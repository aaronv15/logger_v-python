from dataclasses import dataclass
from functools import wraps
from typing import Any


@dataclass
class _Log:
    step: str
    message: str
    customValues: list
    customNames: list
    success: bool

    def __str__(self) -> str:
        gap = " " * 18
        builder = f"{gap}Step: {str(self.step)}\n" if self.step is not None else ""
        builder += (
            f"{gap}Message: {str(self.message)}\n" if self.message is not None else ""
        )
        for c, i in enumerate(self.customNames):
            builder += (
                f"{gap}{str(i)}: {str(self.customValues[c])}\n"
                if self.customValues[c] is not None
                else ""
            )
        builder += f"{gap}Success: {self.success}\n" if self.success is not None else ""
        return builder


# Classes
class Logger:
    def __init__(self, name: str = "Logger") -> None:
        self.name = name
        self.__logsDict: dict = {3: [], 10: []}
        self.__partitionNames: list = ["main", "footer"]
        self.__partitionValues: list = [3, 10]
        self.__customNames = []
        self.__customPrintValues = []
        self.__customDefaults = []
        self.__dontPrintIf = []

        self.__funcNames = {}

    def __validatePartitions(self, name: str = None, value: int = None) -> None:
        """Checks if the provided name and or value match"""
        if name not in self.__partitionNames and name is not None:
            raise ValueError(
                f"Partition '{name}' does not exist. Use 'addPartition()' to create a new partition"
            )
        if value not in self.__partitionValues and value is not None:
            raise ValueError(
                f"Precedence value '{value}' does not exist. Use 'addPartition()' to create a new partition"
            )
        if name is None and value is None:
            raise ValueError(
                "Either a partition name or a partition value must be given"
            )
        return None

    def __parseCustom_oneUse(
        self,
        step: str,
        message: str,
        success: bool,
        names: list,
        values: list,
        partition: int or str,
    ) -> None:
        """Parses a set of names and values that are not added to the logger"""
        if isinstance(partition, str):
            self.__validatePartitions(name=partition)
            partition = self.__getPartition(partition)
        else:
            self.__validatePartitions(value=partition)
        self.__logsDict[partition].append(
            _Log(
                step=step,
                message=message,
                customNames=names,
                customValues=values,
                success=success,
            )
        )
        return None

    def __parseCustom(
        self,
        custom: Any,
        customNames: list,
        customPrintValues: list,
        customDefaults: list,
        dontPrintIf: list,
    ) -> tuple[list]:
        """Parses the custom dataclass provided in append"""
        names = []
        values = []
        if custom is None:
            return [], []
        for c, name in enumerate(customNames):
            names.append(customPrintValues[c])
            value = getattr(custom, name, customDefaults[c])
            if value == dontPrintIf[c]:
                values.append(None)
            elif value is None and dontPrintIf[c] is not None:
                values.append("None")
            else:
                values.append(value)

        return names, values

    def __understandCustomLogger(
        self,
        names: list[str],
        printValues: list[str] = None,
        defaults: list = None,
        dontPrintIf: list = None,
    ) -> tuple[list]:
        """Parses the custom values provided in 'loadCustom()' and adds their values to the logger"""
        customNames = []
        customPrintValues = []
        customDefaults = []
        innerDontPrintIf = []
        for c, name in enumerate(names):
            customNames.append(name)
            if printValues is not None and printValues[c] is not None:
                customPrintValues.append(printValues[c])
            else:
                customPrintValues.append(name)
            if defaults is not None and defaults[c] is not None:
                customDefaults.append(defaults[c])
            else:
                customDefaults.append(None)
            if dontPrintIf is not None and dontPrintIf[c] is not None:
                innerDontPrintIf.append(dontPrintIf[c])
            else:
                innerDontPrintIf.append(None)
        return customNames, customPrintValues, customDefaults, innerDontPrintIf

    def loadCustom(
        self,
        names: list[str],
        printValues: list[str] = None,
        defaults: list = None,
        dontPrintIf: list = None,
    ) -> None:
        """Allows one to use a custom class of log fields. 'names' corresponds to the names of the class fields. 'printValues' corresponds to the structure of the log.
        'defualts' corresponds to what values to use if the fields of the class are None (By default this is None). 'dontPrintIf' tells the logger not to show a row of the log if a value is x
        (By default this is None). Once 'loadCustom()' has been called, a custom class or dataclass can be passed in as the 'custom' argument in 'append()'
        """
        (
            self.__customNames,
            self.__customPrintValues,
            self.__customDefaults,
            self.__dontPrintIf,
        ) = self.__understandCustomLogger(
            names=names,
            printValues=printValues,
            defaults=defaults,
            dontPrintIf=dontPrintIf,
        )
        return None

    def addPartition(self, name: str, precedence: int) -> None:
        """Creates a new partition with name 'name' and precedence 'precedence'. Throws a ValueError if the partition or precedence value already exists"""
        if name in self.__partitionNames:
            raise ValueError(f"Partition '{name}' already exists.")
        if precedence in self.__partitionValues:
            raise ValueError(f"Two partitions cannot have the same precedence.")
        self.__partitionNames.append(name)
        self.__partitionValues.append(precedence)
        self.__logsDict[precedence] = []
        return None

    def getPartitions(self, log=False) -> dict:
        """Returns a list of all partitions and their precedence values. Prints to the console as well if 'log' argument is set to True"""
        out = {}
        for c, i in enumerate(self.__partitionNames):
            out[i] = self.__partitionValues[c]
            print(i, ":", self.__partitionValues[c]) if log else None
        return out

    def __getPartition(self, value: str or int) -> str or int:
        """Pass in either a partition name or a precedence value and it will return the matching value. Throws a ValueError if value is not found"""
        if isinstance(value, int):
            self.__validatePartitions(name=None, value=value)
            return self.__partitionNames[self.__partitionValues.index(value)]
        if isinstance(value, str):
            self.__validatePartitions(name=value, value=None)
            return self.__partitionValues[self.__partitionNames.index(value)]

    def getPartition(self, value: str or int) -> str or int or None:
        """Pass in either a partition name or a precedence value and it will return the matching value. Returns None if value is not found"""
        try:
            if isinstance(value, int):
                return self.__partitionNames[self.__partitionValues.index(value)]
            if isinstance(value, str):
                self.__validatePartitions(name=value, value=None)
                return self.__partitionValues[self.__partitionNames.index(value)]
        except ValueError:
            return None

    def append(
        self,
        step: str = None,
        message: str = None,
        custom: Any = None,
        success: bool = None,
        partition: str or int = "main",
    ) -> None:
        """Creates a new log with defualt precedence being 'main' (3). To pass in a custom class, use 'loadCustom()' to allow the logger to use your custom class.
        To choose a different partition other than 'main', create a new partition with 'addPartition()' and specify the partition with the 'partition argument'
        """
        names, values = self.__parseCustom(
            custom,
            self.__customNames,
            self.__customPrintValues,
            self.__customDefaults,
            self.__dontPrintIf,
        )
        log = _Log(
            step=step,
            message=message,
            customNames=names,
            customValues=values,
            success=success,
        )
        self.__validatePartitions(partition)
        if isinstance(partition, str):
            partition = self.__getPartition(partition)
        self.__logsDict[partition].append(log)
        return None

    def __str__(self) -> str:
        """Returns the logs as a string"""
        builder = "#" * 15 + f"   Start Logs for: {self.name}   " + "#" * 15 + "\n"
        self.__partitionValues.sort()
        for i in self.__partitionValues:
            for i in self.__logsDict.get(i, []):
                builder += "\n" + str(i)
        builder += (
            "\n" + "#" * 15 + f"   End Logs for: {self.name}   " + "#" * 17 + "\n"
        )
        return builder

    def __sizeof__(self) -> int:
        return len(self.__logsDict)


def funcLogger(logger: Logger):
    """A decorator that can be used to log the results of a function. when calling the function three different arguments can be passed.
    'run', 'fail', and 'success'. run has threee different values. 0: log nothing. 1: log in the event of failure. 2: log for failure and success.
    The fail and success provide the ability to set which partition the log should go into. By default this is 'main' (3)
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args: Any, **kwds: Any) -> Any:
            run = kwds.get("run", 1)

            fail = kwds.get("fail", 3)
            success = kwds.get("success", 3)

            name = func.__name__
            innerId = id(func)
            logger._Logger__funcNames[innerId] = (
                logger._Logger__funcNames.get(innerId, 0) + 1
            )
            try:
                func(*args, **kwds)
                if run == 2:
                    logger._Logger__parseCustom_oneUse(
                        step=f"Running function {name}",
                        message=None,
                        names=["Run Number"],
                        values=[logger._Logger__funcNames.get(innerId)],
                        success=None,
                        partition=success,
                    )
            except Exception as ex:
                if run > 0:
                    logger._Logger__parseCustom_oneUse(
                        step=f"Running function {func.__name__}",
                        message=f"Failed with error: {ex}",
                        names=["Run Number"],
                        values=[logger._Logger__funcNames.get(innerId)],
                        success=False,
                        partition=fail,
                    )
                raise ex

        return wrapper

    return decorator
