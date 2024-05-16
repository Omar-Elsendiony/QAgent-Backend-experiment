from flask import Flask, request, jsonify
from flask_cors import CORS  # import flask_cors
from Pipeline_Interface import QAgent_product
app = Flask(__name__)
CORS(app)  # enable CORS
from Configuration import *
from MainFunctions.TestGenerator import *
from MainFunctions.TestFix import *
from MainFunctions.DecisionMaker import *
from MainFunctions.BugFix import *

def setupQAgent():
    try:
        print("All imports successful!")
        testGenerator = TestGenerator(GenUnitTestChain, db, globals())
        testRegenerator = TestFix(
            UnitTestFeedbackChain,
            globals(),
            True,
        )
        judgeGenerator = DecisionMaker(judgeChain, globals())
        bugFixGenerator = BugFix(bugFixChain, globals(), True)
        return testGenerator, testRegenerator, bugFixGenerator, judgeGenerator
    except Exception as e:
        print(e)
        exit(-1)

testGenerator, testRegenerator, bugFixGenerator, judgeGenerator = setupQAgent()

@app.route('/run-qagentai', methods=['POST'])
def run_python():
    code = request.json.get('code')
    description = request.json.get('description')
    if code:
        try:
            # execute the main function
            result = QAgent_product(code, description, testGenerator, testRegenerator, bugFixGenerator, judgeGenerator)
            print(result)
            return jsonify({'output': list(result)})
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'No code provided'}), 400

if __name__ == '__main__':
    app.run(port=5000)