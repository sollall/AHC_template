import time

start=time.time()

try:
    import sys

    from utils.inout import Test_IO

    PROB_NO=sys.argv[1]
    debug_mode=True
    test_io=Test_IO(PROB_NO)

    origin_print=print
    input=test_io.input
    print=test_io.output
except KeyboardInterrupt:
    debug_mode=False

