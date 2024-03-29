![Phonoid's User Interface](https://i.ibb.co/HdSC9VV/Phonoid.png)

![Phonoid running on Windows 10](https://i.ibb.co/SQ6LvKx/Screenshot-490.png)

# About
Phonoid is a desktop music player written in Python + Qt5 solely
with a main purpose of providing a feature-rich music player with simple/minimalistic and cross-platform user interface.

# Status
Phonoid is in the middle of a rewrite as of now. Migrating from Python -> C++ and QtWidgets -> QML to support hardware rendering.

Though, you can still try the current python version.
By default, it will scan your music folder `(C:/Users/*Username*/Music)` for audio files. You can't change it just yet (unless you edit the source code.)

# Support
Your funds will go towards buying domain and my personal needs to maintain this software. Consider supporting me via:

- [PayPal](https://paypal.me/kevinrubycon)

- [Ko-Fi](https://ko-fi.com/vinrato)

[comment]: <> (✓)

Phonoid targets Windows, Linux, and macOS, but for now I'm focusing my attention on Windows and try to optimize it.

# Things to implement
- ~~Music playback functionality (duh)~~ ✓
- ~~Serialization/Marshalling system to save parsed tracks~~ ✓
- Window to view track details (location, album, duration, genre, etc)
- Automatic music library scanning system
- Implement a playlist system
- System that allow the user to 'favourite' a song
- Recently played/History
- Settings UI
- ~~Equalizer UI~~ ✓
- YouTube Playback
- YouTube integration that allow the user to add YouTube tracks as if it's an actual music file
- Search functionality for each tab
- I'll add things as i go on
