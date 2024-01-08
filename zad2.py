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


def save_to_json(
    paths,
    new_file,
    columnsbool=None,
    uniquebool=None,
    rowsbool=None,
    countbool=None,
):
    data = []
    for path in paths:
        file_data = {}
        if columnsbool:
            file_data.update({"columns": columns(path)})
        if rowsbool:
            file_data.update({"rows": rows(path)})
        if uniquebool:
            file_data.update({"unique": unique(path)})
        if countbool:
            file_data.update({"count-per-column": count(path)})
        data.append(file_data)
    with open(new_file, "w") as file_handler:
        json.dump(data, file_handler, indent=4)


def main(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="+")
    parser.add_argument("--columns", action="store_true")
    parser.add_argument("--rows", action="store_true")
    parser.add_argument("--unique", action="store_true")
    parser.add_argument("--count", action="store_true")
    parser.add_argument("--out")
    args = parser.parse_args(arguments[1:])
    for path in args.path:
        if args.columns:
            print(len(columns(path)))
        if args.rows:
            print(rows(path))
        if args.unique:
            print(unique(path))
        if args.count:
            print(count(path))
    if args.out:
        save_to_json(
            args.path,
            args.out,
            args.columns,
            args.unique,
            args.rows,
            args.count,
        )


if __name__ == "__main__":
    main(sys.argv)
