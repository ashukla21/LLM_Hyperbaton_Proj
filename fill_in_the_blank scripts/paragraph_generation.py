import openai
import pandas as pd

openai.api_key = "" # Enter OpenAI key here 

def generate_paragraphs_with_gpt(input_file, output_file):
    data = pd.read_csv(input_file)
    
    if 'Hyperbaton ' not in data.columns:
        raise ValueError("Input CSV must have a 'Hyperbaton' column.")
    
    results = []

    for index, row in data.iterrows():
        hyperbaton = row["Hyperbaton "]

        # GPT prompt 
        prompt = (
            f"Generate a paragraph for the hyperbaton: '{hyperbaton}'. "
            "In the paragraph, include a blank (marked as ________) where the hyperbaton would fit. "
            "Provide three options for the blank:\n"
            "- Option 1: A rephrased or alternative version of the hyperbaton.\n"
            "- Option 2: A generic or less fitting phrase.\n"
            "- Option 3: The original hyperbaton, which fits best."
        )
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI assistant helping to generate tailored writing prompts."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            completion = response["choices"][0]["message"]["content"].strip()
            lines = completion.split("\n")
            paragraph_with_blank = lines[0].strip()
            options = [line.strip() for line in lines[2:6]]  # Extract first three options

            results.append({
                "Hyperbaton": hyperbaton,
                "Generated_Paragraph_with_Blank": paragraph_with_blank,
                "Option_1": options[0],
                "Option_2": options[1],
                "Option_3": options[2]
            })
        except Exception as e:
            print(f"Error processing hyperbaton '{hyperbaton}': {e}")
            continue

    output_df = pd.DataFrame(results)
    output_df.to_csv(output_file, index=False)
    print("Complete")

input_csv = ""  # Replace with your input file name
output_csv = ""  # Replace with output file name

generate_paragraphs_with_gpt(input_csv, output_csv)

