from interpreter import IOHandler, Machine
from self_replication import OPUS_MAGNUM


def capture_output(code):
    output_list = []
    capturing_handler = IOHandler(receive_output_str=output_list.append)
    Machine(code, io_handler=capturing_handler).run()
    return "".join(output_list)


def test_code_equal_to_output():
    assert OPUS_MAGNUM == capture_output(OPUS_MAGNUM)
