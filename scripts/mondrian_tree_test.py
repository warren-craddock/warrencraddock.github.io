import unittest
import mondrian_tree_array as mondrian
import json
import dataclasses


def create_images():
  return {
      'a': mondrian.Image(link='a.jpg',
                          original_width=1500,
                          original_height=1000),
      'b': mondrian.Image(link='b.jpg',
                          original_width=3000,
                          original_height=2000),
      'c': mondrian.Image(link='c.jpg',
                          original_width=6000,
                          original_height=6000),
      'd': mondrian.Image(link='d.jpg',
                          original_width=4000,
                          original_height=6000)
  }


def create_tree():
  return [['a', 'b'], ['c', 'd']]


def print_tree(images, node):
  if isinstance(node, list):
    for c in node:
      print_tree(images, c)
  else:
    print(images[node])


class TestContainers(unittest.TestCase):
  def test_horizontal_aspect_ratio_1(self):
    images = create_images()
    tree = ['a', 'b']
    aspect_ratio = mondrian.horizontal_aspect_ratio(images, tree)
    self.assertEqual(aspect_ratio, (3 / 2) + (3 / 2))

  def test_horizontal_aspect_ratio_2(self):
    images = create_images()
    tree = ['c', 'd']
    aspect_ratio = mondrian.horizontal_aspect_ratio(images, tree)
    self.assertEqual(aspect_ratio, 1 + (2 / 3))

  def test_vertical_aspect_ratio(self):
    images = create_images()
    tree = ['a', 'b']
    aspect_ratio = mondrian.vertical_aspect_ratio(images, tree)
    self.assertEqual(aspect_ratio, 3 / 4)

  def test_horizontal_layout(self):
    print('### test_horizontal_layout')
    images = create_images()
    tree = ['a', 'b']
    mondrian.horizontal_layout(images, tree, 1500)

  def test_simple_tree_aspect_ratio(self):
    images = create_images()
    tree = create_tree()
    aspect_ratio = mondrian.vertical_aspect_ratio(images, tree)
    self.assertEqual(aspect_ratio,
                     1 / (1 / ((3 / 2) + (3 / 2)) + 1 / (1 + (2 / 3))))

  def test_get_largest_leaf_container(self):
    print('### test_get_largest_leaf_container')
    images = create_images()
    tree = create_tree()
    mondrian.vertical_layout(images, tree, 1000)

    print('### Calling get_largest_leaf_container')
    print('### Returned', mondrian.get_largest_leaf_container(images, tree))

  # def test_simple_tree_layout(self):
  #   print('### test_simple_tree_layout')
  #   images = create_images()
  #   tree = create_tree()
  #   mondrian.vertical_layout(images, tree, 1000)
  #   expected_images = {
  #       'a':
  #       mondrian.Image(link='a.jpg',
  #                      original_width=1500,
  #                      original_height=1000,
  #                      width=500.0,
  #                      height=333.3333333333333,
  #                      x=0,
  #                      y=0),
  #       'b':
  #       mondrian.Image(link='b.jpg',
  #                      original_width=3000,
  #                      original_height=2000,
  #                      width=500.0,
  #                      height=333.3333333333333,
  #                      x=500.0,
  #                      y=0),
  #       'c':
  #       mondrian.Image(link='c.jpg',
  #                      original_width=6000,
  #                      original_height=6000,
  #                      width=600.0,
  #                      height=600.0,
  #                      x=0,
  #                      y=333.3333333333333),
  #       'd':
  #       mondrian.Image(link='d.jpg',
  #                      original_width=4000,
  #                      original_height=6000,
  #                      width=400.0,
  #                      height=600.0,
  #                      x=600.0,
  #                      y=333.3333333333333)
  #   }
  #   self.assertEqual(images, expected_images)

  #   # FIXME this makes the test non-hermetic.
  #   images_list = [dataclasses.asdict(x) for x in images.values()]
  #   with open('layouts.js', 'w') as f:
  #     f.write(f'export const LAYOUT = {json.dumps(images_list)};')

  def test_get_largest_leaf_container(self):
    print('### test_get_largest_leaf_container')
    images = create_images()
    tree = create_tree()
    mondrian.vertical_layout(images, tree, 1000)
    largest_leaf_container = mondrian.get_largest_leaf_container(images, tree)
    print('### Largest leaf container is', largest_leaf_container)
    self.assertEqual(largest_leaf_container, ['c', 'd'])

  def test_get_largest_image_1(self):
    print('### test_get_largest_image_1')
    images = create_images()
    tree = create_tree()
    mondrian.vertical_layout(images, tree, 1000)
    largest_image = mondrian.get_largest_image(images, tree)
    print('### Largest image is', largest_image)
    self.assertEqual(largest_image, 'c')

  def test_get_largest_image_2(self):
    images = create_images()
    tree = create_tree()

    images['a'].set_width(1000)
    images['b'].set_width(200)
    images['c'].set_width(200)
    images['d'].set_width(200)

    largest_image = mondrian.get_largest_image(images, tree)
    self.assertEqual(largest_image, 'a')

  def test_convert_image_into_container(self):
    print('### test_convert_image_into_container')
    images = create_images()
    tree = create_tree()
    node = mondrian.convert_image_into_container(images, tree, 'c')
    print('### tree', tree)
    print('### node', node)

  def test_images_in_tree(self):
    print('### test_images_in_tree')
    tree = [['a', ['b', 'c'], ['d'], ['e', 'f'], 'g']]
    result = mondrian.images_in_tree(tree)
    self.assertEqual(result, ['a', 'b', 'c', 'd', 'e', 'f', 'g'])

  def test_insert_next_to_largest_image(self):
    print('### test_insert_next_to_largest_image')
    images = create_images()
    tree = ['a']
    mondrian.vertical_layout(images, tree, 1000)
    images, tree = mondrian.insert_next_to_largest_image(
        images, tree, 'b', 1000)
    print('### after insert, tree is', tree)

  def test_insert(self):
    print('### test_insert')
    images = create_images()
    tree = []

    images, tree = mondrian.insert(images, tree, 'a', 1000)
    print('### After insert a, images is', images)
    print('### After insert a, tree is', tree)

    images, tree = mondrian.insert(images, tree, 'b', 1000)
    print('### After insert b, images is', images)
    print('### After insert b, tree is', tree)

    images, tree = mondrian.insert(images, tree, 'c', 1000)
    print('### After insert c, images is', images)
    print('### After insert c, tree is', tree)

    images, tree = mondrian.insert(images, tree, 'd', 1000)
    print('### After insert d, images is', images)
    print('### After insert d, tree is', tree)

    mondrian.vertical_layout(images, tree, 1000)

    # FIXME this makes the test non-hermetic.
    images_list = [dataclasses.asdict(x) for x in images.values()]
    with open('layouts.js', 'w') as f:
      f.write(f'export const LAYOUT = {json.dumps(images_list)};')


if __name__ == '__main__':
  unittest.main()
