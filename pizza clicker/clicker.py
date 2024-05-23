from kivy import Config
from kivy.app import App
from kivy.properties import NumericProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.graphics import Rectangle, Color

class game(App):

    count = NumericProperty(0)
    amount = NumericProperty(1)
    first_upgrade = NumericProperty(10)
    second_upgrade = NumericProperty(100)
    third_upgrade = NumericProperty(1000)
    fourth_upgrade = NumericProperty(2000)

    def __init__(self, **kwargs):
        super(game, self).__init__(**kwargs)
        self.called = bool(False)
        # Завантаження звуку для кнопки
        self.sound = SoundLoader.load('sfx_taunt.mp3')
        if not self.sound:
            print("Sound loading failed!")
        else:
            print("Sound loaded successfully.")
            self.sound.volume = 0.2  # Встановлюємо гучність на 20%

        # Завантаження фонової музики
        self.background_music = SoundLoader.load('Dungeon Freakshow (WIP V1).mp3')
        if not self.background_music:
            print("Background music loading failed!")
        else:
            print("Background music loaded successfully.")

    def build(self):
        # window configs
        Config.set('graphics', 'fullscreen', 'borderless')
        Config.write()

        # Відтворення фонової музики у циклі
        if self.background_music:
            self.background_music.loop = True
            self.background_music.play()

        # window
        self.window = GridLayout()
        self.window.cols = 2
        self.window.size_hint = (1, 1)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.icon = "images/icon.png"

        # Додавання фону
        with self.window.canvas.before:
            self.bg_color = Color(0.3, 0.3, 0.3, 1)  # Темний сірий колір
            self.bg_rect = Rectangle(source='dungeon_background.png', size=self.window.size, pos=self.window.pos)
            self.window.bind(size=self.update_bg, pos=self.update_bg)

        # cocked score label widget
        self.label = Label(
            text=f'You clicked {self.count} Times in this session.',
            font_size=18,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            color="#B8B8B8"
        )

        self.window.add_widget(self.label)

        # info label widget
        self.info = Label(
            text=f'ESC = Quit game',
            font_size=18,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            color="#2F60B5"
        )

        self.window.add_widget(self.info)

        # cock button
        self.button = Button(
            text="click",
            bold=True,
            size_hint=(0.1, 0.3),
            background_color="#272A41",
            background_normal=""
        )

        self.button.bind(on_press=self.callback)
        self.window.add_widget(self.button)

        # toggle button
        self.toggle = ToggleButton(
            text="Toggle Upgrades",
            bold=True,
            size_hint=(0.1, 0.1),
            background_color="#2F60B5",
            background_normal=""
        )

        self.toggle.bind(on_press=self.toggle_called)
        self.window.add_widget(self.toggle)

        return self.window

    def update_bg(self, *args):
        self.bg_rect.size = self.window.size
        self.bg_rect.pos = self.window.pos

    def toggle_called(self, instance):
        if self.called:
            self.called = False
            self.info.text = f'ESC = Quit game\n Upgrades Enabled'
            self.info.color = "#62A56F"
        else:
            self.called = True
            self.info.text = f'ESC = Quit game\n Upgrades Disabled'
            self.info.color = "#9B3533"

    def callback(self, instance):
        # Відтворення звуку при натисканні кнопки
        if self.sound:
            self.sound.play()
        else:
            print("Sound is not loaded or failed to play.")

        if self.called is False:
            if self.count <= 100:
                self.count += self.amount
                self.label.text = f"You clicked {self.count:,} Times in this session.\n +1 per click"
                self.label.color = "#B8B8B8"
                self.info.text = f'ESC = Quit game\nRewards:\n <100 = +1 coins per click'
                self.info.color = "#2F60B5"

            if self.count >= 100:
                self.count += self.first_upgrade + self.amount
                self.label.text = f"You clicked {self.count:,} Times in this session.\n +10 per click"
                self.label.color = "#B8B8B8"
                self.info.text = f'ESC = Quit game\nRewards:\n - 100 = +10 cocks per cock'
                self.info.color = "#2F60B5"

            if self.count >= 1000:
                self.count += self.second_upgrade
                self.label.text = f"You clicked {self.count:,} Times in this session.\n +100 per click"
                self.label.color = "#B8B8B8"
                self.info.text = f'ESC = Quit game\n Rewards:\n - 100 = +10 coins per click\n - 1000 = +100 coins per click'
                self.info.color = "#2F60B5"

            if self.count >= 10000:
                self.count += self.third_upgrade
                self.label.text = f"You clicked {self.count:,} Times in this session.\n +1000 per click"
                self.label.color = "#B8B8B8"
                self.info.text = f'ESC = Quit game\n Rewards:\n - 100 = +10 coins per click\n - 1000 = +100 coins per click\n - 10000 = +1000 coins per click'
                self.info.color = "#2F60B5"

            if self.count >= 200000:
                self.count += self.fourth_upgrade
                self.label.text = f"You clicked {self.count:,} Times in this session.\n +2000 per click"
                self.label.color = "#B8B8B8"
                self.info.text = f'ESC = Quit game\n Rewards:\n - 100 = +10 coins per click\n - 1000 = +100 coins per click\n - 10000 = +1000 coins per click'
                
        else:
            if self.called is True:
                self.count += self.amount
                self.label.text = f"You clicked {self.count:,} Times in this session.\n +1 per click"
                self.label.color = "#2F60B5"
                self.info.text = f'ESC = Quit game\n Upgrades Disabled'
                self.info.color = "#9B3533"

            else:
                self.label.text = f'ERROR: Failed to add "amount" to your coin score!'
                self.label.color = "#9B3533"


if __name__ == "__main__":
    game().run()
