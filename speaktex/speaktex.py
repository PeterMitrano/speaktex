import pathlib
import string
import tempfile
import random

import boto3
import pyglet
from tex2py import tex2py

root = pathlib.Path(tempfile.gettempdir()) / 'speaktex'

# map of text -> mp3 file names
tts_memory = {}


def rand_str(length=16):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def request_tts(client, text):
    if text in tts_memory:
        audiofilename = tts_memory[text]
        return audiofilename

    response = client.synthesize_speech(VoiceId='Joanna', OutputFormat='mp3', Text=text)
    # audiofilename = root / (rand_str() + ".mp3")
    audiofilename = pathlib.Path('test.mp3')
    tts_memory[text] = audiofilename
    audiofile = audiofilename.open("wb")
    audiofile.write(response['AudioStream'].read())
    return audiofilename


def speaktex(tex_filename: pathlib.Path):
    if not root.exists():
        root.mkdir()

    with tex_filename.open('r') as tex_file:
        data = tex_file.read()
    tex_tree = tex2py(data)

    client = boto3.Session().client('polly')

    audiofilename = request_tts(client, text='this is some sample text')

    player = pyglet.media.Player()
    speech = pyglet.media.load(audiofilename)
    player.queue(speech)
    pyglet.app.run()
