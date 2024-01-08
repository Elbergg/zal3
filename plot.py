from matplotlib import pyplot as plt
import argparse
import sys
import json
from datetime import timedelta, datetime


def read_from_json(path, timestamp, values, fro=0, to=99999):
    charts = []
    with open(path, "r") as file_handle:
        data = json.load(file_handle)
        for value in values:
            return_data1 = []
            return_data2 = []
            for row in data:
                try:
                    if datetime.fromisoformat(row[timestamp]) > datetime.fromisoformat(
                        fro
                    ) and datetime.fromisoformat(
                        row[timestamp]
                    ) < datetime.fromisoformat(
                        to
                    ):
                        measurment = (row[timestamp], row[value])
                        return_data1.append(measurment[0])
                        return_data2.append(measurment[1])
                except KeyError:
                    pass
            charts.append((return_data1, return_data2))
    return charts


def generate_plot(data):
    for i, plot in enumerate(data):
        keys = data[i][0]
        values = data[i][1]
        plt.plot(keys, values)
    plt.show()


def main(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--timestamp", default="timestamp")
    parser.add_argument("--value", default="value", nargs="+")
    parser.add_argument("--fro")
    parser.add_argument("--to")
    args = parser.parse_args(arguments[1:])
    if args.path:
        data = read_from_json(args.path, args.timestamp, args.value, args.fro, args.to)
        generate_plot(data)


if __name__ == "__main__":
    main(sys.argv)
