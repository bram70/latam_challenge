from typing import List, Tuple
import os
import pandas as pd
import json
from collections import Counter

basePath = os.path.dirname(os.path.abspath(''))
def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    df = pd.read_json(basePath + file_path, lines=True)
    df= df['mentionedUsers']
    df_filtered = df.dropna()
    usermentioned = [[str(element['username']).lower() for element in list(row)] for row in df_filtered]
    new_list = Counter(x for xs in usermentioned for x in set(xs))
    return new_list.most_common(10)