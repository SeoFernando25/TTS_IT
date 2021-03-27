import cmd
import argparse
import os
from soundpad import Soundpad
from tts_manager import TTSManager
import configparser

class ClientShell(cmd.Cmd):
    intro = 'help or ? to list commands.\n'
    prompt = '(? TTS) '

    def __init__(self, access_key, secret_key):
        self.sp = Soundpad(True)
        file_dir_name = os.path.dirname(os.path.abspath(__file__))
        cache_folder = os.path.join(file_dir_name, "lines")
        self.tts = TTSManager(access_key, secret_key, cache_dir=cache_folder)
        ClientShell.prompt = f"({self.tts.current_voice['Id']} TTS) "
        super().__init__()

    def do_say(self, msg):
        'Downloads and speaks the text audio on Soundpad. If message is empty enter immediate mode'
        if len(msg) == 0:
            print("Entering immediate mode - Ctrl-C to exit")
            while True:
                try:
                    text = input(f"({self.tts.current_voice['Id']} says) ")
                    out_path = self.tts.synthesize_speech(text)
                    self.sp.add_sound(out_path)
                    self.sp.play_last()
                except KeyboardInterrupt as e:
                    print("Going back to normal mode")
                    break
        else:
            out_path = self.tts.synthesize_speech(msg)
            self.sp.add_sound(out_path)
            self.sp.play_last()

    def do_search(self, arg):
        "Search availible voices"
        print("Voices availible are \n")
        for voice in self.tts.voice_search(arg):
            print(f"{voice['LanguageName']} : {voice['Id']}")

    def do_quit(self, arg):
        'Do clean up and exit'
        self.sp.stop_sound()
        return True
                  
    def do_set(self, voice):
        'Changes the current voice'
        self.tts.set_voice(voice)
        ClientShell.prompt = f"({self.tts.current_voice['Id']} TTS) "

    def emptyline(self):
         pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A simple shell that uses Amazon Polly and SoundPad')
    parser.add_argument('config', help='The configuration file')

    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)

    access_key = config['Credentials']['AccessKeyId']
    secret_key = config['Credentials']['SecretKey']



    ClientShell(access_key, secret_key).cmdloop()
