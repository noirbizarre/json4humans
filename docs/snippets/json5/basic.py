from json4humans import json5

DATA = """
{
    // Comment
    key: "value"
}
"""

# Loads data from string
data = json5.loads(DATA)

# Manipulate using the native types interfaces
assert data["key"] == "value"

# Serialize with style preservation
assert json5.dumps(data) == DATA
