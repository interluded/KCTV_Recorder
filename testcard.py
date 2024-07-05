import cv2
import subprocess
import numpy

def mse(imageA, imageB):
    err = numpy.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

# FFmpeg command to capture one frame from the feed
pipe = subprocess.Popen([ "ffmpeg",
            "-headers", "Origin: https://kcnawatch.org",
            "-headers", "Referer: https://kcnawatch.org", # fool kcnawatch
            "-i", "https://tv.nknews.org/tvhls/stream.m3u8",
            "-loglevel", "quiet", # no logging
            "-an", # no audio
            "-vframes", "1", # one frame
            "-f", "image2pipe",
            "-pix_fmt", "bgr24",
            "-vcodec", "rawvideo", "-"],
            stdin = subprocess.PIPE, stdout = subprocess.PIPE)

# Read the frame from the FFmpeg output
raw_image = pipe.stdout.read(720*576*3) # one 24 bit frame
image = numpy.frombuffer(raw_image, dtype='uint8').reshape((576,720,3))

# Save the captured frame as testcard.png
cv2.imwrite("testcard.png", image)

# Load the predefined testcard image
testcard = cv2.imread("testcard.png", cv2.IMREAD_UNCHANGED)

# Calculate the Mean Squared Error (MSE) between the captured frame and the testcard
image_difference = mse(image, testcard)
if image_difference < 10000:
    print("Testcard")
    testcard = True
else:
    print("No testcard")
    testcard = False
