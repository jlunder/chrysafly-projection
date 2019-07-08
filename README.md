# chrysalis
This project is designed to be run on a Raspberry PI. It is interactive video component for chrysalis.

This project requires Python 3.6+ to run. It does not work with Python 2.7! Because the PI is set to use Python 2.7 by default you will probably need to update it to prefer Python3. See:
https://learn.sparkfun.com/tutorials/python-programming-tutorial-getting-started-with-the-raspberry-pi/configure-your-pi

This project is built with a reactive programming approach and uses the RxPY library heavily. See https://rxpy.readthedocs.io/en/latest/

More background (language agnostic) on reactive programming can be found here: http://reactivex.io/

# Basic Logic
There is a set of Step objects. Each step object (see step.py) defines a single part of the video. Each step contains times for the start and the stop of the video loop and a start and stop of a transition. It also contains a trigger threshold. These timecodes are floats which correspond to the number of seconds into the video. We use a single video and use the omxplayer-wrapper set_position method to jump around the video file This approach was used due to lag in siwtching quickly between video files.

## How it works:
1. We capture audio intensity from the microphone.
2. The audio intensity "indexes" into the list of steps. If we pass a threshold we treat the "loop" as a continuous part of the video and move on to the next step.

⋅⋅⋅For example:
⋅⋅⋅* Audio is loud enough to only index into step 1: Plays step 1 loop and continues looping.
⋅⋅⋅* Audio is loud enough to index into step 2: Plays step 1 loop once, plays step 1 transition once, plays step 2 loop and continues looping.
⋅⋅⋅* Audio is loud enough to index past the last step: Plays through all proceeding loops and transitions and resets back to step 1.
4. We jump to a place in the video.
5. If we are in a loop we loop until the next step occurs.
6. If we reach the end (maximum volume) the sequence resets.

Basically the video will stay looping at a particular step (level) until the threshold sound intensity level above it is exceeded. It will then end the loop and display the video clips on the next step.


# Configuration

All configuration is set in `src/config.py`

## Values
* __STEPS:__ [List[Step]]List of step objects which store timecode information as well as soundthreshold (triggerig information)
* __SOUND_DEVICE:__  [int] The audio device for our microphone. See. https://python-sounddevice.readthedocs.io/en/0.3.13/
* __WINDOW:__ [float] How long in seconds do you want to average (smooth) the audio sampling. Higher values will make the system less reactive to abrupt sounds.
* __VIDEO_FILE:__  [str] Path to the Chrysalis video file


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

