# chrysalis


This project requires Python 3.6+ to run. It does not work with Python 2.7! The PI is set uo use Python 2.7 by. default. you need to update. itto prefer python3. See:
https://learn.sparkfun.com/tutorials/python-programming-tutorial-getting-started-with-the-raspberry-pi/configure-your-pi

This project is built with a reactive programming approach and uses the RxPY library heavily. See https://rxpy.readthedocs.io/en/latest/

More background (language agnostic) on reactive programming can be found here: http://reactivex.io/

# Configuration

All configuration is set in `src/config.py`

## Values
* __STEPS:__ List of step objects which store timecode information as well as soundthreshold (triggerig information)
* __SOUND_DEVICE:__  The audio device for our microphone. See. https://python-sounddevice.readthedocs.io/en/0.3.13/
* __WINDOW:__ Window for our microphone. See https://python-sounddevice.readthedocs.io/en/0.3.13/
* __VIDEO_FILE:__ Path to the Chrysalis video file


# Audio
The Raspberry PI does not have a built in mirophone/line input so a external USB sound card is required. Typically the mirophone appears as device number 1 on the pi.  You can set the device number in config.py. set SOUND_DEVICE to the integer corresponding to the sound device you want to connect to.

```bash
sudo apt-get install libportaudio2
```


# Video Playback

Video is played back full screen on the Raspberry Pi with the command line application OMXPlayer.
We use a python library, omxplayer-wrapper (https://github.com/willprice/python-omxplayer-wrapper) to communicate with OMXPlayer asynchronously over dbus. There is a mock which is present if omxplayer-wrapper fails to initialize (which is useful for development on your own desktop if you're not running ona. pi.) It simulates most interactions with the real omxplayer.  I also found I needed to install some additional dependencies to get this library working, in particular:

```bash
sudo apt-get install libgtk2.0-dev
```

# Setup

```bash
sudo apt-get install libgtk2.0-dev
sudo apt-get install libportaudio2
pip install -r requirements.txt
```

# Run

From the `src` directory

```bash
python main.py
```

