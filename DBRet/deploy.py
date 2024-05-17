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

# db = VecDB()
# rng = np.random.default_rng(50)
# vectors = rng.random((10**4, 70), dtype=np.float32)
# records_dict = [{"id": i, "embed": list(row)} for i, row in enumerate(vectors)]
# db.insert_records(records_dict)
db = VecDB(file_path = PATH_M2Test,new_db=False)
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
M2CodeFiles=os.listdir(M2TestCodeDir)
# the files in the directory are named as test1.py, test2.py, test3.py, ... We sort according to number
M2CodeFiles=sorted(M2CodeFiles, key=lambda x: int(re.search(r'\d+', x).group()))


def query_db(code):
    global db, model, DEVICE
    query = get_embeddings(model, code, DEVICE)
    query = query.numpy()
    db_ids = db.retrieve(query, 3)
    # print(db_ids)
    codes=[]
    tests=[]
    for id in db_ids:
        # open json
        with open(os.path.join(M2TestCodeDir, M2CodeFiles[id])) as f:
            data = json.load(f)
            codes.append(data["code"])
            test=data["test_cases"]
            tests.append(test)
            # test=""
            # for testcase in data["test_cases"]:
            #     test+=testcase + '\n'
    return codes,tests
