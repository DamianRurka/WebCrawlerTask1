import csv
import os
import sys


class FileCSVHandler:
    _type = "csv"

    def open(self, src):
        with open(src, "r") as file:
            reader = csv.reader(file)
            retval = [line for line in reader]
        return retval

    def save(self, dst, obj):
        with open(dst, "w") as file:
            writer = csv.writer(file)
            for row in obj:
                writer.writerow(row)

class DataManipulator:
    def __init__(self, zmiany, data):
        self.zmiany = [z.split(",") for z in zmiany]
        self.data = data

    def make_changes(self):
        for idx in self.zmiany:
            self.data[int(idx[0])][int(idx[1])] = idx[2]


def makedirectory(dst):
    if not os.path.isdir(os.path.split(dst)[0]) and os.path.split(dst)[0]:
        os.makedirs(os.path.split(dst)[0])


src = "./data_of_links.csv"
dst = "./links.csv"
changes = sys.argv[1:]
loader = FileCSVHandler()
writer = FileCSVHandler()
makedirectory(dst)
saved_file = loader.open(src)
bf = DataManipulator(changes, saved_file)
bf.make_changes()
print(bf.data)
writer.save(dst, bf.data)


# python reader.py "3,2, 112" "3,3, 333"
