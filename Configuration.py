from Imports import *
load_dotenv()

MODEL = os.getenv("MODEL")
# model_id = "bigcode/starcoder2-15b"
model_id = "google/gemma-7b-it"
model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"


max_new_tokens = 6000
if "Mixtral" in model_id:
    max_new_tokens = 29_000

if (MODEL == "GPT-3.5-turbo"):
    llm, chat_model = InitializeGptModel(
        os.environ["OPENAI_API_KEY"], model_id, max_new_tokens=max_new_tokens
    )
    # queryGptGenerateTest()
else:
    llm, chat_model = InitializeModel(
        os.environ["HUGGINGFACEHUB_API_TOKEN"], model_id, max_new_tokens=max_new_tokens
    )
    GenUnitTestChain = InitializeTestChain(llm, True)


UnitTestFeedbackChain = InitializeFeedbackChain(llm)


judgeChain = InitializeJudgeChain(llm)

bugFixChain = InitializeBugFixChain(llm)


HEval_JsonObj = pd.read_json(path_or_buf="Datasets/humaneval.jsonl", lines=True)
db = connectDB()
