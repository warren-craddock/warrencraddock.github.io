#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import json
import re
import sys
import io
import os
import dataclasses
import mondrian_tree as mondrian
from PIL import Image
import pickle
import uuid
from pathlib import Path

ALBUM_LINK = 'https://photos.app.goo.gl/B1ZVQ2vZRicUU1y69'

for f in Path('static/photos').glob('*.jpg'):
  f.unlink()

print('Requesting album...')
r = requests.get(ALBUM_LINK)
if r.status_code != 200:
  print(f'Could not get Google Photos album: {r.status_code}')
  sys.exit(1)

soup = BeautifulSoup(r.text, 'html.parser')

images = {}
for script in soup.find_all('script'):
  if script.text.startswith('AF_initDataCallback'):

    result = re.findall(
        r'(https:\/\/lh3\.googleusercontent\.com\/[a-zA-Z0-9\-_]*)',
        script.text)
    links = set([l for l in result if len(l) == 173])

    for i, link in enumerate(links):
      print(i, link)
      basename = str(uuid.uuid4())

      widths = [
          100, 200, 300, 400, 500, 600, 700, 800, 1000, 1600, 2500, 3200, 4800,
          6400
      ]
      link_dict = {}
      largest_width = 0
      largest_height = 0
      for width in widths:
        r = requests.get(f'{link}=w{width}')
        if r.status_code != 200:
          print(f'Error while downloading url {link}: {r.status_code}')
          sys.exit(1)

        image = Image.open(io.BytesIO(r.content))
        print(f'image has width {image.width} and height {image.height}')

        filename = f'static/photos/{basename}-{image.width}.jpg'
        with open(filename, 'wb') as f:
          f.write(r.content)

        largest_width = max(largest_width, image.width)
        largest_height = max(largest_height, image.height)
        link_dict[image.width] = '/' + filename

      print(f'adding image for link {link} with largest width {largest_width}')
      images[basename] = mondrian.Image(link_dict, largest_width,
                                        largest_height)

print('images', images)

filename = 'google_photos_snapshot.bin'
with open(filename, 'wb') as f:
  pickle.dump(images, f)
  print('Wrote images to', filename)