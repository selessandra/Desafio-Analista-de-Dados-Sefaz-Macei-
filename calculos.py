"""
Funções de cálculo dos indicadores da base FINBRA/Siconfi:
taxa de execução, per capita e rankings. Centraliza a lógica usada
tanto em analise.py (investigação) quanto em graficos.py (visualização).
"""

import pandas as pd


def carregar_base(excluir_2025=True):
    """Lendo base e removendo o ano de 2025, que está incompleto"""
    df = pd.read_parquet("finbra_consolidado.parquet")
    if excluir_2025:
        df = df[df["ano"] != 2025]
    return df


def calcular_tabela_execucao(df):
    """Calcula Empenhado, Pago e a Taxa de Execução por
    Instituição/UF/ano/função, já com a população anexada."""
    df_funcao = df[df["tipo_conta"] == "função"]

    tabela = df_funcao.pivot_table(
        index=["Instituição", "UF", "ano", "Conta"],
        columns="Coluna",
        values="Valor",
        aggfunc="sum"
    )
    tabela["taxa_execucao"] = (
        tabela["Despesas Pagas"] / tabela["Despesas Empenhadas"] * 100
    )
    tabela = tabela.reset_index()

    populacao = df[["Instituição", "ano", "População"]].drop_duplicates()
    tabela = tabela.merge(populacao, on=["Instituição", "ano"], how="left")
    tabela["pago_per_capita"] = tabela["Despesas Pagas"] / tabela["População"]

    return tabela


def calcular_total_por_ano(tabela_execucao):
    """Agrega a tabela de execução em total pago e per capita geral,
    somando todas as funções por Instituição/ano."""
    total = tabela_execucao.groupby(["Instituição", "UF", "ano"]).agg(
        total_pago=("Despesas Pagas", "sum"),
        populacao=("População", "first")
    ).reset_index()
    total["pago_per_capita_total"] = total["total_pago"] / total["populacao"]
    return total


def calcular_ranking_execucao(tabela_execucao):
    """Ranking de capitais pela taxa de execução média (maior para menor)."""
    return (
        tabela_execucao.groupby(["Instituição", "UF"])["taxa_execucao"]
        .mean()
        .reset_index()
        .rename(columns={"taxa_execucao": "taxa_execucao_media"})
        .sort_values("taxa_execucao_media", ascending=False)
    )


def calcular_ranking_per_capita(total_por_ano):
    """Ranking de capitais pelo per capita médio (maior para menor)."""
    return (
        total_por_ano.groupby(["Instituição", "UF"])["pago_per_capita_total"]
        .mean()
        .reset_index()
        .rename(columns={"pago_per_capita_total": "per_capita_medio"})
        .sort_values("per_capita_medio", ascending=False)
    )


def calcular_comparacao_maceio(total_por_ano):
    """Compara o per capita de Maceió com a média das demais capitais, por ano."""
    maceio = total_por_ano[total_por_ano["Instituição"].str.contains("Maceió")]
    outras = total_por_ano[~total_por_ano["Instituição"].str.contains("Maceió")]

    media_outras = outras.groupby("ano")["pago_per_capita_total"].mean().reset_index()
    media_outras = media_outras.rename(columns={"pago_per_capita_total": "media_outras_capitais"})

    comparacao = maceio[["ano", "pago_per_capita_total"]].merge(media_outras, on="ano")
    comparacao = comparacao.rename(columns={"pago_per_capita_total": "maceio_per_capita"})

    return comparacao.sort_values("ano")


def calcular_ranking_2025():
    """Calcula o ranking de per capita e taxa de execução apenas para
    2025, isolado dos demais anos já que só 11 das 26 capitais
    reportaram esse ano até o momento. Não deve ser comparado
    diretamente com médias multi-ano (2020-2024)."""

    df_2025 = carregar_base(excluir_2025=False)
    df_2025 = df_2025[df_2025["ano"] == 2025]

    tabela_2025 = calcular_tabela_execucao(df_2025)
    total_2025 = calcular_total_por_ano(tabela_2025)

    capitais_reportantes = sorted(total_2025["Instituição"].unique())

    ranking_execucao_2025 = calcular_ranking_execucao(tabela_2025)
    ranking_per_capita_2025 = calcular_ranking_per_capita(total_2025)

    return capitais_reportantes, ranking_execucao_2025, ranking_per_capita_2025