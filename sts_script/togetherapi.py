from together import Together
import pandas as pd

client = Together()
resps = []

data = pd.read_csv('Synthetic Data - no normalized.csv')
for hyperbaton in data['Hyperbaton']:
    stream = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    messages=[{"role": "user", "content":
'''
A hyperbaton is a figure of speech in which the typical, natural order of words is changed as
certain words are moved out of order. The word hyperbaton is derived from the Greek phrase
hyperbatos meaning “transposed” or “inverted.” Each hyperbaton is based on a 'normal' sentence
without the unnatural word order. Based on the hyperbaton provided, return the corresponding
'normal' sentence. The output should NOT have any hyperbatons. Only output the normal sentence
and no other text. Examples: Hyperbaton sentence: And a small cabin build there, of clay and
wattles made. Normal sentence: And a small cabin made of clay and wattles was built there.
Hyperbaton sentence: One successful cake does not a good chef make. Normal sentence: One
successful cake does not make someone a good chef. Task: Hyperbaton sentence:
''' + hyperbaton + "Normal sentence: "}],
    stream=False,
    )

    resps.append(stream.choices[0].message.content)
    print(stream.choices[0].message.content)

df = pd.DataFrame(data = {'Normal sentence': resps})
df.to_csv('results.csv', sep=',',)

