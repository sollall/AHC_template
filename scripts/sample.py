import time

start=time.time()

try:
    from pathlib import Path
    import sys
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from utils.inout import Test_IO

    PROB_NO=sys.argv[1]
    debug_mode=True
    test_io=Test_IO(PROB_NO)

    origin_print=print
    input=test_io.input
    print=test_io.output
except:
    debug_mode=False

