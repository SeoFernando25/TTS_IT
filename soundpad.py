import time


class Soundpad():
    _PIPE_ADRESS = r'\\.\PIPE\sp_remote_control'

    def __init__(self, verbose=False):
        try:
            self.pipe = open(Soundpad._PIPE_ADRESS, 'rb+', buffering=0)
        except FileNotFoundError as e:
            raise FileNotFoundError("Wasn't able to open pipe. Is Soundpad open?")
        self.verbose = verbose

    def __del__(self):
        self.pipe.close()

    # Commands taken from https://github.com/medokin/soundpad-connector/blob/a9eccfcdca2ad61fe4091f90fa3fe4120d6e8097/src/SoundpadConnector/Soundpad.Calls.cs
    # Not all commands are implemented

    def is_alive(self):
        return self.send("IsAlive()")

    def play_sound(self, index):
        return self.send(f"DoPlaySound({index})")

    def play_previous_sound(self):
        return self.send("DoPlayPreviousSound()")

    def play_next_sound(self):
        return self.send("DoPlayNextSound()")

    def stop_sound(self):
        return self.send("DoStopSound()")

    def toggle_pause(self):
        return self.send("DoTogglePause()")

    def jump_seconds(self, seconds):
        return self.send(f"DoJumpMs({int(seconds * 1000)})")

    def seek_seconds(self, seconds):
        return self.send(f"DoSeekMs({int(seconds * 1000)})")


    def start_recording(self):
        return self.send("DoStartRecording()")

    def stop_recording(self):
        return self.send("DoStopRecording()")

    def add_sound(self, path):
        return self.send(f"DoAddSound(\"{path}\")")


    def get_file_count(self):
        return int(self.send("GetSoundFileCount()"))


    def play_last(self):
        number = self.get_file_count()
        return self.play_sound(number)

    def select_index(self, index):
        return self.send(f"DoSelectIndex({index})")

    def remove_selected(self, remove_from_disk=False):
        return self.send(
            f"DoRemoveSelectedEntries({remove_from_disk})")

    def remove_all(self):
        count = int(self.get_file_count())
        for i in range(0, count+1):
            self.remove_selected()

    def get_playback_position_in_ms(self):
        val = self.send("GetPlaybackPositionInMs()")
        return int(val)

    def get_playback_duration_in_ms(self):
        val = self.send("GetPlaybackDurationInMs()")
        return int(val)

    def search(self, search_term):
        return self.send(f"DoSearch({search_term})")

    def reset_search(self):
        return self.send("DoResetSearch()")

    def select_previous_hit(self):
        return self.send("DoSelectPreviousHit()")

    def select_next_hit(self):
        return self.send("DoSelectNextHit()")

    def scroll(self, rows):
        return self.send(f"DoScrollBy({rows})")

    def send(self, request: str):
        self.pipe.write(request.encode("utf-8"))
        time.sleep(0.1) # Is there a better way to do this?
        response = self.pipe.read(32).decode("utf-8")
        if self.verbose:
            print("{} -> {}".format(request, response))
        return True if response == "R-200" else response