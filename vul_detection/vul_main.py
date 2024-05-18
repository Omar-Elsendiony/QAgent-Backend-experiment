import torch
import torch.nn as nn
from .preprocessing import Preprocess
from .tests import functions
import os

current_dir = os.path.dirname(__file__)


class BertForLineClassification(torch.nn.Module):
    def __init__(self):
        super(BertForLineClassification, self).__init__()
        # self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.dropout = torch.nn.Dropout(0.1)
        self.classifier = torch.nn.Linear(768, 8)  # 8 is the number of labels
        # self.preprocessor = preprocessing.Preprocessor()
        self.preprocessor = Preprocess()

    def forward(self, input_tensor):
        # outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        # pooled_output = outputs.pooler_output
        pooled_output = self.dropout(input_tensor)
        logits = self.classifier(pooled_output)
        return logits


def infere(model, lines_tensor):
    logits = model(lines_tensor)
    _, predicted = torch.max(logits, 1)
    return predicted


def main_vul(function):
    # Load the saved model
    model = BertForLineClassification()
    PATH_bert = os.path.join(current_dir, 'bert_model_generic_2.pth')

    model.load_state_dict(torch.load(PATH_bert))
    model.eval()  # Put the model in evaluation mode for inference
    # train model after load it
    lines_tensors = model.preprocessor.generate_embeddings(function)
    # cleaned_func = model.preprocessor.clean_function_source(functions)
    vul_lines = list()
    for i in range(len(lines_tensors)):
        predicted = infere(model, lines_tensors[i])
        norm_prediction = int(predicted // 2)
        if norm_prediction == 1 or norm_prediction == 2:
            lol = dict()
            lol['line_number'] = i
            lol['vul_level'] = norm_prediction
            vul_lines.append(lol)
    return vul_lines


# print(functions[1])
print(main_vul(functions[1]))
