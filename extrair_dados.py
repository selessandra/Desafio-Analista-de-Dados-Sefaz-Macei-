"""
Script responsável por extrair os arquivos .zip de despesas das capitais
(FINBRA/Siconfi) organizados por ano dentro de 'dados_compactos/',
gerando a estrutura equivalente em 'dados_extraidos/'.
"""

import zipfile
from pathlib import Path

# Pasta de origem: contém uma subpasta por ano, cada uma com um arquivo .zip
pasta_compactados = Path('dados_compactos')

# Pasta de destino: onde os arquivos extraídos (CSVs) serão salvos
pasta_extraidos = Path('dados_extraidos')
pasta_extraidos.mkdir(exist_ok=True)

# Percorre as pastas de ano em ordem (2020, 2021, 2022, ...)
for pasta_ano in sorted(pasta_compactados.iterdir()):

    # Ignora qualquer item que não seja uma pasta (ex.: arquivos soltos)
    if not pasta_ano.is_dir():
        continue

    ano = pasta_ano.name  # nome da pasta = ano dos dados (ex.: "2020")

    # Busca o(s) arquivo(s) .zip dentro da pasta do ano
    for zip_path in pasta_ano.glob('*.zip'):

        # Cria a subpasta de destino correspondente ao ano
        destino = pasta_extraidos / ano
        destino.mkdir(exist_ok=True)

        # Abre e extrai o conteúdo do .zip para a pasta de destino
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(destino)

        print(f'Extração concluída com sucesso: {zip_path.name} -> {destino}')