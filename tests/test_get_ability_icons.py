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
print("Testing get_ability_icons function...")
assert set(get_ability_icons("Malphite", data_path).keys()) \
    == {'Passive', 'Q', 'W', 'E', 'R'}, "All ability keys must be returned"

assert type(get_ability_icons("Malphite", data_path)) == dict,\
    "Function must return a dictionary"

values = list(get_ability_icons("Malphite", data_path).values())
file_extensions = set(list(map(lambda x: x[-3:], values)))
assert len(file_extensions) == 1, "Function returns one type of file extension path"
assert file_extensions.pop() == 'png', "All dictionary values are png file paths"

assert all(type(value) == str for value in get_ability_icons("Malphite", data_path).values()),\
    "Confirm that all dictionary values are a string"

print("All get_ability_icons tests passed!")
