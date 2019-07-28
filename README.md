# Turing Machine

The goal of this project is to simulate Turing machine runs. 

## Introduction Guide

### Turing machine syntax

Turing machines must be defined in a text file using the same syntax used in [turingmachinesimulator.com](https://turingmachinesimulator.com/). For example, this would be a machine which only accepts odd binary numbers:

```
name: isOdd
init: q0
accept: qf

q0,0
q0,0,>

q0,1
q0,1,>

q0,_
q1,_,<

q1,1
qf,1,>
```

As you might notice the machine alphabet is not defined explicitly, so every printable character (except for spaces) can be given as inputs. Another limitation is that you can't represent a transition for every possible character (i.e `Σ`-transition).

### Loading the turing machine

Text files who follow this syntax can be loaded using the `from_file` method:
```python3
from turing_machine import TuringMachine

tm = TuringMachine.from_file("oddbinarymachine.txt")
```

If there are syntax errors the parser will raise a `ParsingError` exception. Comments (`//`) and empty lines will be skipped.

### Simulate a run

To simulate a run in the machine you should use the `run` method and pass the word as an argument:
```python3
result = tm.run("11010") # result = False
```

This method returns three possible values:
- `True`: if the run finishes in a final state (i.e the word is accepted by the machine)
- `False`: if the run finishes in a non-final state (i.e the word is rejected by the machine)
- `None`: if the run gets stucked in a configuration loop (i.e the run never ends)

If you are interested in differentiating between a rejected word and a run that doesn't stop you should compare the result value explicitly, because both `False` and `None` are _falsy_ values.

There is also a possibility for the machine to never stop but changing its configuration in every step, in a way that it never reaches the same configuration twice (i.e without falling in a configuration loop). If this is the case, the `run` method will never end.

### Runs with timeout

Cases where a run doesn't finish can't be caught easily, so the `run` method accepts an optional `timeout` parameter. With this parameter you can specify how many seconds the machine will run until the execution is aborted.

```python3
result = tm.run("11010", timeout=5) # result = False
```

By default there's no timeout limit, but if you specify this parameter and the time is exceeded during the run, the result will be `None`. If your machine is well designed and your input is not extremely big, runs should never take more than a second. If you set a timeout of a few seconds and your machine reaches the timeout, it's very likely that you are under an infinite run. 

### Additional data

The `run` method will only return decidability information, but it won't return the machine state nor the content of the tapes. That information is stored in the attributes of the machine, so you can access them as follows:
```python3
state = tm.current_state # state = 'q1'

tape_content = tm.tapes.words[0] # tape_content = ['1', '1', '0', '1', '0', '_']
```

For debugging purpuses you can also use the `print_current_configuration` method, which prints in a pretty format the actual configuration of the machine. For instance:
```
tm.print_current_configuration()
```

Which outputs:
```
State: q1
        V
1 1 0 1 0 _
```

### More examples

The machine and the code used in this introduction guide can be found in the [example1 folder](https://github.com/Mdelaf/turing-machine/tree/master/example1). 

In [example2 folder](https://github.com/Mdelaf/turing-machine/tree/master/example2) you can find a code for automatic revision of students homeworks.
