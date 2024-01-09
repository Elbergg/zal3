import argparse
import sys


def main(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument("string")
    args = parser.parse_args(arguments[1:])
    code = args.string
    code_without_zero = []
    for letter in code:
        if letter == "0":
            pass
        else:
            code_without_zero.append(letter)
    code_second_ver = "".join(code_without_zero)
    numbers = []
    letters = []
    for letter in code_second_ver:
        try:
            number = int(letter)
            numbers.append(letter)
        except:
            ValueError
            letters.append(letter)
    first_name = ""
    last_name = ""
    output = {}
    id = "".join(numbers)
    capital = False
    for letter in letters:
        if letter.isupper() is True and capital is False:
            capital = True
            first_name += letter
            continue
        if letter.isupper() is False and capital is True:
            first_name += letter
            continue
        if letter.isupper() is True and capital is True:
            last_name += letter
            capital = False
            continue
        if letter.isupper() is False and capital is False:
            last_name += letter
            continue

    output.update({"first_name": first_name})
    output.update({"last_name": last_name})
    output.update({"id": id})
    print(output)
    pass


if __name__ == "__main__":
    main(sys.argv)
