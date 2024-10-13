import importlib
import sys

def run_dynamic_import(module_name,prob_no):
    try:
        # モジュールを動的にインポート
        module = importlib.import_module(module_name)
        # インポートされたモジュールからmain関数を呼び出し
        if hasattr(module, "main"):
            return module.main(prob_no)
        else:
            raise Exception(f"Module '{module_name}' does not have a 'main' function.")
    except ModuleNotFoundError:
        raise Exception(f"Module '{module_name}' not found.")

if __name__ == "__main__":
    NUM_TESTS=1

    if len(sys.argv) > 1:
        module_name = sys.argv[1]
        for i in range(NUM_TESTS):
            run_dynamic_import(module_name,i)
    else:
        print("Please provide a module name as an argument.")