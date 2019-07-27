class TuringMachineParser:

    class ParsingError(Exception):
        pass

    def __init__(self, file_object):
        self.file_object = file_object
        self.tapes = None
        self.current_line = None

    def filtered_lines(self):
        self.current_line = 1
        for line in self.file_object:
            line = line.strip()
            if line and not line.startswith("//"):
                yield line.split("//")[0]
            self.current_line += 1

    def parse_machine_name(self, line):
        if not line.startswith("name:"):
            raise TuringMachineParser.ParsingError(f"Machine name expected, but {line} was found")
        return line[5:].strip()

    def parse_initial_state(self, line):
        if not line.startswith("init:"):
            raise TuringMachineParser.ParsingError(f"Initial state expected, but {line} was found")
        return line[5:].strip()

    def parse_final_states(self, line):
        if not line.startswith("accept:"):
            raise TuringMachineParser.ParsingError(f"Final states expected, but {line} was found")
        return line[7:].strip().split(",")

    def parse_transition_input(self, line):
        state, *symbols = [substring.strip() for substring in line.split(",")]
        if any((" " in substring) or ("" == substring) for substring in [state, *symbols]):
            raise TuringMachineParser.ParsingError(f"Invalid format in line {self.current_line}")
        tapes_used = len(symbols)
        if self.tapes is None:
            self.tapes = tapes_used
        if self.tapes != tapes_used:
            raise TuringMachineParser.ParsingError(f"Invalid format in line {self.current_line}")
        return state, tuple(symbols)

    def parse_transition_output(self, line):
        state, *symbols_and_movements = [substring.strip() for substring in line.split(",")]
        if any((" " in substring) or ("" == substring) for substring in [state, *symbols_and_movements]):
            raise TuringMachineParser.ParsingError(f"Invalid format in line {self.current_line}")
        if len(symbols_and_movements) != self.tapes * 2:
            raise TuringMachineParser.ParsingError(f"Invalid format in line {self.current_line}")
        symbols = symbols_and_movements[:self.tapes]
        movements = symbols_and_movements[self.tapes:]
        return state, tuple(symbols), tuple(movements)

    def parse(self):
        lines = self.filtered_lines()
        name = self.parse_machine_name(next(lines))
        initial_state = self.parse_initial_state(next(lines))
        final_states = self.parse_final_states(next(lines))
        transitions = {}
        input_line = next(lines, None)
        while input_line:
            output_line = next(lines, None)
            if output_line is None:
                TuringMachineParser.ParsingError(f"Transition continuation expected after line {self.current_line}")
            state, symbols = self.parse_transition_input(input_line)
            new_state, new_symbols, movements = self.parse_transition_output(output_line)
            transitions[(state, symbols)] = (new_state, new_symbols, movements)
            input_line = next(lines, None)
        return name, initial_state, final_states, transitions
