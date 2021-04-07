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
    print_hi('s')
    s = p1.get_synonyms('wood')
    s2 = p1.get_synonyms('wood')

    print_hi(len(s))
    print_hi(len(s2))
    ss = p1.get_synonyms('woods')
    ss2 = p1.get_synonyms('woods')
    print_hi(len(ss))
    print_hi(len(ss2))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
