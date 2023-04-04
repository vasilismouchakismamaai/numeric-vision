from numeric_vision.utils import word_to_num
import argparse


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--text", type=str, required=True, help="sentence to extract numbers")

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    text = args.text
    match = word_to_num(text)
    print(f"the match is: {match}")