import os

DEBUG: bool = bool(os.environ.get("DEBUG", 0))
"""
If this environment is set to a truthy value,
the parsing and transform will be done in 2 steps
allowing detailled parsing errors.

See [Tree-less LALR](https://lark-parser.readthedocs.io/en/latest/json_tutorial.html#step-3-tree-less-lalr-1)
"""
