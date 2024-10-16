import time

def main(params,prob_id=None):
    start = time.time()
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
    
    score=solve(**params)
    passed_time=time.time()-start

    return score, passed_time

### 以下が問題ごとに別途作成が必要な部分

def solve(epsilon,cooling_rate,epoch):
    for _ in range(2):
        print(input())
    return epoch

if __name__ == "__main__":
    solve()