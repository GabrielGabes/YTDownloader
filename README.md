# YTDownloader

YTDownloader é um projeto desenvolvido para facilitar o download de vídeos e músicas do YouTube sem anúncios e com maior rapidez. Este projeto foi criado com o objetivo de treinar meus conhecimentos adquiridos em Programação Orientada a Objetos (POO) e na criação de interfaces gráficas usando Tkinter (para PC) e Kivy (para Android).

## Índice

- [Descrição](#descrição)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
  - [YTDownloader.ipynb](#ytdownloaderipynb)
  - [YTDownloader.py](#ytdownloaderpy)
  - [YTDownloader_APP.py](#ytdownloader_apppy)
  - [YTDownloader_APK.py](#ytdownloader_apkpy)
- [Instalação](#instalação)
- [Uso](#uso)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Descrição

O YTDownloader foi desenvolvido para resolver a necessidade de um programa eficiente para download de vídeos e músicas do YouTube, sem anúncios e com maior rapidez. Este projeto também serve como prática de POO e desenvolvimento de interfaces gráficas.

## Funcionalidades

- Download rápido e sem anúncios de vídeos e músicas do YouTube.
- Suporte para download de vídeos únicos ou playlists inteiras.
- Interface gráfica amigável para usuários de PC e Android.

## Estrutura do Projeto

### YTDownloader.ipynb

Um Jupyter Notebook onde foram exploradas todas as funções do pacote `pytube`, que é uma API para downloads de mídias do YouTube, necessárias para o projeto.

### YTDownloader.py

Este arquivo organiza o pipeline do projeto e inclui funções como:

- `progress_function`: exibe uma barra de carregamento.
- `atributos_video`: exibe os atributos da mídia.
- `download`: realiza o download da mídia única ou das mídias de uma playlist.

Este arquivo está pronto para ser convertido em um arquivo `.exe`, mas ainda não possui interface gráfica.

### YTDownloader_APP.py

Contém todo o código com interface gráfica usando o pacote `Tkinter`, pronto para ser convertido em um arquivo `.exe`.

### YTDownloader_APK.py

Contém todo o código com interface gráfica usando o pacote `Kivy`, pronto para ser convertido em um arquivo `.apk` para uso em smartphones Android.

## Instalação

1. Clone o repositório:
   ```sh
   git clone https://github.com/GabrielGabes/YTDownloader.git
