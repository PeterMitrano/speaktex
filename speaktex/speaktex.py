import json
import pathlib
import random
import string

import boto3
import pyglet
from colorama import Fore
from tex2py import tex2py

root = pathlib.Path.home() / '.speaktex'


def rand_str(length=16):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class TexSpeaker:

    def __init__(self):
        self.first_time_setup()
        # load map of text -> mp3 file names
        self.tts_memory = json.load(self.cachefilename.open("r"))

        # load cache
        self.client = boto3.Session().client('polly')

    def save_cache(self):
        json.dump(self.tts_memory, self.cachefilename.open("w"), indent=2)

    def request_tts(self, text) -> str:
        if text in self.tts_memory:
            audiofilename = self.tts_memory[text]
            return audiofilename

        print(Fore.CYAN + "Making API Request..." + Fore.RESET)
        response = self.client.synthesize_speech(VoiceId='Joanna', OutputFormat='mp3', Text=text)
        audiofilename = root / (rand_str() + ".mp3")
        self.tts_memory[text] = str(audiofilename)
        audiofile = audiofilename.open("wb")
        audiofile.write(response['AudioStream'].read())
        self.save_cache()
        return str(audiofilename)

    def speaktex(self, tex_filename: pathlib.Path):
        with tex_filename.open('r') as tex_file:
            data = tex_file.read()
        tex_tree = tex2py(data)

        audiofilename = self.request_tts(text='this is some sample text')

        speech = pyglet.media.load(audiofilename)
        self.player = pyglet.media.Player()
        self.player.queue(speech)
        self.player.play()
        self.player.on_eos = self.on_player_end_of_sequence

        pyglet.app.run()

    def on_player_end_of_sequence(self):
        print("done")
        pyglet.app.exit()

    def first_time_setup(self):
        if not root.exists():
            root.mkdir()

        self.cachefilename = root / 'cache.json'
        if not self.cachefilename.exists():
            json.dump({}, self.cachefilename.open("w"), indent=2)
