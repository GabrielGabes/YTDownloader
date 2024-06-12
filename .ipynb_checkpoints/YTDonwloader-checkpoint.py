from pytube import YouTube, Playlist

import tkinter as tk
from threading import Thread
from tkinter import messagebox, scrolledtext
import os

def download_video():
    url = url_entry.get()
    formato = formato_var.get()
    # Remove a entrada do caminho, pois agora é fixo
    path = os.path.join(os.path.expanduser("~"), "Downloads", "youtube_saves")
    
    if not url:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos")
        return
    if not formato:
        messagebox.showerror("Erro", "Selecione o formato do arquivo")
        return

    output.insert(tk.END, "Iniciando o download...\n")
    output.see(tk.END)

    # Cria a pasta se não existir
    if not os.path.exists(path):
        os.makedirs(path)
    
    formato_video_audio = formato == 'MP4'
    thread = Thread(target=lambda: iniciar_download(url, formato_video_audio, path))
    thread.start()

def iniciar_download(url, formato_video_audio, path):
    try:
        tipo_url = verificar_tipo_url(url)
        if tipo_url == "Video_Unico":
            video = YouTube(url)
            video.register_on_progress_callback(lambda stream, chunk, bytes_remaining: progress_update(stream, bytes_remaining))
            stream = video.streams.filter(file_extension='mp4', progressive=True)[-1] if formato_video_audio else video.streams.filter(file_extension='mp4', only_audio=True)[-1]
            stream.download(output_path=path)
        elif tipo_url == "Playlist":
            playlist = Playlist(url)
            for video in playlist.videos:
                video.register_on_progress_callback(lambda stream, chunk, bytes_remaining: progress_update(stream, bytes_remaining))
                stream = video.streams.filter(file_extension='mp4', progressive=True)[-1] if formato_video_audio else video.streams.filter(file_extension='mp4', only_audio=True)[-1]
                stream.download(output_path=path)
        output.insert(tk.END, "Download concluído com sucesso!\n")
    except Exception as e:
        output.insert(tk.END, f"Erro durante o download: {str(e)}\n")
    output.see(tk.END)

def progress_update(stream, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percent = int((bytes_downloaded / total_size) * 100)
    output.insert(tk.END, f"Download progress: {percent}%\n")
    output.see(tk.END)

def verificar_tipo_url(url):
    if 'playlist?list=' in url or 'list=' in url:
        return "Playlist"
    elif 'watch?v=' in url or 'youtu.be' in url:
        return "Video_Unico"
    else:
        return "URL não reconhecida"

root = tk.Tk()
root.title("YouTube Downloader")

# configurando largura e altura do programa e para abrir no meio exato da tela
#master.geometry("400x100")
width = 400 #1920
height = 300 #1080
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int((screen_width - width) / 2)
center_y = int((screen_height - height) / 2)
root.geometry(f'{width}x{height}+{center_x}+{center_y}')

# Entrada de URL
tk.Label(root, text="URL do Vídeo/Playlist:").pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# Entrada de formato
formato_var = tk.StringVar()
tk.Label(root, text="Formato do download:").pack()
tk.Radiobutton(root, text="MP4 (Vídeo)", variable=formato_var, value='MP4').pack()
tk.Radiobutton(root, text="MP3 (Áudio)", variable=formato_var, value='MP3').pack()

# Remove a entrada do caminho para salvar
# tk.Label(root, text="Caminho para salvar o arquivo:").pack()
# path_entry = tk.Entry(root, width=50)
# path_entry.pack()

# Botão de download
download_button = tk.Button(root, text="Download", command=download_video)
download_button.pack()

# Área de saída de logs
output = scrolledtext.ScrolledText(root, height=10)
output.pack()

root.mainloop()