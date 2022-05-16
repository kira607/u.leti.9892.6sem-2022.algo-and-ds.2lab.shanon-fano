import json
import helpers
import latex


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


def make_complexity_table():
    table = latex.LatexTable(
        2, 
        'l', 
        caption='Оценка временной сложности методов класса ShanonFanoCoder',
        caption_pos='bottom',
        label='complexity',
    )
    table.set_header('Метод', 'Оценка временной сложности')
    table.add_row(r'\verb|encode|', '$ O(n) $')
    table.add_row(r'\verb|decode|', '$ O(n) $')
    return table.render()


def make_encode_example(i, string):
    itstring = f'\\textit{{{string}}}'
    label = f'encode_example_{i}'
    pic = latex.LatexPicture(
        image=label,
        caption=f'Пример кодирования строки {i}',
        label=label,
    )
    example = f'\\subsubsection*{{Пример кодирования {i}}}\n\n'
    example += f'Входная строка: {itstring}\n\n'
    example += f'Пример выполнения представлен на рис. \\ref{{{pic.label}}}\n\n'
    example += pic.render()
    example += '\n\n'
    return example


def make_decode_example(i, code, decoder):
    label = f'decode_example_{i}'
    sq_code = helpers.squarify_string(code, 50, sep="\\\\\n")
    pic = latex.LatexPicture(
        image=label,
        caption=f'Пример декодирования строки {i}',
        label=label,
    )
    example = f'\\subsubsection*{{Пример декодирования {i}}}\n\n'
    example += (
        f'Входной код:\\\\ \n'
        f'\\textit{{\n'
        f'{sq_code}\n'
        f'}}\n\n'
    )
    example += (
        f'Входная таблица кодов:\\\\ \n'
        f'\\begin{{lstlisting}}\n'
        f'{json.dumps(decoder, indent=4)}\n'
        f'\\end{{lstlisting}}\n\n'
    )
    example += f'Пример выполнения представлен на рис. \\ref{{{pic.label}}}\n\n'
    example += pic.render()
    example += '\n\n'
    return example


def make_encode_examples():
    es = '\n\\subsection{Примеры кодирования}\n\n\n'
    for i, s in enumerate(encode_examples, start=1):
        es += make_encode_example(i, s)
    return es


def make_decode_examples():
    es = '\n\\subsection{Примеры декодирования}\n\n\n'
    for i, (c, d) in enumerate(decode_examples, start=1):
        es += make_decode_example(i, c, d)
    return es


def make_examples():
    title = '\\section{Примеры работы}\n\n'
    encode_examples = make_encode_examples()
    decode_examples = make_decode_examples()
    return title + encode_examples + decode_examples


def write_examples():
    path = '/home/kirill/programming/2lab-algo-3-2/report/modules/chapters/example.tex'
    with open(path, 'w+') as f:
        f.write(make_examples())


def main():
    write_examples()
    # print(make_complexity_table())


if __name__ == '__main__':
    main()
