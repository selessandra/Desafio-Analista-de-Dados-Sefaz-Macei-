"""
Script de análise da base consolidada de despesas das capitais
(FINBRA/Siconfi). Usa as funções de calculos.py para gerar os
indicadores e imprime os resultados para investigação.
"""

from calculos import (
    carregar_base,
    calcular_tabela_execucao,
    calcular_total_por_ano,
    calcular_ranking_execucao,
    calcular_ranking_per_capita,
    calcular_comparacao_maceio,
    calcular_ranking_2025,
)

# --- Indicadores 2020-2024 (anos completos, 26 capitais) ---
df = carregar_base()
tabela_execucao = calcular_tabela_execucao(df)
total_por_ano = calcular_total_por_ano(tabela_execucao)
ranking_execucao = calcular_ranking_execucao(tabela_execucao)
ranking_per_capita = calcular_ranking_per_capita(total_por_ano)
comparacao = calcular_comparacao_maceio(total_por_ano)

print("Top 5 - Maior taxa de execução média (2020-2024):")
print(ranking_execucao.head(5))

print("\nTop 5 - Menor taxa de execução média (2020-2024):")
print(ranking_execucao.tail(5))

print("\nTop 5 - Maior per capita médio (2020-2024):")
print(ranking_per_capita.head(5))

print("\nTop 5 - Menor per capita médio (2020-2024):")
print(ranking_per_capita.tail(5))

print("\nMaceió x média das outras capitais, por ano:")
print(comparacao)

# --- Indicador extra: recorte isolado de 2025 (parcial, 11 capitais) ---
capitais_2025, ranking_execucao_2025, ranking_per_capita_2025 = calcular_ranking_2025()

print(f"\n\nCapitais que já reportaram em 2025 ({len(capitais_2025)} de 26):")
for capital in capitais_2025:
    print(f"  - {capital}")

print("\nRanking de taxa de execução - somente 2025 (parcial):")
print(ranking_execucao_2025)

print("\nRanking de per capita - somente 2025 (parcial):")
print(ranking_per_capita_2025)