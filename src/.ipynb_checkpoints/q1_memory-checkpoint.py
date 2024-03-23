from typing import List, Tuple
from datetime import datetime
import os
import pandas as pd
import json
import ast

basePath = os.path.dirname(os.path.abspath(''))

def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    df = pd.read_json(basePath + file_path, lines=True)
    # Transformando el tipo de dato de las columnas
    for col in df.columns:
        if df[col].dtype == 'int64':
            df[col] = df[col].astype('int16')
        if df[col].dtype == 'float64':
            df[col] = df[col].astype('float16')

    df= df[['date', 'user']]
    # Transformando el dictionario "user" transformando cada key,value en columna
    df = df.join(df.user.apply(lambda x: pd.Series(ast.literal_eval(str(x)))))
    # Solo usamos la col date y la col username
    df= df[['date', 'username']]
    # Convertimos la columna fecha a tipo de dato fecha
    df['date'] = pd.to_datetime(df['date']).dt.date
    # Convertimos el username a minuscula
    df['username'] = df['username'].str.lower()
    # Seleccionamos el top 10 de fechas
    top_10_dates = df.groupby(['date']).size().sort_values(ascending=False).reset_index(name='count').head(10)

    # Seleccionamos solo el subconjunto dentro del top 10 de las fechas del dataframe original
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

    