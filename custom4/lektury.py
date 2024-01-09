import requests
import argparse
import sys
import yaml
import json
from matplotlib import pyplot as plt


def create_lib(file):
    books = requests.get("https://wolnelektury.pl/api/books/").json()
    with open(file, "w") as file_handler:
        yaml.dump_all(books, file_handler)


def b(tuple):
    return tuple[1]


def get_authors_stats(path):
    authors = {}
    with open(path, "r") as file_handler:
        data = yaml.load_all(file_handler)
        for row in data:
            author = row["author"]
            if author not in authors:
                authors.update({author: 1})
            if author in authors:
                counter = authors.get(author)
                authors.update({author: counter + 1})
    popular_list = authors.items()
    final_output = sorted(popular_list, key=b)
    final_output.reverse()
    return final_output


def plot_kind(path):
    with open(path, "r") as file_handler:
        data = yaml.load_all(file_handler)
        types = []
        for row in data:
            types.append(row["kind"])
        liric = types.count("Liryka")
        epic = types.count("Epika")
    plt.bar(("liryka", "epika"), ([liric, epic]))
    plt.show()


def plot_authors(path):
    data = get_authors_stats(path)
    labels = []
    values = []
    for author in data:
        labels.append(author[0])
        values.append(author[1])
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.show()


# def show_by_epoch(path, epoch)
# boo


def main(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument("--create-lib")
    parser.add_argument("path", nargs="?")
    parser.add_argument("--stats", action="store_true")
    parser.add_argument("--plot-authors", action="store_true")
    parser.add_argument("--plot-kind", action="store_true")
    parser.add_argument("--epoch")
    args = parser.parse_args(arguments[1:])
    if args.path:
        path = args.path
    if args.create_lib:
        create_lib(args.create_lib)
    if args.stats:
        print(get_authors_stats(path))
    if args.plot_authors:
        plot_authors(path)
    if args.plot_kind:
        plot_kind(path)
    if args.epoch:
        show_by_epoch(path, args.epoch)


if __name__ == "__main__":
    main(sys.argv)
