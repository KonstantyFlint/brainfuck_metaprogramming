PLUS_BYTE = ord("+")
RIGHT_BYTE = ord(">")

LEFT = "<"
RIGHT = ">"


def set_value(value: int, current_value=0, free_space: str = LEFT):
    """
    Sets the value of the current cell. Requires one free space to the left or to the right.
    """
    assert free_space in (LEFT, RIGHT)

    go_to_free, go_back = "<", ">"
    if go_to_free != free_space:
        go_to_free, go_back = go_back, go_to_free

    diff = (value - current_value + 256) % 256

    tens = diff // 10
    digit = diff % 10

    result = "+" * digit
    if tens > 0:
        result = f"{result}{go_to_free}{'+' * tens}[-{go_back}{'+'*10}{go_to_free}]{go_back}"
    return result


def reset():
    return "[-]"


def set_values(code: str):
    result = ""
    result += ">>>>"
    result += ">".join("+" * ord(char) for char in code) + ">"
    return result


def replicate_cell():
    """
    recreate code that sets the value to the cell 1 right, move that value 2 spaces to the left
    """
    result = ""
    result += set_value(PLUS_BYTE)
    result += ">"
    result += "[-<.<+>>]"

    result += "<" + set_value(value=RIGHT_BYTE, current_value=PLUS_BYTE, free_space=">") + "." + reset()

    return result


def replicate_tape():
    """
    print code that generates the current content of the tape
    shift tape 2 to the left
    """

    result = ""

    result += "<[<]<<<"

    # print >>>>
    result += ">"
    result += set_value(RIGHT_BYTE)
    result += "...."
    result += reset()

    # move the pointer to the data
    result += ">>>"

    result += f"[<{replicate_cell()}>>]"

    result += "<<<[<]"

    return result


def print_tape():
    return ">[.>]"


OPUS_MAGNUM = set_values(replicate_tape() + print_tape()) + replicate_tape() + print_tape()

print(OPUS_MAGNUM)
