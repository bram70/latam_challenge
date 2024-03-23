from typing import List, Tuple
import os
import pandas as pd
import json
import emoji
import regex
from collections import Counter

basePath = os.path.dirname(os.path.abspath(''))
def split_count(text):
    emoji_list = []
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.EMOJI_DATA for char in word):
            emoji_list.append(word)
    return emoji_list

def q2_time(file_path: str) -> List[Tuple[str, int]]:
    df = pd.read_json(basePath + file_path, lines=True)
    df= df[['content']]
    df['emojis'] = df['content'].apply(lambda x: split_count(str(x)))
    emojis=df['emojis']
    response = emojis.explode().dropna().value_counts().sort_index(ascending=False).sort_values(ascending=False)
    response = response.head(10)
    return list(response.items())