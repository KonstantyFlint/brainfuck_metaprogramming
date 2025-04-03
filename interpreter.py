from dataclasses import dataclass, field
from functools import cached_property, partial
from typing import Callable


@dataclass
class IOHandler:
    to_byte: Callable[[str], int] = field(default=ord)
    to_repr: Callable[[int], str] = field(default=chr)
    provide_input_str: Callable[[], str] = field(default=input)
    receive_output_str: Callable[[str], None] = field(default=partial(print, end=""))

    def provide_input(self) -> int:
        return self.to_byte(self.provide_input_str())

    def receive_output(self, value: int) -> None:
        self.receive_output_str(self.to_repr(value))


class Machine:

    def __init__(self, instructions: str, tape: list[int] | None = None, io_handler: IOHandler = IOHandler()):
        self.tape = tape or ([0] * 3000)
        self.instructions = instructions
        self.instruction_ptr = 0
        self.tape_ptr = 0
        self.io_handler = io_handler
        self.loop_cache = self.generate_cache()

    def generate_cache(self):
        result = {}
        begin_stack = []
        for i, c in enumerate(self.instructions):
            if c == "[":
                begin_stack.append(i)
            elif c == "]":
                begin = begin_stack.pop()
                result |= {
                    begin: i,
                    i: begin,
                }
        return result

    def __str__(self):
        return (f"Tape: {self.tape}\n"
                f"Instructions: {self.instructions}\n"
                f"Instruction Pointer: {self.instruction_ptr}\n"
                f"Tape Pointer: {self.tape_ptr}\n"
                f"Loop Cache: {self.loop_cache}\n"
                )

    @property
    def val(self):
        return self.tape[self.tape_ptr]

    @val.setter
    def val(self, value):
        self.tape[self.tape_ptr] = ((value % 256) + 256) % 256

    @property
    def halted(self):
        return self.instruction_ptr >= len(self.instructions)

    @property
    def instruction(self):
        return self.instructions[self.instruction_ptr]

    @cached_property
    def instruction_map(self):
        return {
            "+": self._increment,
            "-": self._decrement,
            ">": self._shift_right,
            "<": self._shift_left,
            ",": self._read,
            ".": self._write,
            "[": self._loop_begin,
            "]": self._loop_end,
        }

    def run(self):
        while not self.halted:
            self.step()

    def step(self):
        self.instruction_map[self.instruction]()
        self.instruction_ptr += 1

    def _increment(self):
        self.val += 1

    def _decrement(self):
        self.val -= 1

    def _shift_right(self):
        self.tape_ptr += 1

    def _shift_left(self):
        self.tape_ptr -= 1

    def _read(self):
        self.val = self.io_handler.provide_input()

    def _write(self):
        self.io_handler.receive_output(self.val)

    def _loop_begin(self):
        if self.val == 0:
            self.instruction_ptr = self.loop_cache[self.instruction_ptr]

    def _loop_end(self):
        if self.val != 0:
            self.instruction_ptr = self.loop_cache[self.instruction_ptr]
