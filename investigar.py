import zipfile
from pathlib import Path

zip_path = list((Path('dados_compactos') / '2020').glob('*.zip'))[0]
destino_teste = Path('C:/teste_extracao')

with zipfile.ZipFile(zip_path, 'r') as z:
    z.extractall(destino_teste)

csv_teste = list(destino_teste.glob('*.csv'))[0]
with open(csv_teste, 'rb') as f:
    print(f.read(500))