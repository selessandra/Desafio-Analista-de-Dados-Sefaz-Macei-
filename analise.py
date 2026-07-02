"""
Script de análise da base consolidada de despesas das capitais
(FINBRA/Siconfi), comparando o Empenhado e Pago
por função, com recortes adicionais de per capita e evolução temporal.
"""

import pandas as pd

# Lê a base já consolidada e tratada, gerada por consolidar_dados.py
df = pd.read_parquet("finbra_consolidado.parquet")



print(f"Total de linhas carregadas: {len(df)}")
print(df.head())

# Filtra só as linhas de função, para o primeiro indicador
df_funcao = df[df["tipo_conta"] == "função"]

tabela_execucao = df_funcao.pivot_table(
    index=["Instituição", "UF", "ano", "codigo_funcao"],
    columns="Coluna",
    values="Valor",
    aggfunc="sum"
)

print(tabela_execucao.head())