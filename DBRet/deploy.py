import numpy as np
# from .DiskANN import DiskANN
from .DiskANN import VecDB
# from DiskANN import VecDB
from .unixcoder import UniXcoder
import torch
import os
import json
import re
current_dir = os.path.dirname(__file__)
PATH_M2Test=os.path.join(current_dir,'M2Testindex')

Path_CatlasJ=os.path.join(current_dir,'CatlasJIndex8_clusters')
Path_CatlasPy=os.path.join(current_dir,'CatlasPyIndex5_clusters')

if os.path.exists(Path_CatlasJ):
  Jdb = VecDB(file_path = Path_CatlasJ,new_db=False)
  Pydb=VecDB(file_path = Path_CatlasPy,new_db=False)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = UniXcoder("microsoft/unixcoder-base")
model.to(DEVICE)

#returns numpy array of embeddings
def get_embeddings(model,tokens,device=DEVICE):
  tokens_ids = model.tokenize([tokens],max_length=512,mode="<encoder-only>")
  source_ids = torch.tensor(tokens_ids).to(device)
  _,embeddings = model(source_ids)
  return embeddings.detach()


# # Get the directory where Graph.py is located
M2TestCodeDir = os.path.join(current_dir, "M2TestCode")
# the files in the directory are named as test1.py, test2.py, test3.py, ... We sort according to number
# M2CodeFiles=sorted(M2CodeFiles, key=lambda x: int(re.search(r'\d+', x).group()))

CatlasJCodeDir = os.path.join(current_dir, "catlasM2UniDedup")

def query_db(code):
    global Jdb,Pydb, model, DEVICE
    query = get_embeddings(model, code, DEVICE)
    query = query.numpy()
    db_ids = Jdb.retrieve(query, 3)
    # print(db_ids)
    codes=[]
    tests=[]
    for id in db_ids:
        # open json
        with open(os.path.join(CatlasJCodeDir, f"test{id}.json")) as f:
            data = json.load(f)
            codes.append(data["code"])
            test=data["test_cases"]
            tests.append(test)
            # test=""
            # for testcase in data["test_cases"]:
            #     test+=testcase + '\n'
    return codes,tests
