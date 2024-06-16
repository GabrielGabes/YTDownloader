from pytube import YouTube, Playlist

import time
from tqdm import tqdm

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    progress = int((bytes_downloaded / total_size) * 100)
    bar.update(progress - bar.n)

def atributos_video(stream):
    print("Atributos do Stream:".center(50, '*'))
    print(f"Resolução: {stream.resolution}")
    print(f"Codec de Áudio: {stream.audio_codec}")
    print(f"Tipo de Stream: {stream.type}")
    print(f"Taxa de Bits de Áudio: {stream.abr}")
    print(f"Tamanho: {str(round(stream.filesize / 1024 / 1024, 2))} MB")  # filesize returns bytes
    print('*' * 50)

def download(video, formato_video_audio, caminho_salvar_arquivo, bar):
    if formato_video_audio:
        stream = video.streams.filter(file_extension='mp4', progressive=True)[-1]
    else:
        stream = video.streams.filter(file_extension='mp4', only_audio=True)[-1]

    max_tentativas = 5
    tentativa_atual = 0
    while tentativa_atual < max_tentativas:
        try:
            stream.download(output_path=caminho_salvar_arquivo)
            atributos_video(stream)
            break
        except Exception as e:
            tentativa_atual += 1
            print(f"Falha no download: {e}. Tentativa {tentativa_atual} de {max_tentativas}.")
            time.sleep(5)

def download_only(video_url, formato_video_audio, caminho_salvar_arquivo):
    video = YouTube(video_url)
    print(video.title)
    bar = tqdm(total=100, desc='Loading', unit='%', leave=True)
    video.register_on_progress_callback(progress_function)
    download(video, formato_video_audio, caminho_salvar_arquivo, bar)
    bar.close()

def download_playlist(playlist_url, formato_video_audio, caminho_salvar_arquivo):
    playlist = Playlist(playlist_url)
    print(playlist.title)
    print('Quantidade:', len(playlist.videos))
    for video in playlist.videos:
        print(video.title)
        bar = tqdm(total=100, desc='Loading', unit='%', leave=True)
        video.register_on_progress_callback(progress_function)
        download(video, formato_video_audio, caminho_salvar_arquivo, bar)
        bar.close()

def verificar_tipo_url(url):
    if 'playlist?list=' in url or 'list=' in url:
        return "Playlist"
    elif 'watch?v=' in url or 'youtu.be' in url:
        return "Video_Unico"
    else:
        return "URL não reconhecida"

def main():
    video_url = input('Cole a URL e pressione Enter: ')
    escolha = input('Download mp3 ou mp4?: ').lower()
    formato_video_audio = True if escolha == 'mp4' else False if escolha == 'mp3' else None
    if formato_video_audio is None:
        print('Formato Inválido. Aceito apenas "mp3" ou "mp4".')
        return

    caminho_salvar_arquivo = input('Onde gostaria que fosse colocado o download?: ').replace('\\', '/')

    tipo_url = verificar_tipo_url(video_url)
    if tipo_url == "Video_Unico":
        download_only(video_url, formato_video_audio, caminho_salvar_arquivo)
    elif tipo_url == "Playlist":
        download_playlist(video_url, formato_video_audio, caminho_salvar_arquivo)
    else:
        print("URL não reconhecida.")

    print('Download(s) Concluído(s)')
    input("Pressione Enter para encerrar...")

if __name__ == "__main__":
    main()
