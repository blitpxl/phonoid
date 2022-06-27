import time

from app.avlc import AudioPlayer

a = AudioPlayer()
a.add_local_media(r"C:\Users\Kevin\Music\Gryffin - Tie Me Down ft. Elley Duhé.mp3")
a.play()
print(a.vlcPlayer.get_state())
time.sleep(10)
a.pause()
print(a.vlcPlayer.get_state())
a.wait()
