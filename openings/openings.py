import csv
import argparse
import sys


def load_game(game):
    with open(game, "r") as file_handler:
        content = file_handler.readlines()
        lines = []
        for line in content:
            new_line = line.strip("\n")
            lines.append(new_line)
        content_str = "".join(lines)
    return content_str


def check_openings(openings, game):
    list_of_all = load_game(game)
    with open(openings, "r") as file_handler:
        reader = csv.DictReader(file_handler)
        matching_rows = []
        for row in reader:
            moves_list = row["moves"]
            moves_list_split = moves_list
            if moves_list_split in list_of_all:
                matching_rows.append(moves_list_split)
    if matching_rows == []:
        print("no openings found")
        return
    best_opening = max(matching_rows)
    with open(openings, "r") as file_handler:
        reader = csv.DictReader(file_handler)
        for row in reader:
            if row["moves"] == best_opening:
                print(row["name"])


def main(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument("openings")
    parser.add_argument("game")
    args = parser.parse_args(arguments[1:])
    openings = args.openings
    game = args.game
    check_openings(openings, game)


if __name__ == "__main__":
    main(sys.argv)
