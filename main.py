# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from packages.Implementation.synonymizer import synonymizer
from packages.Implementation.data_source import DataSource


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    p1 = synonymizer()
    p1.set_synonym_data_source(DataSource())
    s = p1.get_synonyms("Wood")

    print(s)

    """print_hi('s')"""

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
