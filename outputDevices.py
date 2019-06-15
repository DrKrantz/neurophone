#!/usr/bin/env python

""" DOCSTRING """

__author__ = "Benjamin Staude"
__email__ = "benjamin.staude@gmail.com"
__date__ = 140621

import pygame.midi as pm


class Sforzando(pm.Output):
    NAME = 'sforzando'

    def __init__(self):
        pm.init()
        self.__noteRange = list(range(1, 127))
        id = self.__getDeviceId(self.NAME)
        if id == -1:
            print("SETUP Warning: output: " + self.NAME + " not available!!!")
        else:
            super(Sforzando, self).__init__(id)

    def __getDeviceId(self, midiport):
        n_device = pm.get_count()
        foundId = -1
        for id in range(n_device):
            if int(pm.get_device_info(id)[1] == midiport.encode()) & \
                    int(pm.get_device_info(id)[3] == 1):
                foundId = id
        return foundId
