import argparse
import csv
import sys
from pathlib import Path


def search_file(path, name, titlelist, duplicates_list):
    with open(path, "r") as file_handler:
        reader2 = csv.reader(file_handler)
        for row2 in reader2:
            if row2[0] == name:
                description_list = row2[4:]
                description = "".join(description_list)
    with open(path, "r") as file_handler2:
        reader = csv.DictReader(file_handler2)
        for row in reader:
            title = row["title"]
            year = row[" year"]
            genre = row[" genre"]
            duration = row[" duration"]
            if row["title"] == name:
                info = f"- {title}\n-{year}\n-{genre}\n-{duration}\n-{description}"
                print(info)
            if title not in titlelist:
                titlelist.append(title)
            else:
                duplicates_list.append(title)


def main(arguments):
    name = input("Film title: ")
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("-r", action="store_true")
    parser.add_argument("-d", action="store_true")
    args = parser.parse_args(arguments[1:])
    titles = []
    duplicates = []
    if args.r:
        path = Path(args.path)
        for file in path.rglob("*.csv"):
            search_file(file, name, titles, duplicates)
    else:
        search_file(file, name, titles, duplicates)
    print(duplicates)


if __name__ == "__main__":
    main(sys.argv)
