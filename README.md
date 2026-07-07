## 📊 Minha Solução

### Como rodar o projeto do zero

​```bash
# 1. Extrair os arquivos .zip por ano
python extrair_dados.py

# 2. Consolidar os CSVs em uma única base tratada (gera finbra_consolidado.parquet)
python consolidar_dados.py

# 3. Rodar a análise e ver os indicadores no terminal
python analise.py

# 4. Gerar os gráficos (matplotlib)
python graficos.py

# 5. Exportar as tabelas de indicadores para uso no Power BI
python exportar_powerbi.py
​```

**Bibliotecas necessárias:** `pandas`, `pyarrow` (para Parquet), `matplotlib`.

### Estrutura do repositório

| Arquivo | Responsabilidade |
|---|---|
| `extrair_dados.py` | Descompacta os `.zip` de `dados_compactos/` para `dados_extraidos/` |
| `consolidar_dados.py` | Lê os CSVs, trata o formato Siconfi e consolida em `finbra_consolidado.parquet` |
| `calculos.py` | Funções de cálculo dos indicadores (taxa de execução, per capita, rankings) — reutilizadas por `analise.py` e `graficos.py` |
| `analise.py` | Roda os cálculos e imprime os principais achados no terminal |
| `graficos.py` | Gera os gráficos em matplotlib (`.png`) |
| `exportar_powerbi.py` | Exporta as tabelas de indicadores em Parquet para importação no Power BI |

### Tratamento dos dados: decisões e dificuldades encontradas

**1. Corrupção de caracteres acentuados no arquivo de 2020**

Ao consolidar as bases, o ano de 2020 apresentava caracteres corrompidos (`�`) em nomes de instituições e contas. Investigação passo a passo:

- Comparei os bytes brutos **dentro do `.zip`** (antes de qualquer extração) com os bytes do arquivo já extraído, e descobri que o `.zip` original estava correto — a corrupção era introduzida **depois** da extração.
- Isolando a variável, extraí o mesmo `.zip` em duas pastas diferentes: uma dentro de `Documentos` (sincronizada pelo OneDrive) e outra fora dele. O problema só ocorria dentro da pasta sincronizada.
- **Conclusão:** o OneDrive estava reprocessando/corrompendo os arquivos extraídos. **Solução:** mover o projeto para uma pasta local fora do OneDrive (`C:\Projetos\...`), resolvendo o problema na raiz, sem necessidade de tratamento adicional no código.

**2. Ano de 2025 incompleto**

Confirmei via `df.groupby("ano")["Instituição"].nunique()` que 2025 tem apenas 11 das 26 capitais reportadas (contra 26 em todos os outros anos). Por isso:

- Os rankings, médias e a evolução temporal usam apenas **2020-2024** (anos completos), evitando comparações injustas entre capitais com quantidades diferentes de anos disponíveis.
- Um indicador complementar (`calcular_ranking_2025`) isola e analisa apenas as 11 capitais que já reportaram em 2025, entre si, deixando claro que é um recorte parcial.

**3. Classificação função vs. subfunção vs. outros**

A coluna `Conta` foi classificada com base no padrão de formatação (2 dígitos + espaço = função; 2 dígitos + ponto = subfunção; qualquer outro padrão = totais/agregados como "Despesas Exceto Intraorçamentárias" ou "FUxx - Demais Subfunções"), evitando dupla contagem nas análises.

### Principais achados

**Taxa de Execução (Empenhado → Pago), 2020-2024:**
- Maior execução média: Recife (PE), Belém (PA), Manaus (AM) — todas acima de 95%
- Menor execução média: Porto Velho (RO), Macapá (AP), São Luís (MA) — entre 80% e 83%

**Gasto Per Capita médio, 2020-2024:**
- Maior: São Paulo (R$ 6.276), Vitória (R$ 5.931), Belo Horizonte (R$ 5.503)
- Menor: Macapá (R$ 2.693), Belém (R$ 2.880), Maceió (R$ 3.293)

**Maceió em perspectiva:**
- Maceió está entre as capitais com **menor gasto per capita** do país (3º menor), mas **não** aparece nos extremos de taxa de execução — ou seja, o que é planejado para gastar é executado dentro da normalidade.
- Ao longo de 2020-2024, o per capita de Maceió cresceu na mesma tendência da média das outras capitais, mas manteve-se consistentemente abaixo dela em todos os anos analisados — uma diferença de aproximadamente R$ 900 a R$ 1.800 por habitante, a depender do ano.
- O per capita de Maceió cresceu **109%** entre 2020 e 2024 — acompanhando a aceleração observada nas demais capitais no mesmo período.
- **Leitura sugerida:** o desafio orçamentário de Maceió parece estar mais relacionado à disponibilidade de recursos por habitante (arrecadação/receita) do que à gestão da execução do gasto em si, que se mostra tecnicamente saudável.

### Visualização

Os gráficos gerados em Python (`grafico_taxa_execucao.png`, `grafico_per_capita.png`, `grafico_evolucao_maceio.png`) estão disponíveis na raiz do repositório. Um dashboard interativo complementar foi montado em Power BI, a partir das tabelas exportadas por `exportar_powerbi.py`.