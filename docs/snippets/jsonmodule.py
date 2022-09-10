from json4humans import json, json5, jsonc
from json4humans.protocol import JSONModule

for format in json, jsonc, json5:
    assert isinstance(format, JSONModule)
