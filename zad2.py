import argparse
import sys
import csv
import json


def columns(path):
    with open(path, "r") as file_handler:
        reader = csv.DictReader(file_handler)
        columns = reader.fieldnames
        return columns


def rows(path):
    count = -2
    with open(path, "r") as file_handler:
        reader = csv.reader(file_handler)
        for row in reader:
            count += 1
    return count


def unique(path):
    with open(path, "r") as file_handler:
        reader = csv.DictReader(file_handler)
        liist = list(reader)
        header = columns(path)
        dict = {}
        for head in header:
            unique_list = []
            for row in liist:
                unique_list.append(row[head])
            unique = set(unique_list)
            dict.update({head: len(unique)})
        return dict


def count(path):
    with open(path, "r") as file_handler:
        reader = csv.DictReader(file_handler)
        liist = list(reader)
        header = columns(path)
        dict = {}
        for head in header:
            column = {}
            for row in liist:
                if row[head] in column:
                    counter = column.get(row[head])
                    counter += 1
                else:
                    column.update({row[head]: 1})
            dict.update({head: column})
        return dict


def save_to_json(path, new_file):
    with open(new_file, "a") as file_handler:
        file_handler.write("\n")
        file_data = {path: {"columns": columns(path), "rows": rows(path)}}
        json.dump(file_data, file_handler, indent=4)


def main(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--columns", action="store_true")
    parser.add_argument("--rows", action="store_true")
    parser.add_argument("--unique", action="store_true")
    parser.add_argument("--count", action="store_true")
    parser.add_argument("--out")
    args = parser.parse_args(arguments[1:])
    if args.columns:
        print(len(columns(args.path)))
    if args.rows:
        print(rows(args.path))
    if args.unique:
        print(unique(args.path))
    if args.count:
        print(count(args.path))
    if args.out:
        save_to_json(args.path, args.out)


if __name__ == "__main__":
    main(sys.argv)
