import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def visualize_bleu_scores(df):
    if 'Samples' in df.columns:
        samples = df.pop('Samples')
    else:
        samples = pd.Series([1] * len(df))

    model_language_scores = {}

    for col in df.columns:
        print(col.rsplit(' ', 1))
        model, language = col.rsplit(' ', 1)

        avg_score = (df[col] * samples).sum() / samples.sum()

        if model not in model_language_scores:
            model_language_scores[model] = {}
        model_language_scores[model][language] = avg_score

    avg_scores_df = pd.DataFrame(model_language_scores).T

    ax = avg_scores_df.plot(kind='bar', figsize=(12, 6), colormap='viridis', edgecolor='black')

    plt.title('Average Human Eval Scores per Model and Language', fontsize=14)
    plt.ylabel('Average Human Eval Score', fontsize=12)
    plt.xlabel('Model', fontsize=12)
    plt.xticks(rotation=0, fontsize=10)
    plt.legend(title='Language', fontsize=10, title_fontsize=12)
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    df = pd.read_csv('translation_humaneval.csv')
    #df.drop(columns=['input', 'translation_hindi', 'translation_spanish', 'translation_french',
    #        'GPT-4o_Hindi', 'GPT-4o_Spanish', 'GPT-4o_French', 'Llama-3-8B_Hindi',
    #        'Llama-3-8B_Spanish', 'Llama-3-8B_French', 'Mixtral_Hindi', 'Mixtral_Spanish',
    #        'Mixtral_French', 'Llama-3-70B_Spanish', 'Llama-3-70B_Hindi', 'Llama-3-70B_French', 'abc'], inplace=True)
    visualize_bleu_scores(df)
    df.to_csv('translation_humaneval_final.csv')
    print(df.head())
