import argparse
import pyaudio
import numpy as np

from pythonosc import dispatcher
from pythonosc import osc_server
from _thread import start_new_thread


class Player:
    def __init__(self, n_notes, paudio):
        self.__p = paudio

        self.base_data = np.array([])
        self.volume = 0.5  # range [0.0, 1.0]

        fs = 44100  # sampling rate, Hz, must be integer

        # the duration of the sniplet is critical! Too short, and the sound will be noisy
        duration = .1  # in seconds, may be float
        f = 440.0  # sine frequency, Hz, may be float
        '''
        frequency = 440 * 2^^(n/12) - for note n
        for n=−21,−19,…,27
        from https://www.intmath.com/trigonometric-graphs/music.php
        '''

        self.base_data = self.volume * (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs))
        # for paFloat32 sample values must be in range [-1.0, 1.0]
        self.stream = p.open(format=pyaudio.paFloat32,
                             channels=1,
                             rate=fs,
                             output=True)

    def sound_loop(self, args):
        while True:
            self.stream.write((self.volume*self.base_data).astype(np.float32).tobytes())

    def play(self):
        start_new_thread(self.sound_loop, (None, ))

    def set_volume(self, addr, args, volume):
        print("receiving", addr, args, volume)
        self.volume = volume


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=5005, help="The port to listen on")
    args = parser.parse_args()

    p = pyaudio.PyAudio()
    player = Player(10, p)
    player.play()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/volume", player.set_volume, "Volume")

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    server.serve_forever()
