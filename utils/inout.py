class Test_IO:
    def __init__(self,test_id):
        self.file_path=f"in/{str(test_id).zfill(4)}.txt"

        self.reader=self._readline()

        self.out_path=f"out/{str(test_id).zfill(4)}.txt"
        with open(self.out_path,"w") as f:
            pass
        return 
    def _readline(self):
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def input(self):
        return next(self.reader)
    
    def output(self,*args):
        with open(self.out_path,"a") as f:
            print(*args,file=f)

        return 