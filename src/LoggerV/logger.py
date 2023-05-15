from dataclasses import dataclass
from functools import wraps
import tracemalloc
from time import perf_counter
from typing import Any


# Decorators
def preformer(func):
    @wraps(func)
    def wrapper(*args: Any, **kwds: Any) -> Any:
        tracemalloc.start()
        start_time = perf_counter()
        func(*args, **kwds)
        current, peak = tracemalloc.get_traced_memory()
        finish_time = perf_counter()
        print(
            f"Function Name: {func.__name__}",
            f"\nDocstring: {func.__doc__}"
            f"\nCurrent memory usage: {current / 10**6:.3f} MB"
            f"\nPeak memory usage: {peak / 10**6:.3f} MB"
            f"\nTime taken: {(finish_time - start_time):.6f}\n",
        )
        tracemalloc.stop()

    return wrapper


@dataclass
class Log:
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
        self.__logs: list[Log] = []
        self.__customNames = []
        self.__customPrintValues = []
        self.__customDefaults = []
        self.__dontPrintIf = []

        self.__funcNames = {}

    def __parseCustom_oneUse(
        self, step: str, message: str, success: bool, names: list, values: list
    ):
        self.__logs.append(
            Log(
                step=step,
                message=message,
                customNames=names,
                customValues=values,
                success=success,
            )
        )

    def __parseCustom(
        self,
        custom: Any,
        customNames: list,
        customPrintValues: list,
        customDefaults: list,
        dontPrintIf: list,
    ) -> list:
        names = []
        values = []
        if custom is None:
            return [], []
        for c, name in enumerate(customNames):
            names.append(customPrintValues[c])
            value = getattr(custom, name, customDefaults[c])
            if value == dontPrintIf[c]:
                values.append(None)
            elif value is None and dontPrintIf[c] is None:
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
    ):
        customNames = []
        customPrintValues = []
        customDefaults = []
        innerDontPrintIf = []
        for c, name in enumerate(names):
            customNames.append(name)
            customPrintValues.append(
                printValues[c]
            ) if printValues is not None and printValues[c] is not None else name
            customDefaults.append(defaults[c]) if defaults is not None and defaults[
                c
            ] is not None else customDefaults.append(None)
            innerDontPrintIf.append(
                dontPrintIf[c]
            ) if dontPrintIf is not None and dontPrintIf[
                c
            ] is not None else innerDontPrintIf.append(
                None
            )
        return customNames, customPrintValues, customDefaults, innerDontPrintIf

    def loadCustom(
        self,
        names: list[str],
        printValues: list[str] = None,
        defaults: list = None,
        dontPrintIf: list = None,
    ) -> None:
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

    def append(
        self, step: str = None, message: str = None, custom: Any = None, success=None
    ):
        names, values = self.__parseCustom(
            custom,
            self.__customNames,
            self.__customPrintValues,
            self.__customDefaults,
            self.__dontPrintIf,
        )
        self.__logs.append(
            Log(
                step=step,
                message=message,
                customNames=names,
                customValues=values,
                success=success,
            )
        )
        return None

    def __str__(self) -> str:
        builder = "#" * 15 + f"   Start Logs for: {self.name}   " + "#" * 15 + "\n"
        for i in self.__logs:
            builder += "\n" + str(i)
        builder += (
            "\n" + "#" * 15 + f"   End Logs for: {self.name}   " + "#" * 17 + "\n"
        )
        return builder


def funcLogger(logger: Logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args: Any, **kwds: Any) -> Any:
            run = kwds.get("run", 1)
            name = func.__name__
            logger._Logger__funcNames[name] = logger._Logger__funcNames.get(name, 0) + 1
            try:
                func(*args, **kwds)
                if run == 2:
                    logger._Logger__parseCustom_oneUse(
                        step=f"Running function {name}",
                        message=None,
                        names=["Run Number"],
                        values=[logger._Logger__funcNames.get(name)],
                        success=None,
                    )
            except Exception as ex:
                if run > 0:
                    logger._Logger__parseCustom_oneUse(
                        step=f"Running function {func.__name__}",
                        message=f"Failed with error: {ex}",
                        names=["Run Number"],
                        values=[logger._Logger__funcNames.get(func.__name__)],
                        success=False,
                    )
                raise ex

        return wrapper

    return decorator
