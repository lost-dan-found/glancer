import random
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, Header, Footer, Static, ProgressBar, Sparkline

from macos_media import MacOSMediaController


class MediaApp(App):
    CSS = """
    Screen {
        background: #0f0f0f;
        align: center middle;
    }

    .controls {
        width: 100%;
        align: center middle;
        content-align: center middle;
        padding: 2 2;
    }

    Button {
        min-width: 12;
        min-height: 5;
        margin: 0 2;
        background: #1a1a1a;
        color: white;
        border: round #2a2a2a;
        text-align: center;
    }

    Button#play {
        min-width: 14;
        min-height: 6;
        background: #222222;
    }

    .track {
        text-align: center;
        padding: 1;
    }

    ProgressBar {
        width: 100%;
        margin: 1 0;
    }

    Sparkline {
        width: 100%;
        height: 5;
        margin-bottom: 1;
    }
    """


    BINDINGS = [
        ("space", "play", "Play/Pause"),
        ("n", "next", "Next"),
        ("p", "prev", "Previous"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Safe to define here — but not required yet
        self.media = None
        self.volume = 50

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Nothing Playing", id="track", classes="track")
        yield ProgressBar(total=100, id="progress")
        yield Sparkline(id="spark")

        yield Horizontal(
            Button("⏮", id="prev"),
            Button("⏯", id="play"),
            Button("⏭", id="next"),
            classes="controls"
        )
        yield Footer()

    def on_mount(self) -> None:
        # Safe place to initialize controller
        self.media = MacOSMediaController()

        # Grab widgets
        self.spark = self.query_one("#spark", Sparkline)
        self.progress = self.query_one("#progress", ProgressBar)
        self.track = self.query_one("#track", Static)

        # Timer for UI updates
        self.set_interval(0.3, self.update_ui)

    # IMPORTANT: not named refresh()
    def update_ui(self, **kwargs):
        if not self.media:
            return

        data = self.media.now_playing()

        if not data:
            self.track.update("Nothing Playing")
            self.spark.data = [random.randint(0, 2) for _ in range(40)]
            return

        title = data.get("title") or "Unknown Title"
        artist = data.get("artist") or "Unknown Artist"
        dur = data.get("duration") or 1
        pos = data.get("elapsed") or 0

        self.track.update(f"{title} — {artist}")
        self.progress.total = int(dur)
        self.progress.progress = int(pos)

        # Fake waveform tied loosely to duration
        intensity = max(1, int(self.volume / 5))
        self.spark.data = [random.randint(0, intensity) for _ in range(40)]

    def on_button_pressed(self, event):
        if not self.media:
            return

        match event.button.id:
            case "prev":
                self.media.previous()
            case "play":
                self.media.play_pause()
            case "next":
                self.media.next()

    def action_play(self):
        if self.media:
            self.media.play_pause()

    def action_next(self):
        if self.media:
            self.media.next()

    def action_prev(self):
        if self.media:
            self.media.previous()


if __name__ == "__main__":
    MediaApp().run()
