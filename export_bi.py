"""
Script responsável por exportar as tabelas de indicadores usadas no
storytelling final (Power BI): ranking de taxa de execução, ranking
de per capita, e evolução temporal (Maceió x demais capitais).
"""

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

# Exporta apenas as tabelas usadas no storytelling final, em Parquet
ranking_execucao.to_parquet("powerbi_ranking_execucao.parquet", index=False)
ranking_per_capita.to_parquet("powerbi_ranking_per_capita.parquet", index=False)
comparacao.to_parquet("powerbi_comparacao_maceio.parquet", index=False)
total_por_ano.to_parquet("powerbi_total_por_ano.parquet", index=False)

print("Arquivos Parquet exportados para uso no Power BI:")
print("  - powerbi_ranking_execucao.parquet")
print("  - powerbi_ranking_per_capita.parquet")
print("  - powerbi_comparacao_maceio.parquet")
print("  - powerbi_total_por_ano.parquet")