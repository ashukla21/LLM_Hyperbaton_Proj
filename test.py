import openai

# Quick script to print out all models available to use 
openai.api_key = "" # Replace with your API key

models = openai.Model.list()
for model in models["data"]:
    print(model["id"])
