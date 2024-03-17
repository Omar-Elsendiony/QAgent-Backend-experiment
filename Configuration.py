from Imports import *

load_dotenv()
# model_id="google/gemma-7b-it"
model_id="mistralai/Mixtral-8x7B-Instruct-v0.1"
max_new_tokens= 6000
if 'Mixtral' in model_id:
    max_new_tokens= 31_000

llm, chat_model = InitializeModel(os.environ['HF_TOKEN'], model_id,
                                  max_new_tokens= max_new_tokens)
if 'Mixtral' in model_id:
    GenUnitTestChain= InitializeTestChain(llm,True)
else:
    GenUnitTestChain= InitializeTestChain(chat_model,True)

if 'Mixtral' in model_id:
    UnitTestFeedbackChain= InitializeFeedbackChain(llm)
else:
    UnitTestFeedbackChain= InitializeFeedbackChain(chat_model)


HEval_JsonObj = pd.read_json(path_or_buf='humaneval.jsonl', lines=True)
db = connect_db()