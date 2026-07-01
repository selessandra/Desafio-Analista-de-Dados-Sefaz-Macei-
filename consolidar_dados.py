"""
Script responsável por ler os arquivos finbra.csv extraídos em
'dados_extraidos/' (um por ano) e consolidá-los em um único
DataFrame, tratando as particularidades do formato Siconfi:
encoding Latin-1, separador ';', decimal ',' e 3 linhas de metadados
no início de cada arquivo.

OBS: o arquivo de 2020 apresenta corrupção de caracteres acentuados
(aparecem como '�') já na fonte, tanto no cabeçalho quanto em alguns
valores de texto (ex.: nomes de subfunção). Por isso, os nomes das
colunas são fixados manualmente abaixo, em vez de lidos do cabeçalho,
já que a ordem das colunas é constante em todos os anos (ver README).
"""

import pandas as pd
from pathlib import Path

# Pasta de origem: contém uma subpasta por ano, cada uma com o finbra.csv
pasta_extraidos = Path('dados_extraidos')

# Nomes fixos das colunas, na ordem em que aparecem no CSV (ver README)
colunas_finbra = [
    'Instituição', 'Cod.IBGE', 'UF', 'População',
    'Coluna', 'Conta', 'Identificador da Conta', 'Valor'
]

# Lista que vai guardar o DataFrame de cada ano, antes de juntar tudo
lista_dataframes = []

# Percorre as pastas de ano em ordem (2020, 2021, 2022, ...)
for pasta_ano in sorted(pasta_extraidos.iterdir()):

    # Ignora qualquer item que não seja uma pasta
    if not pasta_ano.is_dir():
        continue

    ano = pasta_ano.name  # nome da pasta = ano dos dados (ex.: "2020")

    # Busca o arquivo .csv dentro da pasta do ano
    for csv_path in pasta_ano.glob('*.csv'):

        # Lê o CSV tratando o padrão brasileiro do Siconfi
        df_ano = pd.read_csv(
            csv_path,
            sep=';',                # separador de colunas é ponto e vírgula
            skiprows=4,              # pula 3 linhas de metadados + 1 de cabeçalho
            header=None,             # cabeçalho não é confiável (ver OBS acima)
            names=colunas_finbra,    # usamos nomes fixos no lugar
            encoding='latin-1',      # ISO-8859-1, evita quebrar acentuação
            decimal=',',             # vírgula é o separador decimal
            thousands='.',           # ponto é o separador de milhar
        )

        # Adiciona a coluna 'ano', já que o CSV não traz essa informação
        df_ano['ano'] = int(ano)

        lista_dataframes.append(df_ano)

# Junta todos os DataFrames de ano em um único DataFrame consolidado
df = pd.concat(lista_dataframes, ignore_index=True)


def classificar_conta(texto):
    """Classifica cada valor da coluna 'Conta' como função, subfunção ou outro,
    com base no padrão de formatação descrito no README (ver dicionário de colunas)."""
    if texto[:2].isdigit() and texto[2] == '.':
        return 'subfunção'
    elif texto[:2].isdigit() and texto[2] == ' ':
        return 'função'
    else:
        return 'outro'


# Cria a coluna 'tipo_conta', classificando cada linha da coluna 'Conta'
df['tipo_conta'] = df['Conta'].apply(classificar_conta)

# Confere o resultado da consolidação
print(f'Total de linhas consolidadas: {len(df)}')
print(f'Anos presentes na base: {sorted(df["ano"].unique())}')
print(f'Colunas: {list(df.columns)}')
print(f'Tipo da coluna Valor: {df["Valor"].dtype}')
print(f'Distribuição de tipo_conta:\n{df["tipo_conta"].value_counts()}')
print(df.head())

# Exporta a base consolidada dos dados para o formato parquet
df.to_parquet('finbra_consolidado.parquet', index=False)

print('Arquivo Parquet salvo com sucesso: finbra_consolidado.parquet')