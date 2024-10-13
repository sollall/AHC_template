import time

start = time.time()


def main(prob_id=None):
    try:
        from pathlib import Path
        import sys

        sys.path.append(str(Path(__file__).resolve().parent.parent))
        from utils.inout import replace_io

        debug_mode = True
        if prob_id is None:
            raise ValueError("Please specify the problem in debug mode.")
        replace_io(prob_id)
    except ModuleNotFoundError:
        debug_mode = False
    
    solve()

def solve():
    for _ in range(2):
        print(input())

if __name__ == "__main__":
    main(0)