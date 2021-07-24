""" Script to run the summarization pipeline and expose the API
    @author:AbinayaM02
"""

# Imports
import torch
import os
from transformers.pipelines import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class Summarizer():

    def __init__(self, data, min_len = 75, max_len = 150):
        self.model_path = os.path.join(os.getcwd() + "/distilbart-cnn-12-6/")
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_path,
                                                        local_files_only=True)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path,
                                                    local_files_only=True)
        self.summarizer = pipeline('summarization', 
                                    model=self.model,
                                    tokenizer=self.tokenizer,
                                    device=0 if torch.cuda.is_available is True else -1)
        self.data = data
        self.min_len = min_len
        self.max_len = max_len

    def get_summary(self):
        output = self.summarizer(self.data,
                                min_length=self.min_len,
                                max_length=self.max_len)
        return {'summary':output}

class Summary(Resource):
    def post(self):
        try:
            # Decode json object from the request
            json_object = request.get_json()
            data = json_object["text"]
            minl = json_object["min_length"]
            maxl = json_object["max_length"]
            obj = Summarizer(data, minl, maxl)
        except Exception as e:
            return {"Message": "Error in creating Summarizer object" + str(e)}
        status = obj.get_summary()
        return status

api.add_resource(Summary, '/api/get-summary')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5069, debug = False)
