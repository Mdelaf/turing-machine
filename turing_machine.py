from turing_machine_parser import TuringMachineParser
from datetime import datetime


class Tapes:

    alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~'

    def __init__(self, word, number):
        if not isinstance(word, str):
            raise ValueError("Expected word to be a string")
        elif not all(symbol in Tapes.alphabet for symbol in word):
            raise ValueError("The word has invalid characters")

        self.current_positions = [0 for _ in range(number)]
        self.words = [list(word)] + [["_"] for _ in range(number - 1)]

    @property
    def current_symbols(self):
        return tuple(word[pos] for pos, word in zip(self.current_positions, self.words))

    def write_symbols(self, new_symbols):
        for pos, word, new_symbol in zip(self.current_positions, self.words, new_symbols):
            word[pos] = new_symbol

    def move_positions(self, movements):
        tape_number = 0
        for pos, word, movement in zip(self.current_positions, self.words, movements):
            if pos == 0 and movement == "<":
                word.insert(0, "_")
            elif pos == len(word) - 1 and movement == ">":
                word.append("_")
                self.current_positions[tape_number] += 1
            else:
                if movement == ">":
                    self.current_positions[tape_number] += 1
                elif movement == "<":
                    self.current_positions[tape_number] -= 1
            tape_number += 1


class TuringMachine:

    def __init__(self, name, initial_state, final_states, transitions):
        self.name = name
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions
        state, symbols = next(iter(transitions.keys()))
        self.number_of_tapes = len(symbols)
        self.tapes = None
        self.current_state = None

    @classmethod
    def from_file(cls, filename):
        with open(filename, "rt") as fp:
            parser = TuringMachineParser(fp)
            attributes = parser.parse()
        return TuringMachine(*attributes)

    def print_current_configuration(self):
        print(f"State: {self.current_state}")
        max_position = max(self.tapes.current_positions)
        copied_tapes = []
        for tape, pos in zip(self.tapes.words, self.tapes.current_positions):
            copied_tapes.append(["_"] * (max_position - pos) + list(tape))
        max_length = max(len(tape) for tape in copied_tapes)
        print(" " * max_position * 2 + "V")
        for tape in copied_tapes:
            print(" ".join(tape) + " _" * (max_length - len(tape)))

    def current_machine_configuration(self):
        return hash(str(self.tapes.current_positions) + str(self.tapes.words) + self.current_state)

    def next_step(self):
        return self.transitions.get((self.current_state, self.tapes.current_symbols), [None, None, None])

    def run(self, word, timeout=None):
        self.current_state = self.initial_state
        self.tapes = Tapes(word, self.number_of_tapes)
        configurations = {self.current_machine_configuration()}
        to_state, to_symbols, movements = self.next_step()
        start_time = datetime.now()
        while to_state:
            self.current_state = to_state
            self.tapes.write_symbols(to_symbols)
            self.tapes.move_positions(movements)
            new_configuration = self.current_machine_configuration()
            if new_configuration in configurations:
                return None
            configurations.add(new_configuration)
            to_state, to_symbols, movements = self.next_step()
            if timeout and (datetime.now() - start_time).total_seconds() >= timeout:
                return None
        return self.current_state in self.final_states
