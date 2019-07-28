from turing_machine import TuringMachine

tm = TuringMachine.from_file("oddbinarymachine.txt")

result = tm.run("11010")
print('result = tm.run("11010") # result =', result)

state = tm.current_state
print('state = tm.current_state # state =', state)

tape_content = tm.tapes.words[0]
print('tape_content = tm.tapes.words[0] # tape_content =', tape_content)

tm.print_current_configuration()
