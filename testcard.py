import cv2
import subprocess
import numpy as np

def mse(imageA, imageB):
    # Ensure the images have the same size
    if imageA.shape != imageB.shape:
        raise ValueError("Images must have the same dimensions for MSE calculation.")
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageB.shape[1])
    return err

# FFmpeg command to capture one frame from the feed
pipe = subprocess.Popen([
            "ffmpeg",
            "-headers", "Origin: https://kcnawatch.org",
            "-headers", "Referer: https://kcnawatch.org", # fool kcnawatch
            "-i", "https://tv.nknews.org/tvhls/stream.m3u8",
            "-loglevel", "quiet", # no logging
            "-an", # no audio
            "-vframes", "1", # one frame
            "-f", "image2pipe",
            "-pix_fmt", "bgr24",
            "-vcodec", "rawvideo", "-"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)

# Read the frame from the FFmpeg output
raw_image = pipe.stdout.read(720*576*3) # one 24 bit frame
image = np.frombuffer(raw_image, dtype='uint8').reshape((576, 720, 3))

# Save the captured frame as testcard.png (for debug purposes)
cv2.imwrite("captured_frame.png", image)

# Load the predefined testcard images
predefined_testcard1 = cv2.imread("predefined_testcard.png", cv2.IMREAD_UNCHANGED)
predefined_testcard2 = cv2.imread("predefined_testcard2.png", cv2.IMREAD_UNCHANGED)

# Calculate the Mean Squared Error (MSE) between the captured frame and the predefined testcards
try:
    mse1 = mse(image, predefined_testcard1)
    mse2 = mse(image, predefined_testcard2)
    if mse1 < 10000:
        print("testcard")
        is_testcard = True
    elif mse2 < 10000:
        print("testcard")
        is_testcard = True
    else:
        print("no testcard ")
        is_testcard = False
except ValueError as ve:
    print(f"Error: {ve}")
    is_testcard = False
