import os
import random
import ctypes
import vlc
from inspect import getfullargspec


class RandomMediaIndexGenerator(object):
    def __init__(self):
        super(RandomMediaIndexGenerator, self).__init__()
        self.generatedIndex = []

    def __call__(self, media_count: int):
        randomIndex = random.randint(0, media_count - 1)
        while randomIndex in self.generatedIndex and len(self.generatedIndex) < media_count:
            randomIndex = random.randint(0, media_count - 1)
        self.generatedIndex.append(randomIndex)
        if len(self.generatedIndex) >= media_count:
            return None
        else:
            return randomIndex


def hasparam(func):
    return bool(getfullargspec(func).args)


def set_lib(dll, plugin_path=None):
    vlc.dll = ctypes.CDLL(dll)
    vlc.plugin_path = plugin_path


def ms2min(int_milliseconds: int):  # convert ms (int) to mm:ss (str)
    time = str(int((int_milliseconds / 1000) / 60)) + ":" + str(
        '%02d' % int((int_milliseconds / 1000) % 60))
    return time


def ms2hr(int_milliseconds: int):  # convert ms (int) to hh:mm:ss (str)
    time = str(int((int_milliseconds / (1000 * 60 * 60) % 24))) + ":" + str(
        '%02d' % int((int_milliseconds / (1000 * 60)) % 60)) + ":" + str(
        '%02d' % int((int_milliseconds / 1000) % 60))
    return time


def min2ms(int_minutes: int):  # convert minutes (int) to milliseconds (int)
    time = int_minutes * 60000
    return time


def ms2sec(int_ms: int):
    time = int_ms / 1000
    return float(time)
