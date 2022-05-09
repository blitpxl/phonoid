from vlc import libvlc_audio_equalizer_new
from .event import EqualizerEvent


class AudioEqualizer(object):
    def __init__(self, AudioPlayer):
        super(AudioEqualizer, self).__init__()
        self.AudioPlayerInstance = AudioPlayer
        self.vlcEqualizer = libvlc_audio_equalizer_new()
        self.eq2pass = False

    def set_eq_values(self, eq_index, eq_value):
        if eq_index > 10 or eq_index < 0:
            e = f"The equalizer index band of {eq_index} doesn't exist."
            raise IndexError(e)
        else:
            if eq_index != 10:
                self.vlcEqualizer.set_amp_at_index(eq_value, eq_index)
            else:
                self.vlcEqualizer.set_preamp(eq_value)
            self.toggle_equalizer(True)

    def toggle_equalizer(self, on: bool):
        if on:
            self.AudioPlayerInstance.vlcPlayer.set_equalizer(self.vlcEqualizer)
            EqualizerEvent.EqualizerEnabled()
        else:
            self.AudioPlayerInstance.vlcPlayer.set_equalizer(None)
            EqualizerEvent.EqualizerDisabled()

    def toggle_2pass(self, on: bool):
        if on:
            if not self.eq2pass:
                self.AudioPlayerInstance.add_args("--equalizer-2pass")
                self.toggle_equalizer(True)
                self.eq2pass = True
                EqualizerEvent.Enabled2Pass()
            else:
                pass
        else:
            if self.eq2pass:
                self.AudioPlayerInstance.remove_args("--equalizer-2pass")
                self.toggle_equalizer(True)
                self.eq2pass = False
                EqualizerEvent.Disabled2Pass()
            else:
                pass

    @staticmethod
    def connect_event(event, function):
        event.connect_callback(function)
