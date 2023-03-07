#!/usr/bin/env python3

import copy
import json
import pickle
import dataclasses
import mondrian_tree as mondrian
from pathlib import Path


def finalize_image(image):
  image = dataclasses.asdict(image)

  del image['original_width']
  del image['original_height']
  del image['link']

  return image


for f in Path('static/js').glob('layouts-*'):
  f.unlink()

with open('google_photos_snapshot.bin', 'rb') as f:
  images = pickle.load(f)

filename = f'static/js/photo_metadata.js'
photo_metadata = {}
for basename, image in images.items():
  photo_metadata[basename] = dataclasses.asdict(image)
with open(filename, 'w') as f:
  f.write(f"export const PHOTO_METADATA = {json.dumps(photo_metadata)};")

# widths = sorted(list(range(100, 6000, 50)))
widths = [400, 800, 1600, 3200, 6400]
filename = 'static/js/widths.js'
with open(filename, 'w') as f:
  f.write(f"export const WIDTHS = {json.dumps(list(reversed(widths)))};")

for width in widths:
  layouts = []
  while len(layouts) < 10:
    layout = mondrian.build_random_layout(images, width)
    if layout:
      height = max(im.y + im.height for im in layout.values())
      for basename, image in layout.items():
        layout[basename] = finalize_image(image)
      layouts.append(dict(images=layout, width=width, height=height))

  filename = f'static/js/layouts-{width}.js'
  with open(filename, 'w') as f:
    f.write(f"export const LAYOUTS = {json.dumps(layouts)};")

  print(f'Successfully built {len(layouts)} random trees for width {width}')

print('Success!')
