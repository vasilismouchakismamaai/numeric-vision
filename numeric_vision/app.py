from numeric_vision.utils import word_to_num

if __name__ == "__main__":
    text = "five million, minus three, point four"
    match = word_to_num(text)
    print(f"the match is: {match}")