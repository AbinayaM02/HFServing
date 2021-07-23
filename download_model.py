""" Script to download the HF model to a local folder
    @author: AbinayaM02
"""

# Imports
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Specify model paths
hf_model_path = "sshleifer/distilbart-cnn-12-6"
local_model_path = "model/distilbart-cnn-12-6"

# Save the tokenizer and model locally
tokenizer = AutoTokenizer.from_pretrained(hf_model_path)
print("Tokenizer downloaded...")
tokenizer.save_pretrained(local_model_path)
print("Tokenizer saved locally...")
model = AutoModelForSeq2SeqLM.from_pretrained(hf_model_path)
print("Model downloaded...")
model.save_pretrained(local_model_path)
print("Model saved locally...")

