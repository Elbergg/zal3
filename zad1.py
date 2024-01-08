import argparse
from random import choice, randint
import sys


def main(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument("--possible_seperators")
    parser.add_argument("--padding_digits")
    parser.add_argument("--symbols_number")
    parser.add_argument("--padding_symbols")
    parser.add_argument("--words_number")
    parser.add_argument("--minimal_word_length")
    parser.add_argument("--maximal_word_length")
    parser.add_argument("--generated_passwords")
    parser.add_argument("--padding_symbols_number")

    args = parser.parse_args(arguments[1:])

    for _ in range(int(args.generated_passwords)):
        selected_words = []
        with open("words.txt", "r") as file_handler:
            words = [word.rstrip() for word in file_handler]
            for _ in range(int(args.words_number)):
                selected_word = ""
                if args.minimal_word_length or args.maximal_word_length:
                    while len(selected_word) < int(
                        args.minimal_word_length
                    ) or len(selected_word) > int(args.maximal_word_length):
                        selected_word = choice(words)
                        selected_words.append(selected_word)
                else:
                    selected_word = choice(words)
                    selected_words.append(selected_word)
            # print(selected_words)
        padding_symbol = choice(args.padding_symbols)
        padding_digits = [
            str(randint(0, 9)) for i in range(int(args.padding_digits))
        ]
        final_padding_digits = "".join(padding_digits)
        seperator = choice(args.possible_seperators)
        core = f"{seperator}"
        for i in range(int(args.words_number)):
            core += f"{selected_words[i]}{seperator}"
        border = f"{padding_symbol*int(args.padding_symbols_number)}{final_padding_digits}"
        print(f"{border}{core}{border}")


if __name__ == "__main__":
    main(sys.argv)
