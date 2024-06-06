import sys
from bugFixLogic2 import *



def main():
    # Access command-line arguments
    # print('enterrrrrrrrrrrrrrrrrrrrrr')
    arguments = sys.argv[1:]
    code = arguments[0]
    function_name = arguments[1]
    inputs = arguments[2]
    outputs = arguments[3]
    # code = arguments[0]
    # Process the arguments
    # TODO: Add your code here
    bugFix(code, function_name, inputs, outputs)

if __name__ == "__main__":
    main()