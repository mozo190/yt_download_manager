from functools import partial

from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivymd.uix.relativelayout import MDRelativeLayout
from pytube import YouTube

Window.size = (500, 600)


class MainApp(MDApp):

    def getLinkInfo(self, instance):
        try:
            self.link = self.linkinput.text
            self.yt = YouTube(self.link, use_oauth=True, allow_oauth_cache=True)
            self.title = str(self.yt.title) if hasattr(self.yt, 'title') else "No Title"
            self.views = str(self.yt.views) if hasattr(self.yt, 'views') else "No Views"
            self.length = str(self.yt.length) if hasattr(self.yt, 'length') else "No Length"

            self.titleLabel.text = f"Title: {self.title}"
            self.titleLabel.pos_hint = {"center_x": 0.5, "center_y": .40}

            self.viewLabel.text = f"Views: {self.views}"
            self.viewLabel.pos_hint = {"center_x": 0.5, "center_y": .35}

            self.lengthLabel.text = f"Length: {self.length} seconds"
            self.lengthLabel.pos_hint = {"center_x": 0.5, "center_y": .30}

            self.downloadButton.text = "Download"
            self.downloadButton.pos_hint = {'center_x': 0.5, 'center_y': 0.20}
            self.downloadButton.size_hint = (.2, .1)

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
        layout = MDRelativeLayout(md_bg_color=(248 / 255, 200 / 255, 220 / 255, 1))

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

        self.downloadButton = Button(text="Download", pos_hint={'center_x': 0.5, 'center_y': 0.20}, size_hint=(.2, .1),
                                     background_color=(0, 1, 0, 1), color=(1, 1, 1, 1), font_size=20)
        self.downloadButton.bind(on_press=self.downloadVideo)

        layout.add_widget(self.img)
        layout.add_widget(self.youtubelink)
        layout.add_widget(self.linkinput)
        layout.add_widget(self.linkbutton)
        layout.add_widget(self.titleLabel)
        layout.add_widget(self.viewLabel)
        layout.add_widget(self.lengthLabel)
        layout.add_widget(self.downloadButton)

        return layout


if __name__ == "__main__":
    MainApp().run()
