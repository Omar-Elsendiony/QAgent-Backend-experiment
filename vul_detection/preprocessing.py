import re
import inspect
import torch
from transformers import RobertaTokenizer, RobertaConfig, RobertaModel


class Preprocess:
    def __init__(self):
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = RobertaTokenizer.from_pretrained(
            "microsoft/codebert-base")
        self.model = RobertaModel.from_pretrained("microsoft/codebert-base")
        self.model.to(self.device)

    def clean_function_source(self, input_function):
        # Get the source code of the function

        # source_code = inspect.getsource(input_function)
        source_code = input_function

        # Find all variables in the function definition
        def_pattern = r'def\s+\w+\((.*?)\):'
        match = re.search(def_pattern, source_code)
        if match:
            params = match.group(1).split(',')
            params = [param.strip().split('=')[0].strip() for param in params]
        else:
            params = []

        # Find all variables that are assigned within the function
        assign_pattern = r'(\w+)\s*='
        assignments = re.findall(assign_pattern, source_code)

        # Combine the lists and remove duplicates
        all_variables = list(set(params + assignments))
        # Create a mapping from original variable names to var_i
        variable_mapping = {var: f'var_{i}' for i,
                            var in enumerate(all_variables)}

        # Replace the variable names in the source code
        for original_var, new_var in variable_mapping.items():
            # Use regex to replace whole words only to avoid partial replacements
            source_code = re.sub(
                r'\b' + re.escape(original_var) + r'\b', new_var, source_code)

        print(source_code)
        # print(all_variables)
        # Split the source code into lines
        lines = source_code.split('\n')

        # Remove comment lines
        cleaned_lines = [line if not line.strip().startswith(
            '#') else '' for line in lines]

        trimmed_lines = [re.sub(r'\s+', ' ', line) for line in cleaned_lines]
        trimmed_lines = [line.strip() for line in trimmed_lines]

        return trimmed_lines

    def generate_embeddings(self, func):
        # Clean the function source code
        cleaned_code_lines = self.clean_function_source(func)

        # Convert the cleaned code to a single string
        cleaned_code = '\n'.join(cleaned_code_lines)
        # print(cleaned_code)

        # Tokenize the entire function (function-level representation)
        # tokens_function = self.tokenizer(
        #     cleaned_code, return_tensors='pt', padding=True, truncation=True)

        # Tokenize and embed each statement (statement-level representation)
        tokens_statements = [self.tokenizer(
            statement, return_tensors='pt', padding=True, truncation=True) for statement in cleaned_code_lines]

        # Convert each statement embedding to a tensor
        tensors_statements = [self.model(
            **tokens).last_hidden_state.mean(dim=1) for tokens in tokens_statements]

        # # Convert the function embedding to a tensor
        # with torch.no_grad():
        #     output_function = self.model(**tokens_function)

        # embedding_function = output_function.last_hidden_state.mean(dim=1)[:, :514]

        return tensors_statements

    def generate_line_emdeddings(self, line):
        # Tokenize and embed the input line
        tokens_line = self.tokenizer(
            line, return_tensors='pt', padding=True, truncation=True)

        # Convert the line embedding to a tensor
        with torch.no_grad():
            tensor_line = self.model(
                **tokens_line).last_hidden_state.mean(dim=1)
        # print(tensor_line.shape)
        return tensor_line

# main function


def main():
    # Create a Preprocess object
    preprocess = Preprocess()

    # Define a simple function
    def simple_function(x, y, k):
        a = x + y
        # lol
        b = x * y

        Mohamed = 5 + x
        c = eval(input("Enter an expression: "))
        # lol
        return p

    # Generate embeddings for the simple function

    function_lines = preprocess.clean_function_source(simple_function)
    # print(function_lines)

    # Print the embeddings
    # print(embeddings)


# Call the main function
if __name__ == "__main__":
    main()
