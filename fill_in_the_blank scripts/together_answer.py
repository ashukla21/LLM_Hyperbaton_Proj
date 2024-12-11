import pandas as pd
import random
from together import Together


together_key = "" # Set your Together.ai API key
client = Together(api_key=together_key)

# File paths
input_file = "" # Enter input file path here 
output_file = "" # Enter output file path here 

df = pd.read_csv(input_file)

def get_model_selection(paragraph, options):
    
    # Create a prompt
    prompt = f"""
    The following paragraph has a blank. Choose the option that best fits the blank:

    Paragraph:
    {paragraph}

    Options:
    """
    for i, option in enumerate(options):
        prompt += f"{i+1}. {option}\n"

    prompt += "\nRespond with just the option number that best fits the blank."
    print(f"Prompt:\n{prompt}")
    
    try:
        response = client.chat.completions.create(
            model="", # Enter model here 
            messages=[{"role": "user", "content": prompt}]
        )
        
        for token in response:
            if hasattr(token, 'choices'):
                print(token.choices[0].delta.content)

    except Exception as e:
        print(f"Error with Together.ai API: {e}")
        return "Error"

gpt_choices = []
for _, row in df.iterrows():
    paragraph = row["Generated_Paragraph_with_Blank"]
    options = [row["Option_1"], row["Option_2"], row["Option_3"]]
    best_option = get_model_selection(paragraph, options)
    gpt_choices.append(best_option)


df["Together_Model"] = gpt_choices

df.to_csv(output_file, index=False)

print("Complete")
