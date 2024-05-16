import numpy as np
from DiskANN import VecDB
from unixcoder import UniXcoder
import torch
import os
import json
import re
PATH_M2Test='M2Testindex'

db = VecDB(file_path = PATH_M2Test, new_db = False)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = UniXcoder("microsoft/unixcoder-base")
model.to(DEVICE)

#returns numpy array of embeddings
def get_embeddings(model,tokens,device=DEVICE):
  tokens_ids = model.tokenize([tokens],max_length=512,mode="<encoder-only>")
  source_ids = torch.tensor(tokens_ids).to(device)
  _,embeddings = model(source_ids)
  return embeddings.detach()

M2TestCodeDir='M2TestCode'
M2CodeFiles=os.listdir(M2TestCodeDir)
# the files in the directory are named as 1.py, 2.py, 3.py, ... I want them sorted according to number
# M2CodeFiles.sort(key=lambda x: int(x.split('.')[0]))
# the files in the directory are named as test1.py, test2.py, test3.py, ... I want them sorted according to number
M2CodeFiles=sorted(M2CodeFiles, key=lambda x: int(re.search(r'\d+', x).group()))


def query_db(code):
    global db, model, DEVICE
    query = get_embeddings(model, code, DEVICE)
    query = query.numpy()
    db_ids = db.retrieve(query, 3)
    # print(db_ids)
    codes=[]
    tests=[]
    for _,id in db_ids:
        # open json
        with open(os.path.join(M2TestCodeDir, M2CodeFiles[id])) as f:
            data = json.load(f)
            codes.append(data["code"])
            test=data["test_cases"]
            tests.append(test)
            # test=""
            # for testcase in data["test_cases"]:
            #     test+=testcase + '\n'
    return codes

code='lol'

print(query_db(code))