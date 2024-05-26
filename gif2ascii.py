import requests
from PIL import Image, ImageSequence
from io import BytesIO
import os
import time

# ASCII characters used to build the output text
ASCII_CHARS = "@%#*+=-:. "

def fetch_image(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    return image

def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayscale_image(image):
    return image.convert("L")

def pixel_to_ascii(image):
    pixels = image.getdata()
    ascii_str = "".join([ASCII_CHARS[pixel // 32] for pixel in pixels])
    return ascii_str

def frame_to_ascii(frame, width=100):
    frame = resize_image(frame, width)
    frame = grayscale_image(frame)
    ascii_str = pixel_to_ascii(frame)
    img_width = frame.width
    ascii_str_len = len(ascii_str)
    ascii_img = "\n".join([ascii_str[index: index + img_width] for index in range(0, ascii_str_len, img_width)])
    return ascii_img

def gif_to_ascii(url, width=100):
    image = fetch_image(url)
    frames = []
    for frame in ImageSequence.Iterator(image):
        ascii_frame = frame_to_ascii(frame, width)
        frames.append(ascii_frame)
    return frames

def main():
    url = input("Enter the URL of the GIF: ")
    width = int(input("Enter the width of the ASCII art (default 100): ") or 100)
    ascii_frames = gif_to_ascii(url, width)
    
    while True:
        for frame in ascii_frames:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(frame)
            time.sleep(0.1)  # Adjust the delay as needed

if __name__ == "__main__":
    main()
