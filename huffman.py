import sys
import heapq as hq

def H_T_C(Htree, code=""):
    '''If tree length is greater than 1 split the tree into recursive calls
    left branch and right branch'''
    if len(Htree) > 1:
        '''left branch is index 0 and add a 0 to the code because thats the left edge of a huffman tree
        right branch is index 1 and add 1 to the code because thats the right edge of a huffman tree'''
        return H_T_C(Htree[0], code+"0") +  H_T_C(Htree[1], code+"1")
    else:
        '''if length of the tree is 1 then you are at the leaf node and you can now return a tuple of the character 
        and the code within a list so it can be added to a larger list through the above return statement'''
        return [(Htree, code)]


def file_character_frequencies(file_name):
    # Suggested helper
    temp_dict = {}
    file = open(file_name)
    # iterate through the file character by character
    for line in file:
        for char in line:
            # get key value if it exists
            temp = temp_dict.get(char)
            # if it exists increment value
            if temp != None:
                temp_dict.update({char: temp+1})
            else:
                # if it does not exist add char with value 1
                temp_dict.update({char: 1})
    return temp_dict


class PriorityTuple(tuple):
    """A specialization of tuple that compares only its first item when sorting.
    Create one using double parens e.g. PriorityTuple((x, (y, z))) """

    def __lt__(self, other):
        return self[0] < other[0]

    def __le__(self, other):
        return self[0] <= other[0]

    def __gt__(self, other):
        return self[0] > other[0]

    def __ge__(self, other):
        return self[0] >= other[0]

    def __eq__(self, other):
        return self[0] == other[0]

    def __ne__(self, other):
        x = self.__eq__(other)
        return not x

def huffman_codes_from_frequencies(frequencies):
    '''convert the frequencies dictionary into a list of priority tuples
    the first item in the tuple must be the frequency so heapify can sort properly'''
    frequencies = [PriorityTuple((v, k)) for k, v in frequencies.items()]
    # heapify the list of priority tiples
    hq.heapify(frequencies)
    # do these steps |C|-1 times
    while len(frequencies) > 1:
        # extract the first min
        t1 = hq.heappop(frequencies)
        # extract the second min
        t2 = hq.heappop(frequencies)
        # merge the mins together
        t3 = PriorityTuple((t1[0] + t2[0], PriorityTuple((t1[1], t2[1]))))
        # insert the merged mins into the heap while maintaining the heap property
        hq.heappush(frequencies, t3)
    '''Now that you have a tre build convert the huffman tree into a dictionary of codes
    and then return the dictionary'''
    return dict(H_T_C(frequencies[0][-1]))



def huffman_letter_codes_from_file_contents(file_name):
    """WE WILL GRADE BASED ON THIS FUNCTION."""
    # Suggested strategy...
    freqs = file_character_frequencies(file_name)
    return huffman_codes_from_frequencies(freqs)


def encode_file_using_codes(file_name, letter_codes):
    """Provided to help you play with your code."""
    contents = ""
    with open(file_name) as f:
        contents = f.read()
    file_name_encoded = file_name + "_encoded"
    with open(file_name_encoded, 'w') as fout:
        for c in contents:
            fout.write(letter_codes[c])
    print("Wrote encoded text to {}".format(file_name_encoded))


def decode_file_using_codes(file_name_encoded, letter_codes):
    """Provided to help you play with your code."""
    contents = ""
    with open(file_name_encoded) as f:
        contents = f.read()
    file_name_encoded_decoded = file_name_encoded + "_decoded"
    codes_to_letters = {v: k for k, v in letter_codes.items()}
    with open(file_name_encoded_decoded, 'w') as fout:
        num_decoded_chars = 0
        partial_code = ""
        while num_decoded_chars < len(contents):
            partial_code += contents[num_decoded_chars]
            num_decoded_chars += 1
            letter = codes_to_letters.get(partial_code)
            if letter:
                fout.write(letter)
                partial_code = ""
    print("Wrote decoded text to {}".format(file_name_encoded_decoded))


def main():
    """Provided to help you play with your code."""
    filename = sys.argv[1]
    codes = huffman_letter_codes_from_file_contents(filename)
    print(codes)
    encode_file_using_codes(filename, codes)
    decode_file_using_codes(filename + "_encoded", codes)

'''
    import pprint
    frequencies = file_character_frequencies(sys.argv[1])
    pprint.pprint(frequencies)
    codes = huffman_codes_from_frequencies(frequencies)
    pprint.pprint(codes)'''


if __name__ == '__main__':
    """We are NOT grading you based on main, this is for you to play with."""
    main()