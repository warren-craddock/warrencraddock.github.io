from __future__ import annotations

import copy
import dataclasses
from typing import Dict, Optional, Sequence, Union
from operator import itemgetter
import random
import json
import os
import glob


@dataclasses.dataclass
class Image:
  link: Dict[int, str]
  original_width: int
  original_height: int
  width: float = 0
  height: float = 0
  x: float = 0
  y: float = 0

  def aspect_ratio(self):
    return float(self.original_width) / self.original_height

  def set_width(self, width: float):
    self.width = width
    self.height = width / self.aspect_ratio()

  def set_height(self, height: float):
    self.height = height
    self.width = height * self.aspect_ratio()

  def layout(self, x: float, y: float):
    self.x = x
    self.y = y

  def area(self):
    return self.width * self.height


def horizontal_layout(images, tree, height, x: float = 0, y: float = 0):
  aspect_ratios = [vertical_aspect_ratio(images, c) for c in tree]
  widths = [height * a for a in aspect_ratios]

  for node, width in zip(tree, widths):
    if isinstance(node, list):
      vertical_layout(images, node, width, x, y)
    else:
      # Consider making this one call.
      images[node].set_width(width)
      images[node].layout(x, y)

    x += width


def vertical_layout(images, tree, width, x: float = 0, y: float = 0):
  aspect_ratios = [horizontal_aspect_ratio(images, c) for c in tree]
  heights = [width / a for a in aspect_ratios]

  for node, height in zip(tree, heights):
    if isinstance(node, list):
      horizontal_layout(images, node, height, x, y)
    else:
      # Consider making this one call.
      images[node].set_height(height)
      images[node].layout(x, y)

    y += height


# FIXME I'm not a huge fan of these if statements... is there some way
# to unify them?
def vertical_aspect_ratio(images, node):
  if isinstance(node, list):
    return 1.0 / sum(1.0 / horizontal_aspect_ratio(images, c) for c in node)
  else:
    return images[node].aspect_ratio()


def horizontal_aspect_ratio(images, node):
  if isinstance(node, list):
    return sum(vertical_aspect_ratio(images, c) for c in node)
  else:
    return images[node].aspect_ratio()


def images_in_tree(node):
  if isinstance(node, list):
    accumulator = []
    for c in node:
      accumulator += images_in_tree(c)
    return accumulator
  else:
    return [node]


def area(images, node):
  if isinstance(node, list):
    return sum(area(images, c) for c in node)
  else:
    return images[node].area()


def select_dict_keys(D, keys):
  return {key: D[key] for key in D.keys() if key in keys}


# FIXME maybe return the image and its area, for convenience.
def get_smallest_image(images, node):
  image_ids = images_in_tree(node)
  images = select_dict_keys(images, image_ids)
  images_and_areas = [(k, v.area()) for k, v in images.items()]
  index, element = min(images_and_areas, key=itemgetter(1))
  return index


def get_largest_image(images, node):
  image_ids = images_in_tree(node)
  images = select_dict_keys(images, image_ids)
  images_and_areas = [(k, v.area()) for k, v in images.items()]
  index, element = max(images_and_areas, key=itemgetter(1))
  return index


def images_are_not_too_small(images, tree, width):
  smallest_width = images[get_smallest_image(images, tree)].width
  return smallest_width > (width / 4.0)


def images_are_not_too_large(images, tree, width):
  largest_width = images[get_largest_image(images, tree)].width
  return largest_width < (width * 0.35)


def convert_image_into_container(images, node, image_id):
  if isinstance(node, list):
    if image_id in node:
      idx = node.index(image_id)
      node[idx] = [image_id]
      return node[idx]
    else:
      for c in node:
        result = convert_image_into_container(images, c, image_id)
        if result:
          return result


def split_largest_image_and_insert(images, tree, image_id, width):
  images_copy, tree_copy = copy.deepcopy(images), copy.deepcopy(tree)
  largest_image = get_largest_image(images_copy, tree_copy)
  node = convert_image_into_container(images_copy, tree_copy, largest_image)
  node.append(image_id)
  vertical_layout(images_copy, tree_copy, width)
  if images_are_not_too_small(images_copy, tree_copy, width):
    return images_copy, tree_copy
  else:
    return None, None


# FIXME consider unifying the `images` and `tree` params.
def insert(images, tree, image_id, width):
  original_images = copy.copy(images)
  original_tree = copy.copy(tree)

  if not tree:
    tree.append(image_id)
    vertical_layout(images, tree, width)
    return images, tree

  # Try to find the largest image, split it into an opposite-direction
  # container, and insert the image into that new container. Doing this first
  # encourages a complex tree structure.
  new_images, new_tree = split_largest_image_and_insert(
      images, tree, image_id, width)
  if new_tree:
    return new_images, new_tree

  # If that wasn't successful, just put the image at the end of the outermost
  # container.
  tree.append(image_id)
  vertical_layout(images, tree, width)
  return images, tree


def build_random_layout(images, width):
  tree = []
  keys_list = list(images.keys())
  random.shuffle(keys_list)
  for image_id in keys_list:
    new_images, new_tree = insert(images, tree, image_id, width)
    if new_tree:
      images, tree = new_images, new_tree

  vertical_layout(images, tree, width)

  if images_are_not_too_large(images, tree, width):
    return images
