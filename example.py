import json
from coder import ShanonFanoCoder
from pprint import pprint


def split_iterable(iterable, w):
    splitted = []
    l = 0
    r = w
    while r < len(iterable):
        splitted.append(tuple(iterable[l:r]))
        l += w
        r += w
    splitted.append(tuple(iterable[r-w:]))
    return splitted


def squarify_string(string, w=30, sep='\n'):
    parts = split_iterable(string, w)
    result = sep.join((''.join(part) for part in parts))
    return result


encode_examples = [
    'It\'s easy to quit smoking. I\'ve done it hundreds of times.',
    'Many of life\'s failures are people who did not realize how close they were to success when they gave up.',
    'May the force be with you',
]

decode_examples = [
    ( 
        '011111111000100010001000111100001111100100110001001111011001100101',
        {
            'h': '11111',
            'a': '11110',
            'e': '1110',
            'r': '1101',
            'n': '1100',
            'g': '101',
            'i': '100',
            't': '011',
            's': '010',
            ' ': '00',
        },
    ),
    (
        '1111111101000100001010111111110001101100110101010010010111000110011000100101110110111'
        '1010000011111001110111100001010110010011010001110101011001110000110010111001001000011'
        '1101011100011010000010000101111001001010101111100110101100000001101000110111001110110',
        {
            "T": "111111",
            "v": "111110",
            ",": "111101",
            "x": "111100",
            "p": "111011",
            "o": "111010",
            "k": "111001",
            "c": "111000",
            "m": "110111",
            ".": "110110",
            "h": "11010",
            "f": "11001",
            "l": "11000",
            "d": "10111",
            "n": "10110",
            "u": "1010",
            "r": "1001",
            "i": "1000",
            "s": "0111",
            "t": "0110",
            "a": "010",
            "e": "001",
            " ": "000",
        },
    ),
    (
        '111111110010111011101010010000111110010101010011110111011011100101101011101010100001'
        '1101000110100101100011001100110001101001011000011100010000111010001101101110110',
        {
            "S": "111111",
            "d": "111110",
            "n": "11110",
            "'": "111011",
            "m": "111010",
            "g": "11100",
            "i": "11011",
            "y": "11010",
            "u": "1100",
            "c": "1011",
            "e": "1010",
            "s": "100",
            "t": "0111",
            ".": "0110",
            "o": "010",
            " ": "00",
        },
    ),
]


def get_coder_info(coder):
    sqstr = squarify_string(coder.string, 50)
    sqcode = squarify_string(coder.code, 50)
    sqcdsep = '\n'.join(str(p) for p in split_iterable(coder.code_sep, 7))
    sqcdt = '\n'.join(str(p) for p in split_iterable(list(coder.tree.get_codes_table().items()), 4))
    string = f'String (length: {len(coder.string)}, size: {coder.string_size}):\n{sqstr}'
    code = f'Code (size: {coder.code_size}):\n{sqcode}'
    code_sep = f'Code separated:\n{sqcdsep}'
    codes_table = f'Codes table:\n{sqcdt}'
    wc = f'Wrapping coefficient: {coder.wrapping_coefficient}'
    return '\n\n'.join((
        string,
        code,
        code_sep,
        wc,
        codes_table,
    ))


def run_encode_example(coder, i, string):
    print('Encode example', i, end='\n\n')
    coder.encode(string)
    print(get_coder_info(coder))
    print('\n', '=' * 120, '\n')


def run_decode_example(coder, i, code, decoder):
    print('Decode example', i, end='\n\n')
    coder.decode(code, decoder)
    print(get_coder_info(coder))
    print('\n', '=' * 120, '\n')


def run_encode_examples(coder):
    for i, s in enumerate(encode_examples, start=1):
        run_encode_example(coder, i, s)


def run_decode_examples(coder):
    for i, (code, decoder) in enumerate(decode_examples, start=1):
        run_decode_example(coder, i, code, decoder)


def main():
    coder = ShanonFanoCoder()
    run_encode_examples(coder)
    run_decode_examples(coder)


if __name__ == '__main__':
    main()