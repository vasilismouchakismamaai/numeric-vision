from numeric_vision.config import *


def word_to_num(number_sentence):
    """
    function to return integer for an input `number_sentence` string
    input: string
    output: int or double or None
    """
    if type(number_sentence) is not str:
        raise ValueError(
            "Type of input is not string! Please enter a valid number word (eg. \'two million twenty three thousand and forty nine\')")
    if number_sentence.isdigit():  # return the number if user enters a number string
        return int(number_sentence)
    # split_words = number_sentence.replace('-', ' ').replace(',', ' ').lower().split()
    # split_words = number_sentence.replace('-', ' ').lower().split()
    split_words = _split_commas(number_sentence.replace('-', ' ').lower().split())

    words = _batch_numbers(split_words)
    # removing and, & etc.
    # clean_numbers = [word for word in split_words if word in NUMBER_WORDS]
    clean_numbers = _prepare_clean_numbers(words)
    output = []
    for item in clean_numbers:
        output.append(_clean_words_to_num(item))
    return output


def _split_commas(input_list):
    output_list = []

    for item in input_list:
        # if the item is only a ',' just append it in the output list
        if ',' in item and len(item) > 1:
            sub_items = item.split(',')
            for sub_item in sub_items:
                # after the strip a sub_item might be equal to "", so do not append it
                if sub_item != "":
                    output_list.append(sub_item.strip())
                output_list.append(',')
            output_list.pop() # Remove the last comma
        else:
            output_list.append(item)

    return output_list


def _batch_numbers(input_list):
    output_list = []
    temp = []
    for item in input_list:
        if item != ",":
            temp.append(item)
        else:
            output_list.append(temp)
            temp = []

    output_list.append(temp)
    
    return output_list


def _prepare_clean_numbers(input_list):
    output_list = []
    for item in input_list:
        temp = []
        for sub_item in item:
            word = _check_plural_section_word(sub_item)
            if word in NUMBER_WORDS:
                temp.append(word)
        output_list.append(temp)
    return output_list


def _clean_words_to_num(clean_words):
    _validate_clean_words(clean_words)
    negative_number = False
    clean_decimal_numbers = []
    # separate decimal part of number (if exists)
    if clean_words.count('point') == 1:
        clean_decimal_numbers = clean_words[clean_words.index('point') + 1:]
        clean_words = clean_words[:clean_words.index('point')]
        
    # separate negative part of number (if exists)
    if clean_words.count('minus') == 1:
        negative_number = True
        clean_words.remove('minus')
        
    total_sum = 0  # storing the number to be returned
    if len(clean_words) > 0:
        for word in SECTION_WORDS:
            word_index = clean_words.index(word) if word in clean_words else -1
            if word_index > -1:
                total_sum += _number_formation(clean_words[:word_index])
                clean_words = clean_words[word_index + 1:]
            total_sum *= 1000
        if clean_words:
            total_sum += _number_formation(clean_words)
        
    # adding decimal part to total_sum (if exists)
    if len(clean_decimal_numbers) > 0:
        decimal_sum = _get_decimal_sum(clean_decimal_numbers)
        total_sum += decimal_sum
    
    # if len(clean_negative_numbers) > 0:
    if negative_number:
        total_sum = f"-{total_sum}"
        if "." in total_sum: return float(total_sum)
        else: return int(total_sum)
        
    return total_sum


def _check_plural_section_word(word):
    # TODO: find better way to check for plural, it should work for other languages too
    for section_word in SECTION_WORDS:
        if word == section_word + "s":
            return section_word
    return word


def _number_formation(number_strings):
    """
    function to form numeric multipliers for million, billion, thousand etc.
    input: list of strings
    return value: integer
    """
    if not number_strings:
        return 1  # to correctly handle "a hundred and twelve", "thousand", etc
    hundred_index = number_strings.index('hundred') if 'hundred' in number_strings else -1
    number = 0
    if hundred_index >= 0:
        number = 100 * _number_formation(number_strings[0:hundred_index])
        number_strings = number_strings[hundred_index + 1:]
    number += sum([NUMBERS_ENGLISH[word] for word in number_strings])
    return number


def _get_decimal_sum(decimal_digit_words):
    """
    function to convert post decimal digit words to numerial digits
    input: list of strings
    output: double
    """
    decimal_number_str = []
    for dec_word in decimal_digit_words:
        if dec_word not in DECIMAL_WORDS:
            return 0
        else:
            decimal_number_str.append(NUMBERS_ENGLISH[dec_word])
    final_decimal_string = '0.' + ''.join(map(str, decimal_number_str))
    return float(final_decimal_string)


def _validate_clean_words(clean_words):
    # Error message if the user enters invalid input!
    if len(clean_words) == 0:
        raise ValueError(
            "No number words were found in the string.")
    # Error if user enters million, billion, thousand or decimal point twice
    if clean_words.count('thousand') > 1 \
        or clean_words.count('million') > 1 \
        or clean_words.count('billion') > 1 \
        or clean_words.count('point') > 1 \
        or clean_words.count('.') > 1 \
        or clean_words.count('minus') > 1 \
        or clean_words.count("-") > 1:
        raise ValueError(
            "Redundant number word! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")
        
    separators = list(filter(lambda x: x in ALL_SEPARATORS, clean_words))
    sorted_seps = sorted(separators, key=lambda i: ALL_SEPARATORS.index(i))
    if sorted_seps != separators:
        raise ValueError(
            "Malformed number! Something is out of order here.")
    

# def numwords_in_sentence(sentence):
#     if type(sentence) is not str:
#         raise ValueError(
#             "Type of input is not string! Please enter a valid number word (eg. \'two million twenty three thousand and forty nine\')")

#     # TODO: some way to tell the difference between "one thousand, two hundred, and three" = 1203 and
#     # TODO  "four, seven, twelve, three" = "4, 7, 12, 3"
#     number_sentence = sentence.replace('-', ' ').replace(',', ' ').lower()
#     split_words = number_sentence.strip().split()  # strip extra spaces and split sentence into words

#     last_found_index = 0
#     new_sentence = ''
#     i = 0
#     while i < len(split_words):
#         if split_words[i] in NUMBER_WORDS:
#             num_words = split_words[i - 1:i + 1] if i > 0 and split_words[i - 1] == 'a' else [split_words[i]]
#             clean_words = [split_words[i]]
#             while i + 1 < len(split_words) and split_words[i + 1] in NUMBER_SAFE_WORDS:
#                 i += 1
#                 num_words.append(split_words[i])
#                 if split_words[i] in NUMBER_WORDS:
#                     clean_words.append(split_words[i])
#             num = _clean_words_to_num(clean_words)
#             replace_start, replace_end = _get_replaceable(number_sentence, num_words, last_found_index)
#             new_sentence += sentence[last_found_index:replace_start] + str(num)
#             last_found_index = replace_end
#         i += 1

#     new_sentence += sentence[last_found_index:]
    
#     return new_sentence


# def _get_replaceable(sentence, clean_words, last_found_index):
#     start = sentence[last_found_index:].find(clean_words[0]) + last_found_index
#     end = start + len(clean_words[0])
#     for word in clean_words[1:]:
#         end += sentence[end:].lower().find(word) + len(word)
#     return start, end
