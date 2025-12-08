from MediaPlayer import MPNowPlayingInfoCenter
import subprocess


class MacOSMediaController:
    def __init__(self):
        self.center = MPNowPlayingInfoCenter.defaultCenter()

    def now_playing(self):
        info = self.center.nowPlayingInfo()
        if not info:
            return None

        return {
            "title": info.get("MPMediaItemPropertyTitle", ""),
            "artist": info.get("MPMediaItemPropertyArtist", ""),
            "album": info.get("MPMediaItemPropertyAlbumTitle", ""),
            "duration": info.get("MPMediaItemPropertyPlaybackDuration", 0),
            "elapsed": info.get("MPNowPlayingInfoPropertyElapsedPlaybackTime", 0),
        }

    def play_pause(self):
        self._key_code(16)

    def next(self):
        self._key_code(17)

    def previous(self):
        self._key_code(18)

    def _key_code(self, code):
        subprocess.run(
            ["osascript", "-e", f'tell application "System Events" to key code {code}'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
