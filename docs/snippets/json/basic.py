from json4humans import json

DATA = """
{
    "key": "value"
}
"""

# Loads data from string
data = json.loads(DATA)

# Manipulate using the native types interfaces
assert data["key"] == "value"

# Serialize with style preservation
assert json.dumps(data) == DATA
