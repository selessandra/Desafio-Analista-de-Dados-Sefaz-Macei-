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

total_ano = tabela_execucao.groupby(["Instituição", "UF", "ano"]).agg(
    total_pago=("Despesas Pagas", "sum"),
    populacao=("População", "first")
). reset_index()

total_ano["pago_per_capita_total"] = total_ano["total_pago"] / total_ano["populacao"]

# Separando maceió das outras capitais 
maceio = total_ano[total_ano["Instituição"].str.contains("Maceió")]
outras_capitais = total_ano[~total_ano["Instituição"].str.contains("Maceió")]

# Calculando média das outras capitais, anuais 
media_outras = outras_capitais.groupby("ano")["pago_per_capita_total"].mean().reset_index()
media_outras = media_outras.rename(columns={"pago_per_capita_total": "media_outras_capitais"})

# Junta Maceió com a média das outras, lado a lado, por ano
comparacao = maceio[["ano", "pago_per_capita_total"]].merge(media_outras, on="ano")
comparacao = comparacao.rename(columns={"pago_per_capita_total": "maceio_per_capita"})

print(comparacao.sort_values("ano"))

# Ranking de taxa de execução média por capital contendo todas as funções e anos 
ranking_execucao =(
    tabela_execucao.groupby(["Instituição", "UF"])["taxa_execucao"]
    .mean()
    .reset_index()
    .rename(columns={"taxa_execucao":"taxa_execucao_media"})
    .sort_values("taxa_execucao_media", ascending=False)
)

print(ranking_execucao)

# Ranking de gasto per capita total médio por capital, ranqueando todos os anos 
ranking_per_capta = (
    total_ano.groupby(["Instituição", "UF"])["pago_per_capita_total"]
    .mean()
    .reset_index()
    .rename(columns={"pago_per_capita_total": "media_per_capita"})
    .sort_values("media_per_capita", ascending=False)
)

print(ranking_per_capta)