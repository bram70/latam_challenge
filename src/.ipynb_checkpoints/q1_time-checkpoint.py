from typing import List, Tuple
from datetime import datetime
import os
import pandas as pd
import json
basePath = os.path.dirname(os.path.abspath(''))

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    tweets = []
    # Leemos el archivo .json y lo adjuntamos en una lista
    with open(basePath + file_path, 'r') as file:
        for line in file:
            tweets.append(json.loads(line))
    # Convertimos la lista en un dataframe de panda
    df = pd.json_normalize(tweets)
    # Renombramos las columnas que tienen el prefijo "user." para obtener el username
    df.columns = [c.replace('user.', '') for c in df.columns]
    # Reducimos el dataframe solo a fecha y username
    df = df[['date', 'username']]
    # Convertimos la columna fecha a tipo de dato fecha
    df['date'] = pd.to_datetime(df['date']).dt.date
    # Convertimos el username a minuscula
    df['username'] = df['username'].str.lower()

    # Seleccionamos el top 10 de fechas
    top_10_dates = df.groupby(['date']).size().sort_values(ascending=False).reset_index(name='count').head(10)

    # Seleccionamos un subconjunto del dataframe original
    sub_df = df.loc[df['date'].isin(top_10_dates['date'])]

    response = []
    # Recorremos las 10 fechas con mas tweets
    for date_elem in top_10_dates['date']:
        # Solo las fechas que pertenecen a cada elemento iterado en el top10
        tmp_df = sub_df.query("date == @date_elem")
        # Dentro de ese subconjunto agrupamos por usuario y elegimos el top 1
        top_username = tmp_df.groupby('username').size().sort_values(ascending=False).reset_index(name='count').head(1)
        # Creamos la tupla y la anadimos a la lista de respuesta final
        response.append((date_elem, top_username['username'].iloc[0]))
    return response