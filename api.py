import requests
import json
import time

credenciais = json.load(open("credenciais.txt"))
contas = [key for key in credenciais.keys()]
print(contas)
rate_flag = True
for c_i, c in enumerate(credenciais):
  print('Coleta login ',contas[c_i])
  rate_flag = True
  while(rate_flag):
    dados = {
        'grant_type':'client_credentials',
        'client_id':credenciais[c][0],
        'client_secret':credenciais[c][1]
    }

    def get_token(dados):
      resp = requests.post('https://accounts.spotify.com/api/token',headers={'Content-Type':'application/x-www-form-urlencoded'}, data=dados)
      return resp.json()

    token = get_token(dados)

    def get_artist(id_artista, token):
      r = []
      url = 'https://api.spotify.com/v1/artists/'+id_artista
      auth = token['token_type']+' '+token['access_token']
      resp = requests.get(url, headers={'Authorization': auth})
      if 'retry-after' in resp.headers:
        print('Muitas requisições. Time sleep de ', resp.headers['retry-after'])
        return None, None, None
      resposta = resp.json()
      if 'error' in resposta:
        if resposta['error']['status'] == 401:
          token = get_token(dados)
          return get_artist(id_artista, token)

      out = {'id_artista' : id_artista,
        'followers': resposta['followers']['total'],
        'genres' : resposta['genres'],
        'popularity' : resposta['popularity']}

      return r, token, out 


    print()

    ids_artistas = json.load(open("grafo.txt"))
    print("Total: ", len(ids_artistas.keys()))

    save = 500
    tempo_req = 1
    lista = list(ids_artistas.keys())

    with open('artists_dumps.txt', 'r') as file:
      file_contents = file.read()
  
    control = 0
    count = 0 
    dumps = []
    for id_artista in lista:
      control = control + 1
      if id_artista not in file_contents:
        r, token, out = get_artist(id_artista, token)
        if r == None and token == None and out == None:
          rate_flag = False
          flag = True
          break
        dumps.append(out)
        time.sleep(tempo_req)
        count = count + 1

      if count == save:
        count = 0
        print(control,"/",len(lista))
        print("Coletados ", save," salvando. Ultimo ID COLETADO: ",id_artista )
        with open('artists_dumps.txt', 'a') as file:
            file.write(json.dumps(dumps))