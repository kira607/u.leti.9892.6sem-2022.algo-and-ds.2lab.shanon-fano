from coder import ShanonFanoCoder


def main():
    string = 'this is a test string'
    coder = ShanonFanoCoder()
    coder.decode(
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
        }
    )
    coder.print_info()


if __name__ == '__main__':
    main()