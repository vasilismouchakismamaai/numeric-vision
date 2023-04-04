from numeric_vision.utils import word_to_num

if __name__ == "__main__":
    text = "minus point two"
    match = word_to_num(text)[0]
    print(type(match))
    print(f"the match is: {match}")