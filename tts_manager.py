import os
import boto3
import json

class TTSManager():

    def __init__(self, access_key, secret_key, voices_file='./voices.json', region='us-west-2', file_format='mp3', cache_dir="./lines"):
        self.client = boto3.Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
            region_name=region).client('polly')

        json_f = json.load(open(voices_file, 'r'))
        self.voices = json_f["Voices"]
        self.current_voice = None
        self.set_voice("Brian")


        self.file_format = file_format
        self.cache_dir = cache_dir
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    def get_fullpath(self, voice, message):
        filename = self._get_filename(voice, message)
        full_path = os.path.join(self.cache_dir, filename)
        return os.path.abspath(full_path)

    def is_cached(self, voice, message):
        filepath = self.get_fullpath(voice, message)
        return os.path.exists(filepath)

    def voice_search(self, term, name_only=False):
        for voice in self.voices:
            if name_only:
                if term.lower() in voice["Id"].lower():
                    yield voice
            else:
                for v in voice.values():
                    if term.lower() in str(v).lower():
                        yield voice
                        break

    def set_voice(self, term):
        for voice in self.voice_search(term, True):
            self.current_voice = voice
            return
        print(f"No voices matched '{term}'")

    def _get_filename(self, voice, message):
        msg_hash = hash(message.lower())
        return f"{voice}{msg_hash}.{self.file_format}"

    def synthesize_speech(self, message: str):
        out_path = self.get_fullpath(self.current_voice["Id"], message)
        if self.is_cached(self.current_voice["Id"], message):
            return out_path
        else:
            response = self.client.synthesize_speech(
                Engine=self.current_voice['SupportedEngines'][0], # Use the best availible format
                OutputFormat=self.file_format,
                Text=message,
                VoiceId=self.current_voice['Id'])
            file = open(out_path, 'wb')
            file.write(response['AudioStream'].read())
            file.close()
            return out_path