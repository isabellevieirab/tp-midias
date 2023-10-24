import json

with open("artists_dumps.txt") as f:
    arquivo = f.read()

arquivo = arquivo.replace('][', '],[')
arquivo = '{"dados":['+arquivo+']}'
with open('artistas.txt', 'w') as file:
    file.write(arquivo)

dados = json.load(open("artistas.txt"))
print(len(dados['dados'][0]))

coleta = {}
for chunk in dados['dados']:
    for dado in chunk:
        coleta[dado['id_artista']] = {
                                        'followers':dado['followers'], 
                                        'genres':dado['genres'],
                                        'popularity':dado['popularity']
                                    }

print(len(coleta))
with open('info_artistas.txt', 'w') as file:
    file.write(json.dumps(coleta))