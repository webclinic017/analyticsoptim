import psycopg2
import pandas as pd
import torch
import torch.nn as nn

start = "2020-01-01"
end = "2020-01-03"
conn = psycopg2.connect(host="slave",
                        database="testdb1",
                        user="postgres",
                        password="reallyStrongPwd123")
cursor = conn.cursor()
symbols = ("MSFT", "GOOGL", "FB")
# query = f""" SELECT * from incertae."StockData" where symbol in %s and date between '{start}' AND '{end}' """

# cursor.execute(query, (symbols,))
# data = cursor.fetchall()
# df = pd.DataFrame(data)

query2 = f""" SELECT * from incertae."StockData" where symbol in {symbols} and date between '{start}' AND '{end}' """
df = pd.read_sql_query(query2, con=conn)
df.set_index(["date", "symbol"], inplace=True)
df = df.unstack()