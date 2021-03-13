if __name__ == '__main__':
    import inspect
    import os
    import sys

    current_dir = os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe())))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)

from src.utils import *

data_path = "data/dragontail-11.1.1/11.1.1/data/en_US/champion/"

print("Testing get_PQWER function...")
assert set(get_PQWER("Malphite", data_path).keys()) \
    == {'passive','Q', 'W', 'E', 'R'}, "All ability keys must be returned"

assert type(get_PQWER("Malphite", data_path)) == dict,\
    "Function must return a dictionary"

assert all(type(value) == str for value in get_PQWER("Malphite", data_path).values()),\
    "Confirm that all dictionary values are a string"

print("All get_PQWER tests passed!")