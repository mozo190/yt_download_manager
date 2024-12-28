import re

from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivymd.uix.relativelayout import MDRelativeLayout
from pytube import YouTube

Window.size = (500, 600)


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.link = ""
        self.title = ""
        self.views = ""
        self.length = ""
        self.downloadButtonAdded = False

    def is_valid_youtube_link(self, link):
        pattern = r"(?:www\.)?youtube\.com/watch\?v=[0-9A-Za-z_-]{11}"
        return re.search(pattern, link) is not None

    def getLinkInfo(self, instance):
        try:
            self.link = self.linkinput.text

            if not self.is_valid_youtube_link(self.link):
                self.titleLabel.text = "Invalid Youtube Link"
                self.viewLabel.text = "Please enter a valid Youtube Link."
                self.lengthLabel.text = ""
                return

            self.yt = YouTube(self.link, use_oauth=True, allow_oauth_cache=True)
            self.title = str(self.yt.title) if hasattr(self.yt, 'title') else "No Title"
            self.views = str(self.yt.views) if hasattr(self.yt, 'views') else "No Views"
            self.length = str(self.yt.length) if hasattr(self.yt, 'length') else "No Length"

            self.titleLabel.text = f"Title: {self.title}"
            self.viewLabel.text = f"Views: {self.views}"
            self.lengthLabel.text = f"Length: {self.length} seconds"

            if not hasattr(self, 'downloadButtonAdded'):
                self.downloadButton = Button(text="Download", pos_hint={'center_x': 0.5, 'center_y': 0.20},
                                             size_hint=(.2, .1), background_color=(0, 1, 0, 1), color=(1, 1, 1, 1),
                                             font_size=20)
                self.downloadButton.bind(on_press=self.downloadVideo)
                self.layout.add_widget(self.downloadButton)
                self.downloadButtonAdded = True

            self.downloadButton.text = "Download"
            self.downloadButton.pos_hint = {'center_x': 0.5, 'center_y': 0.20}
            self.downloadButton.size_hint = (.2, .1)

            self.video = self.yt.streams.filter(file_extension='mp4').order_by('resolution').desc().first()
            # self.video.download("Downloads")

            self.dropDown = DropDown()
            for video in self.video:
                btn = Button(text=video.resolution, size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn: self.dropDown.select(btn.text))

                self.dropDown.add_widget(btn)

            print(f"Title: {self.title}")
            print(f"Views: {self.views}")
            print(f"Length: {self.length}")
        except Exception as e:
            print(f"Error occurred: {e}")
            self.titleLabel.text = "Error: Could not retrieve video details."
            self.viewLabel.text = "Please check the link and try again."
            self.lengthLabel.text = ""

    def downloadVideo(self, event):
        try:
            self.ys = self.yt.streams.get_highest_resolution()
            print("Downloading Video...")

            self.ys.download("Downloads")

            print("Video Downloaded Successfully")
        except Exception as e:
            print(f"Error occurred during download: {e}")

    def build(self):
        self.layout = MDRelativeLayout(md_bg_color=(248 / 255, 200 / 255, 220 / 255, 1))

        self.img = Image(source="assets/img/logo.png", size_hint=(.5, .5),
                         pos_hint={"center_x": 0.5, "center_y": 0.90})
        self.youtubelink = Label(text="Please Enter the Youtube link to Download", size_hint=(.5, .5),
                                 pos_hint={"center_x": 0.5, "center_y": 0.75},
                                 color=(1, 0, 0, 1), font_size=20)
        self.linkinput = TextInput(hint_text="Enter the Youtube Link", size_hint=(.90, None),
                                   pos_hint={"center_x": 0.5, "center_y": 0.60}, height=50, font_size=20,
                                   foreground_color=(0, 0.5, 0, 1), font_name="Comic")

        self.linkbutton = Button(text="Get Video", pos_hint={'center_x': 0.5, 'center_y': 0.50}, size_hint=(.2, .1),
                                 background_color=(0, 1, 0, 1), color=(1, 1, 1, 1), font_size=20)
        self.linkbutton.bind(on_press=self.getLinkInfo)

        self.titleLabel = Label(text="Title: ", size_hint=(.5, .5),
                                pos_hint={"center_x": 0.5, "center_y": .40},
                                color=(1, 0, 0, 1), font_size=20)

        self.viewLabel = Label(text="View: ", size_hint=(.5, .5),
                               pos_hint={"center_x": 0.5, "center_y": .35},
                               color=(1, 0, 0, 1), font_size=20)

        self.lengthLabel = Label(text="Length: ", size_hint=(.5, .5),
                                 pos_hint={"center_x": 0.5, "center_y": .30},
                                 color=(1, 0, 0, 1), font_size=20)

        self.layout.add_widget(self.img)
        self.layout.add_widget(self.youtubelink)
        self.layout.add_widget(self.linkinput)
        self.layout.add_widget(self.linkbutton)
        self.layout.add_widget(self.titleLabel)
        self.layout.add_widget(self.viewLabel)
        self.layout.add_widget(self.lengthLabel)

        return self.layout


if __name__ == "__main__":
    MainApp().run()
