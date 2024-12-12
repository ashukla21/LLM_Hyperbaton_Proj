from google.cloud import translate_v2 as translate
import pandas as pd

data = pd.read_csv('all_data_proper.csv')
translate_client = translate.Client()
results = translate_client.translate(
   data['Internet-sourced Hyperbatons'][:69].to_list(),
   target_language='fr',
)
print(results)

r = pd.DataFrame(results)
r.to_csv('online_sourced_translated_french.csv')


chunks = [data.iloc[i:i + 50]['Synthetically generated Hyperbaton'] for i in range(0, len(data), 50)]
print(chunks)
translated_chunks = []
try:
    for chunk in chunks:
        results = translate_client.translate(
            chunk.to_list(),
            target_language='fr',
        )
        translated_chunks.extend(results)
except Exception as e:
    print("error " + e)
r = pd.DataFrame(translated_chunks)
r.to_csv('synthetic_data_translated_french.csv')
