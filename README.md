# FFmpeg Online
## Autores
Augusto dos Santos Gomes Vaz - 800268
Gabrielly Castilho Guimarães - 805757

## Como rodar
1. Tenha o Docker e o Docker Compose instalados
2. Preencha o arquivo `variables.env` com as variáveis de ambiente corretas. 
3. Suba os serviços usando o compose
```sh
docker compose up
```
O docker vai gerar as imagens do frontend, do backend e baixar a do dabase

## Descrição da aplicação
A aplicação consiste de uma serviço web com ferramentas do software FFmpeg, um software usado para fazer
operações e edições em vídeos, como mudar o encode, cortar (duração), "cropar"(cortar como em fotos),
calcular índices de semelhança, etc.

Essa aplicação fornece uma maneira online, robusta e acessível para essa ferramenta.

## Bastidores a aplicação
### backend
O coração do serviço é o backend: ele recebe os vídeos passados pelo usuário, os guarda no banco de dados
e, quando o usuário decide fazer uma operação, ele recupera o vídeo e usa o programa do FFmpeg
para compactar, cortar, redimensionar, reencodar ou _cropar_ o vídeo.

A API é feira em FASTAPI, sendo rápida de implementar, mas ainda muito responsiva e com muitos recursos. O resto da aplicação
são wrappers para o FFmpeg, usando os recursos das bibliotecas de subprocess para chamar os binários do FFmpeg.

### Database
O banco de dados escolhido foi o MinIO, um banco de dados voltado a objetos (object storage) que permite o armazenamento de arquivos
grandes e sem estrutura definida criando _blobs_ e os armazenando em objetos e em _buckets_

### Frontend
O frontend foi feito usando HTML e Javascript puro, sendo bem versátil e mais minimalista. Para lançar um serviços com os arquivos
.html e .js para o cliente, foi usado um servidor nginx, que provisiona um servidor web com base nos arquivos indicados a ele.

## Containerização
Para cada um dos serviços foi usado uma abordagem ligeiramente diferente para containerizar.

No backend, foi produzida uma imagem do zero, saindo de uma imagem ubuntu, onde é compilado o FFmpeg e as bibliotecas necessárias, instalado o Python e copiados os arquivos do programa principal.
> Por compilar tudo, o build dessa imagem pode demorar bastante, em torno de 5-10 min em nossos testes

No frontend, foi usada uma imagem nginx como base e incorporado um shell script para permitir que o javascript rodando no cliente
pudesse receber variáveis de ambiente passadas na execução do docker.

No banco de dados, foi usada uma imagem oficial do minion, que pode ser usada "out of the box".

## Saiba mais
Saiba mais em nosso [arquivo detalhado](./pratica_devops.pdf)
