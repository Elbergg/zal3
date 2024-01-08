import json
import argparse
import sys
import csv

"""
simple json analyzer - analizuje jsony
--rows - analizuje ile "elementow" ma json
--unique - zczytuje wszystkie unikatowe pola dla elementow
--count - liczy ilosc pol dla kazdego elementu
--out zapisuje  do csv dane dla kazdego pliku
"""


def rows(path):
    count = 0
    with open(path, "r") as file_handler:
        data = json.load(file_handler)
        for row in data:
            count += 1
    return count


def unique(path):
    unique_list = []
    with open(path, "r") as file_handler:
        data = json.load(file_handler)
        for row in data:
            tiles = row.keys()
            for tile in tiles:
                if tile not in unique_list:
                    unique_list.append(tile)
    final = " ".join(unique_list)
    return final


def save_to_csv(files, new_file, brows=None, bunique=None, bcount=None):
    with open(new_file, "w") as file_handler:
        fieldnames = ["file", "rows", "unique", "count"]
        writer = csv.DictWriter(file_handler, fieldnames)
        writer.writeheader()
        for file in files:
            data = {}
            data.update({"file": file})
            if brows:
                data.update({"rows": rows(file)})
            if bunique:
                data.update({"unique": unique(file)})
            if bcount:
                data.update({"count": count(file)})
            writer.writerow(data)


def count(path):
    count = 0
    with open(path, "r") as file_handler:
        data = json.load(file_handler)
        for row in data:
            count += len(row.keys())
    return count


def main(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    parser.add_argument("--rows", action="store_true")
    parser.add_argument("--unique", action="store_true")
    parser.add_argument("--count", action="store_true")
    parser.add_argument("--out")
    args = parser.parse_args(arguments[1:])
    files = args.files
    for file in files:
        if args.rows:
            print(rows(file))
        if args.unique:
            print(unique(file))
        if args.count:
            print(count(file))
    if args.out:
        save_to_csv(files, args.out, args.rows, args.unique, args.count)


if __name__ == "__main__":
    main(sys.argv)
