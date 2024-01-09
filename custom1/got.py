import argparse
import sys
import requests
import csv
import yaml
import json
from matplotlib import pyplot as plt

"""
korzystajac z api cytatow z gota pozwol uzytkownikowi utworzyc biblioteke w csv
50 losowych cytatow (--lib - arguments plik wyjsciowy)
potem stworz flagi --stats wylistuje  ile cytatow danej postaci --pie-plot wezmie
dane ze stats i zrobi wykres kolowy --plot-house pozwala na pokazanie wykresu cytatow tylko z rodu
podanego przez uzytkownika
"""


def quotes():
    quotes = []
    for _ in range(0, 51):
        quote = requests.get(
            "https://api.gameofthronesquotes.xyz/v1/random"
        ).json()
        quotes.append(quote)
    return quotes


def create_lib(path):
    quotes_list = quotes()
    with open(path, "w") as file_handler:
        fieldhouse = ["sentence", "name", "slug", "house_name"]
        writer = csv.DictWriter(file_handler, fieldhouse)
        writer.writeheader()
        for quote in quotes_list:
            writer.writerow(
                {
                    "sentence": quote["sentence"],  # noqa
                    "name": quote["character"]["name"],  # noqa
                    "slug": quote["character"]["slug"],  # noqa
                    "house_name": quote["character"]["house"]["name"],
                }  # noqa
            )


def lib_in_yaml(path):
    quotes_list = quotes()
    with open(path, "w") as file_handler:
        yaml.dump_all(quotes_list, file_handler)


def stats_get(path):
    with open(path, "r") as file_handler:
        reader = csv.DictReader(file_handler)
        house_dict = {}
        for row in reader:
            name = row["name"]
            if name not in house_dict:
                house_dict.update({name: 0})
            if name in house_dict:
                count = house_dict.get(name)
                house_dict.update({name: count + 1})
        return house_dict


def stats_print(path):
    house_dict = stats_get(path)
    for name in house_dict:
        info = f"{name} - {house_dict.get(name)} quotes"
        print(info)


def stats_from_yaml(path):
    with open(path, "r") as file_handler:
        data = yaml.load_all(file_handler)
        characters = []
        for row in data:
            name = row["character"]["name"]
            characters.append(name)
        set_of_characters = set(characters)
    print(set_of_characters)


def plot_pie(path):
    statistics = stats_get(path)
    x = []
    labels = []
    for name in statistics:
        x.append(statistics.get(name))
        labels.append(name)
    plt.pie(x, labels=labels)
    plt.show()


def get_stats_on_house(path):
    with open(path, "r") as file_handler:
        reader = csv.DictReader(file_handler)
        house_dict = {}
        for row in reader:
            house = row["house_name"]
            if house not in house_dict:
                house_dict.update({house: 0})
            if house in house_dict:
                count = house_dict.get(house)
                house_dict.update({house: count + 1})
        return house_dict


def plot_house(path):
    stats = get_stats_on_house(path)
    values = []
    labels = []
    for house in stats:
        labels.append(house)
        values.append(stats.get(house))
    plt.pie(values, labels=labels)
    save = plt.gcf()
    save.savefig("Save.pdf", format="pdf")
    plt.show()


# def save_house(path):
#         figure = plt.gcf()
#     if args.save:
#         figure.savefig(args.save, format="pdf")


def main(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?")
    parser.add_argument("--lib", action="store_true")
    parser.add_argument("--stats", action="store_true")
    parser.add_argument("--pie-plot", dest="pie_plot", action="store_true")
    parser.add_argument("--plot-house", dest="plot_house", action="store_true")
    parser.add_argument("--lib-in-yaml")
    parser.add_argument("--stats-yaml", action="store_true")
    args = parser.parse_args(arguments[1:])
    if args.path:
        path = args.path
    if args.lib:
        create_lib(path)
    if args.stats:
        stats_print(path)
    if args.pie_plot:
        plot_pie(path)
    if args.plot_house:
        plot_house(path)
    if args.lib_in_yaml:
        lib_in_yaml(args.lib_in_yaml)
    if args.stats_yaml:
        stats_from_yaml(path)


if __name__ == "__main__":
    main(sys.argv)
