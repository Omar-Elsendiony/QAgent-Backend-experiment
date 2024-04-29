try:
    from Configuration import *
    from Benchmark.TestGenerator import *
    from Benchmark.TestFix import *
    from Benchmark.DecisionMaker import *
    from Benchmark.BugFixBench import *
    from Benchmark.BugFix import *

    # llm_arb, chat_model_arb = InitializeModelArbiter(os.environ["HUGGINGFACEHUB_API_TOKEN"],repo_id='mistralai/Mixtral-8x7B-Instruct-v0.1')
    # with open(r"Datasets/atcoder_problem_test_cases_description.jsonl", "r") as f:
    #     data = f.read()
    #     jsonObj = json.loads(data)
    # jsonObj=pd.read_json(path_or_buf="Datasets/atcoder_problem_test_cases_description.jsonl")
    # jsonObj=pd.read_json(path_or_buf="Datasets/cleanedhumaneval.json")
    # # jsonObj = HEval_JsonObj
    # testGenerator = TestGenerator(GenUnitTestChain, db, jsonObj, globals())
    # testGenerator.isHumanEval=False
    # testRegenerator = TestFix(UnitTestFeedbackChain,True,globals())
    # judgeGenerator = DecisionMaker(judgeChain,globals())
    # bugFixGenerator = BugFix(bugFixChain,True,globals())
    bugFixGeneratorben = BugFixBench(bugFixChainben, True, globals())
except Exception as e:
    print(e)
    exit(-1)
