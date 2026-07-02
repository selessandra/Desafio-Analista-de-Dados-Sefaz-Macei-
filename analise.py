"""
Script de análise da base consolidada de despesas das capitais
(FINBRA/Siconfi), comparando o Empenhado e Pago
por função, com recortes adicionais de per capita e evolução temporal.
"""

import pandas as pd

# Lendo a base consolidada que foi criada 
df = pd.read_parquet("finbra_consolidado.parquet")

# Filtrando as linhas de "função", para indicador
df_funcao = df[df["tipo_conta"] == "função"]

tabela_execucao = df_funcao.pivot_table(
    index=["Instituição", "UF", "ano", "Conta"],
    columns="Coluna",
    values="Valor",
    aggfunc="sum"
)

# Calcula a Taxa de Execução: quanto do que foi empenhado, foi pago
tabela_execucao["taxa_execucao"] = (
    tabela_execucao["Despesas Pagas"] / tabela_execucao["Despesas Empenhadas"] * 100
)

# Reseta o índice para transformar a tabela pivotada de volta em colunas normais
tabela_execucao = tabela_execucao.reset_index()

populacao = df[["Instituição", "ano", "População"]]. drop_duplicates()

tabela_execucao = tabela_execucao.merge(populacao, on=["Instituição", "ano"], how="left")

tabela_execucao["pago_per_capita"] = (
    tabela_execucao["Despesas Pagas"] / tabela_execucao["População"]
)

print(tabela_execucao[["Instituição", "ano", "Conta", "Despesas Empenhadas", "Despesas Pagas", "taxa_execucao", "População", "pago_per_capita"]].head(10))