import openai
import pandas as pd

openai.api_key = "" # Enter OpenAI key here 

# File paths
input_file = "" # Enter input file path here 
output_file = "" # Enter output file path here 

df = pd.read_csv(input_file)

def get_gpt_selection(paragraph, options):
    # Prompt
    prompt = f"""
    The following paragraph has a blank. Choose the option that best fits the blank:

    Paragraph:
    {paragraph}

    Options:
    """
    for i, option in enumerate(options):
        prompt += f"{i+1}. {option}\n"

    prompt += "\nRespond with just the option number that best fits the blank and not the entire sentence."
    print(prompt)
    
    # Call the OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="", # Enter gpt model here 
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10
        )
        reply = response["choices"][0]["message"]["content"]
        try:
            return reply[0]
        except (ValueError, IndexError):
            print(f"Unexpected response format: {reply}")
            return "Error"
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "Error"

gpt_choices = []
for _, row in df.iterrows():
    paragraph = row["Generated_Paragraph_with_Blank"]
    options = [row["Option_1"], row["Option_2"], row["Option_3"]]
    best_option = get_gpt_selection(paragraph, options)
    gpt_choices.append(best_option)

# Add the choices to the DataFrame
df["GPT_Selection"] = gpt_choices

df.to_csv(output_file, index=False)

output_file
