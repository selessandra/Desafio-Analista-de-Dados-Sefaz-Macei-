"""
Script responsável por gerar visualizações gráficas dos indicadores
calculados em calculos.py: ranking de taxa de execução, ranking de
per capita, e evolução temporal (Maceió x demais capitais).
Os gráficos usam apenas 2020-2024 (anos completos); 2025 é tratado
separadamente por estar parcial.
"""

import matplotlib.pyplot as plt
from calculos import (
    carregar_base,
    calcular_tabela_execucao,
    calcular_total_por_ano,
    calcular_ranking_execucao,
    calcular_ranking_per_capita,
    calcular_comparacao_maceio,
)

df = carregar_base()
tabela_execucao = calcular_tabela_execucao(df)
total_por_ano = calcular_total_por_ano(tabela_execucao)
ranking_execucao = calcular_ranking_execucao(tabela_execucao)
ranking_per_capita = calcular_ranking_per_capita(total_por_ano)
comparacao = calcular_comparacao_maceio(total_por_ano)

# --- Gráfico 1: Ranking de taxa de execução ---
plt.figure(figsize=(10, 8))
plt.barh(ranking_execucao["UF"], ranking_execucao["taxa_execucao_media"], color="steelblue")
plt.xlabel("Taxa de execução média (%)")
plt.title("Taxa de Execução Média por Capital (2020-2024)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("grafico_taxa_execucao.png")
plt.close()
print("Gráfico salvo: grafico_taxa_execucao.png")

# --- Gráfico 2: Ranking de per capita ---
plt.figure(figsize=(10, 8))
plt.barh(ranking_per_capita["UF"], ranking_per_capita["per_capita_medio"], color="darkorange")
plt.xlabel("Gasto per capita médio (R$)")
plt.title("Gasto Per Capita Médio por Capital (2020-2024)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("grafico_per_capita.png")
plt.close()
print("Gráfico salvo: grafico_per_capita.png")

# --- Gráfico 3: Evolução temporal - Maceió x média das outras capitais ---
plt.figure(figsize=(10, 6))
plt.plot(comparacao["ano"], comparacao["maceio_per_capita"], marker="o", label="Maceió")
plt.plot(comparacao["ano"], comparacao["media_outras_capitais"], marker="o", label="Média das outras capitais")
plt.xlabel("Ano")
plt.ylabel("Gasto per capita (R$)")
plt.title("Evolução do Gasto Per Capita: Maceió x Média das Capitais (2020-2024)")
plt.legend()
plt.tight_layout()
plt.savefig("grafico_evolucao_maceio.png")
plt.close()
print("Gráfico salvo: grafico_evolucao_maceio.png")