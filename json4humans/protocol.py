"""
This modules provides the JSONModule protocol as well as some related helpers.
"""

from __future__ import annotations

import inspect
from pathlib import Path
from typing import Any, Literal, Protocol, TextIO, runtime_checkable

from lark import Lark
from lark.visitors import Transformer

from .env import DEBUG


class JSONEncoder(Protocol):
    """
    Protocol for JSON encoders
    """

    indent: int | str | None

    def __init__(self, *, indent: int | str | None = None) -> None:
        super().__init__()
        self.indent = indent

    def encode(self, obj: Any) -> str:
        """
        Serialize any object into a JSON string.

        :param obj: Any supported object to serialize
        :returns: the JSON serialized string representation
        """
        raise NotImplementedError(f"Unknown type: {type(obj)}")


@runtime_checkable
class JSONModule(Protocol):
    """
    Protocol for JSON modules implemnentation.

    Each implementation must be defined as module implementing this protocol.
    """

    transformer: Transformer
    """
    The default tranformer instance
    """

    __name__: str
    """The module fully qualified name"""

    def __str__(self) -> str:
        return self.__name__

    def loads(self, src: str) -> Any:
        """
        Loads data from a string.

        :param src: Some JSON data as string.
        """
        ...

    def load(self, file: TextIO | Path) -> Any:
        """
        Loads data from a file-like object or a Path.

        :param file: A file-like object or path to a file containing JSON to parse.
        """
        ...

    def dumps(
        self, obj: Any, *, cls: type[JSONEncoder] | None = None, indent: str | int | None = None
    ) -> str:
        """
        Serialize `obj` to a string.

        The parameters have the  same meaning as [dump()][json4humans.protocol.JSONModule.dump]

        :param obj: The object to serialize as JSON.
        :param cls: An encoder class to use. Will use the default module encoder if `None`.
        :param indent: Indentation to use, either an integer defining the number of spaces
                       or a string representing the indentation characters to be used as indentation.
        :returns: The serialized object as a JSON string representation.
        """
        ...

    def dump(
        self,
        obj: Any,
        out: TextIO | Path,
        *,
        cls: type[JSONEncoder] | None = None,
        indent: str | int | None = None,
    ):
        """
        Serialize `obj` to a file-like object.

        :param obj: The object to serialize as JSON.
        :param cls: An encoder class to use. Will use the default module encoder if `None`.
        :param indent: Indentation to use, either an integer defining the number of spaces
                       or a string representing the indentation characters to be used as indentation.
        :param out: A file-like object or path to a file to serialize to JSON into.
        """
        ...


LexerType = Literal["auto", "basic", "contextual", "dynamic", "complete_dynamic"]
"""Lark supported lexer types"""


def implement(
    grammar: str, transformer: Transformer, encoder: type[JSONEncoder], lexer: LexerType = "auto"
):
    """
    A [JSON module][json4humans.protocol.JSONModule] attributes factory.

    Only provide the grammar, the transformer, the encoder class (and a few optional parameters)
    and this factory will create all the missing helpers and boiler plate to implement
    [JSONModule][json4humans.protocol.JSONModule] in the caller module.

    :param grammar: the base name of the grammar (will use the Lark grammar of the same name)
    :param transformer: the instanciated tranformer for this grammar
    :param encoder: the default encoder class used on serialization
    :param lexer: optionaly specify a lexer implementation for Lark
    """
    _params = {
        "lexer": lexer,
        "parser": "lalr",
        "start": "value",
        "maybe_placeholders": False,
        "regex": True,
    }

    if not DEBUG:
        _params["transformer"] = transformer

    parser = Lark.open(f"grammar/{grammar}.lark", rel_to=__file__, **_params)

    def dump(obj: Any, out: TextIO | Path, *, indent: str | int | None = None):
        out = out.open("w") if isinstance(out, Path) else out
        out.write(dumps(obj))
        out.write("\n")

    def dumps(obj: Any, *, indent: str | int | None = None) -> str:
        return encoder(indent=indent).encode(obj)

    def load(file: TextIO | Path) -> str:
        data = file.read_text() if isinstance(file, Path) else file.read()
        return loads(data)

    def loads(src: str) -> Any:
        if DEBUG:
            tree = parser.parse(src)
            return transformer.transform(tree)
        else:
            return parser.parse(src)

    dump.__doc__ = JSONModule.dump.__doc__
    dumps.__doc__ = JSONModule.dumps.__doc__
    load.__doc__ = JSONModule.load.__doc__
    loads.__doc__ = JSONModule.loads.__doc__

    info = inspect.stack()[1]
    module = inspect.getmodule(info[0])

    if module is None:
        raise RuntimeError(f"Unable to process module from FrameInfo: {info}")

    setattr(module, "parser", parser)
    setattr(module, "loads", loads)
    setattr(module, "load", load)
    setattr(module, "dump", dump)
    setattr(module, "dumps", dumps)
