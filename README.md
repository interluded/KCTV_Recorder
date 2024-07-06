# KCTV_Checker

This is a helpful set of programs to record Korean Central TV (KCTV) from KCNAWatch without recording the endless colour bars when there is no programming.

## Special thanks

Thank you [thinkingsand](https://github.com/thinkingsand) for the testcard.py code. This project would not exist without you!

## SETUP

To set up KCTV_Checker, you will need:

* A VPS (Virtual Private Server)
* Python 3, numpy, and cv2
* A recording station (e.g., a computer with FFMPEG installed)

### Step-by-Step Setup Instructions

1. Copy the following files to your VPS:
	* predefined_testcard.png
	* testcard.py
	* checker.py
2. Run checker.py (in a screen, preferably) in the same directory as the other files.
3. Change the IP address in check_response.cpp to your VPS's IP; make sure it's static with port 8000 open
4. On the recording machine, build the following C++ files using `g++`:
	* check_up.cpp (compile with `g++ -o check_response check_response.cpp -lcurl`)
	* monitor.cpp (compile with `g++ -o monitor checkerClient.cpp`)
5. Run the recording machine and start FFMPEG to record KCTV.

### What it does

KCTV_Checker is a set of scripts and C++ programs that help you record Korean Central TV (KCTV) from KCNAWatch without recording the endless colour bars when there is no programming. It uses test cards to detect when KCTV is broadcasting 
and skips the recording of the colour bars.

### How it works

1. KCTV Broadcasts a set of colour bars, when there is no programming.
2. If KCTV is not broadcasting, the script will skip the recording of the colour bars.
3. If KCTV is broadcasting, the script will start recording using FFMPEG.

### Troubleshooting

* Q: I get an error message saying "No such file or directory" when running checker.py.
A: Make sure that predefined_testcard.png is in the same directory as the other files.
* Q: The recording stops after a few minutes.
A: Check if KCTV is still broadcasting. If not, the script will stop recording.
* Q: I get an error message saying "Unable to open device" when running checker.py.
A: Ensure FFMPEG is installed and working properly on your recording machine.

### Contributing

Contributions are welcome! Please open a pull request or contact the maintainer if you have any suggestions or improvements.

### License

KCTV_Checker is released under the  License. See LICENSE for more information.

