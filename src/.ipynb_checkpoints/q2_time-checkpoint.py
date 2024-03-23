from typing import List, Tuple
import os
import pandas as pd
import json
import emoji
import regex
from collections import Counter

basePath = os.path.dirname(os.path.abspath(''))
# Esta funcion retorna una lista de emojis encontradas en un text tipo str
def split_count(text: str) -> List[str]:
    emoji_list = []
    # elegimos todas las coincidencias con el escape de unicode
    data = regex.findall(r'\X', text)
    for word in data:
        # Usamos la libreria emoji para confirmar si cada unicode es un emoji
        if any(char in emoji.EMOJI_DATA for char in word):
            emoji_list.append(word)
    return emoji_list

def q2_time(file_path: str) -> List[Tuple[str, int]]:
    df = pd.read_json(basePath + file_path, lines=True)
    #Obtenemos solo la columna content del dataframe original
    df= df[['content']]
    # Aplicamos la busqueda de la lista de emojis a cada fila de la columna "content"
    df['emojis'] = df['content'].apply(lambda x: split_count(str(x)))
    # eliminar listas vacias, contar cada emoji y ordenar descendente el contador de cada emoji
    emojis = df['emojis'].explode().dropna().value_counts().sort_index(ascending=False).sort_values(ascending=False)
    # retorna lista de top 10
    return list(emojis.head(10).items())