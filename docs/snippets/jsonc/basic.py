from json4humans import jsonc

DATA = """
{
    // Comment
    "key": "value"
}
"""

# Loads data from string
data = jsonc.loads(DATA)

# Manipulate using the native types interfaces
assert data["key"] == "value"

# Serialize with style preservation
assert jsonc.dumps(data) == DATA
