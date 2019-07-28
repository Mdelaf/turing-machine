from turing_machine import TuringMachine
from os import listdir

TESTS = [
    ("1", True),
    ("00.10", True),
    ("00.01", True),
    ("0001.0010.0100.1000", True),
    ("1000.1010.1100", True),
    ("10000000000.10000001000.10000010000", True),
    ("010001.100000.110001.110011.110101", True),
    ("00000", True),
    ("00000001.00000010.00000101.00100001", True),
    ("0000.0001.0010.0011.0100.0110.0111.1000.1001", True),

    ("1.0", False),
    ("00.10.01", False),
    ("110.111.111", False),
    ("000.001.100.010", False),
    ("00.01.10.11.11", False),
    ("00000.00010.00010", False),
    ("010.101.100", False),
    ("1.1", False),
    ("00.00", False),
    ("10.10", False),
]


BONUS_TESTS = [
    ("1.10.100", True),
    ("0.011.100.01000", True),
    ("1.010.11.001000", True),
    ("0000.10.0100.10000", True),
    ("10.011.1100", True),

    ("1.000.10", False),
    ("110.111.11", False),
    ("0.000", False),
    ("000.01", False),
    ("100.110.000", False),
]


if __name__ == "__main__":
    folder = 'input_machines'
    timeout = 8
    for filename in listdir(folder):
        filepath = f"{folder}/{filename}"
        username = filename.upper().split(".TXT")[0]
        tm = TuringMachine.from_file(filepath)

        print(username, end="\t")
        for word, expected in TESTS:
            result = tm.run(word, timeout=timeout)
            value = "1" if result is expected else "0"
            print(value, end="\t")

        for word, expected in BONUS_TESTS:
            result = tm.run(word, timeout=timeout)
            value = "1" if result is expected else "0"
            print(value, end="\t")
        print()
