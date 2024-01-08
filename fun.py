import argparse
import sys


def main(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument("--add", nargs=2, type=int)
    args = parser.parse_args(arguments[1:])
    if args.add:
        value = add(args.add[0], args.add[1])
        print(value)


def add(value1, value2):
    return value1 + value2


if __name__ == "__main__":
    main(sys.argv)
