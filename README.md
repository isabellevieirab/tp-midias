<h1> Análise e Mineração de Mídias Sociais - Mineração do Spotify </h1>

* Isabelle Vieira Barbosa
* Paulo Henrique Maciel Fraga

Este trabalho consiste na coleta de dados provenientes do Spotify. Nosso objetivo principal é mapear uma rede de colaborações de artistas, com base em suas colaborações em álbuns, singles ou compilações disponíveis na plataforma. Além disso, também coletamos dados como os gêneros musicais, quantidade de seguidores e popularidade de cada artista mapeado.

O Spotify é o serviço de streaming de música mais popular e usado do mundo, e oferece uma vasta biblioteca de músicas, álbuns e playlists de diversos gêneros musicais. Com o objetivo de visualizar as conexões entre diferentes artistas com base em suas colaborações disponibilizadas na plataforma, mapeamos uma rede através da coleta de dados provenientes da própria API do serviço.

Para a realizar a coleta de dados, utilizamos o Spotify Web https://developer.spotify.com/documentation/web-api. Como ponto inicial de partida, escolhemos a cantora Doja Cat, que até então estava no top 1 do Spotify Global com o seu single "Paint The Town Red".

A partir dela, através da API da plataforma foi possível coletar os artistas participantes de cada álbum da cantora (levando em conta que um álbum na plataforma pode ser do tipo "album", "single" ou "compilation"). Através dos artistas retornados foi possível então desenvolver um algoritmo semelhante ao BFS, que a partir do nó inicial (a artista Doja Cat) explora todos os vizinhos desse nó (artistas com colaborações) antes de avançar para os vizinhos dos vizinhos. As principais chamadas, limitações dos dados e códigos utilizados serão apresentados a seguir.
<h2> Coleta de Dados </h2>
Para executar os coletores, é necessário ter no mesmo diretório um arquivo "credenciais.txt", no seguinte formato:

```python
{
"Conta1":[client_id1,client_secret1],
"Conta2":[client_id2,client_secret2]
}
```
O arquivo pode conter uma ou mais contas e suas respectivas credenciais, que serão utilizadas na coleta.

Os arquivos "dict.txt" e "grafo.txt" presentes nesse repositório já estão absoletos devido ao tamanho atingido, mas podem ser utilizados de exemplo.

<h2> Dados Coletados </h2>
Os resultados das Coletas podem ser encontrados nos arquivos:

* "dict.txt" (dicionário que vincula os IDs dos artistas aos seus respectivos nomes)
* "grafo.txt" (que contém a rede de colaboração dos artistas)
* "artists_dumps.txt" (que contém outras features de cada artista)
  
disponíveis no seguinte link: https://drive.google.com/drive/u/0/folders/1cA67U8uKmxxNpP7UwFBbeSBBzOoI50eX. 
