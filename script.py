import requests
import time
import json

client_id = ''
client_secret = ''
limite = 500
tempo_req = 0.8 #tempo de time.sleep() a cada requisição

dados = {
    'grant_type':'client_credentials',
    'client_id':client_id,
    'client_secret':client_secret
}

def get_token(dados):
  resp = requests.post('https://accounts.spotify.com/api/token',headers={'Content-Type':'application/x-www-form-urlencoded'}, data=dados)
  return resp.json()

token = get_token(dados)
print(token)
print()

def get_albums(id_artista, token):
  r = []
  url = 'https://api.spotify.com/v1/artists/'+id_artista+'/albums?limit=50'
  auth = token['token_type']+' '+token['access_token']
  resp = requests.get(url, headers={'Authorization': auth})
  time.sleep(tempo_req)
  if 'retry-after' in resp.headers:
    print('Muitas requisições. Time sleep de ', resp.headers['retry-after'], 'segundos')
    return None, None
  # Se o token expirar, atualiza ele
  resposta = resp.json()
  if 'error' in resposta:
     if resposta['error']['status'] == 401:
      token = get_token(dados)
      return get_albums(id_artista, token)
  r.append(resposta)
  if resposta['next'] != None:
    prox = resposta['next']
    while prox:
      url = prox
      auth = token['token_type']+' '+token['access_token']
      resp = requests.get(url, headers={'Authorization': auth})
      time.sleep(tempo_req)
      if 'retry-after' in resp.headers:
        print('Muitas requisições. Time sleep de ', resp.headers['retry-after'])
        return None, None
      else:
        resp = resp.json()
        if 'next' not in resp:
          return None, None
        r.append(resp)
        prox = resp['next']
  return r, token


def get_artistas_album(pai, albuns):
  artistas_relacionados = []
  for album in albuns:
    for b in album['items']:
      artistas = b['artists']
      for a in artistas:
        if(a['id'] != pai):
          artistas_relacionados.append((a['name'], a['id']))
  return artistas_relacionados

def retorna_valores(tupla):
  unique = []
  dict_artistas = {}
  ids = []
  for t in tupla:
    if t[1] not in dict_artistas:
      dict_artistas[t[1]] = t[0]
      ids.append(t[1])
  return dict_artistas, ids

grafo = json.load(open("grafo.txt"))
artistas_dict = json.load(open("dict.txt"))

print('Total de artistas já coletados:', len(grafo))
print('Total de artistas já adicionados no dicionário:', len(artistas_dict))
print()

visitados = []
flag = False
count = 0
add = {}
for pai in grafo:
  if pai not in visitados:
    visitados.append(pai)
    for filho in grafo[pai]:
      if filho not in grafo:
        albums, token = get_albums(filho, token)
        if(albums == None and token == None):
          flag = True
          break
        try:
          nomes, resps = retorna_valores(get_artistas_album(filho,albums))
        except Exception as e:
          # atualiza o grafo com valores coletados até então antes do erro
          print('Erro capturado, encerrando loop...')
          #print(e)
          artistas_dict.update(nomes)
          flag = True
          break
        add[filho] = resps
        print(count,filho, len(resps))
        artistas_dict.update(nomes)
        count = count+1
        if count>limite:
          print()
          print(count,' artistas coletados')
          flag = True
          break
    if flag:
      break
grafo.update(add)

with open('new_dict.txt', 'w') as file:
     file.write(json.dumps(artistas_dict))
with open('new_grafo.txt', 'w') as file:
     file.write(json.dumps(grafo))

print('Total atualizado de artistas coletados:', len(grafo))
print('Total atualizado de artistas no dicionário:', len(artistas_dict))