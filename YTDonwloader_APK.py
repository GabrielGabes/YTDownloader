from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from pytube import YouTube, Playlist
from threading import Thread
import os

class YTDownloaderApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.url_label = Label(text="URL do Vídeo/Playlist:")
        self.url_entry = TextInput(multiline=False)

        self.formato_label = Label(text="Formato do download:")
        self.formato_mp4 = CheckBox(group='formato', active=True)
        self.formato_mp3 = CheckBox(group='formato')

        self.formato_label_mp4 = Label(text="MP4 (Vídeo)")
        self.formato_label_mp3 = Label(text="MP3 (Áudio)")

        self.download_button = Button(text="Download", on_press=self.download_video)

        self.output = Label(size_hint_y=None, text="Logs:\n")
        self.output.bind(texture_size=self.output.setter('size'))

        self.scrollview = ScrollView(size_hint=(1, None), size=(400, 300))
        self.scrollview.add_widget(self.output)

        self.layout.add_widget(self.url_label)
        self.layout.add_widget(self.url_entry)
        self.layout.add_widget(self.formato_label)
        
        self.formato_layout = BoxLayout(orientation='horizontal')
        self.formato_layout.add_widget(self.formato_mp4)
        self.formato_layout.add_widget(self.formato_label_mp4)
        self.formato_layout.add_widget(self.formato_mp3)
        self.formato_layout.add_widget(self.formato_label_mp3)
        self.layout.add_widget(self.formato_layout)

        self.layout.add_widget(self.download_button)
        self.layout.add_widget(self.scrollview)

        return self.layout

    def download_video(self, instance):
        url = self.url_entry.text
        formato = 'MP4' if self.formato_mp4.active else 'MP3'

        if not url:
            self.show_popup("Erro", "Por favor, preencha todos os campos")
            return

        self.output.text += "Iniciando o download...\n"
        formato_video_audio = formato == 'MP4'
        thread = Thread(target=self.iniciar_download, args=(url, formato_video_audio))
        thread.start()

    def iniciar_download(self, url, formato_video_audio):
        path = os.path.join(os.path.expanduser('~'), 'Download', 'youtube_saves')
        if not os.path.exists(path):
            os.makedirs(path)

        try:
            tipo_url = self.verificar_tipo_url(url)
            if tipo_url == "Video_Unico":
                video = YouTube(url)
                video.register_on_progress_callback(lambda stream, chunk, bytes_remaining: self.progress_update(stream, bytes_remaining))
                stream = video.streams.filter(file_extension='mp4', progressive=True).last() if formato_video_audio else video.streams.filter(file_extension='mp4', only_audio=True).last()
                stream.download(output_path=path)
            elif tipo_url == "Playlist":
                playlist = Playlist(url)
                for video in playlist.videos:
                    video.register_on_progress_callback(lambda stream, chunk, bytes_remaining: self.progress_update(stream, bytes_remaining))
                    stream = video.streams.filter(file_extension='mp4', progressive=True).last() if formato_video_audio else video.streams.filter(file_extension='mp4', only_audio=True).last()
                    stream.download(output_path=path)
            self.output.text += "Download concluído com sucesso!\n"
        except Exception as e:
            self.output.text += f"Erro durante o download: {str(e)}\n"

    def progress_update(self, stream, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percent = int((bytes_downloaded / total_size) * 100)
        self.output.text += f"Download progress: {percent}%\n"

    def verificar_tipo_url(self, url):
        if 'playlist?list=' in url or 'list=' in url:
            return "Playlist"
        elif 'watch?v=' in url or 'youtu.be' in url:
            return "Video_Unico"
        else:
            return "URL não reconhecida"

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text=message)
        close_button = Button(text="Fechar", size_hint=(1, 0.2))
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.4))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    YTDownloaderApp().run()
