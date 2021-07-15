!git clone https://github.com/fizyr/keras-retinanet.git

!pip install .

!python setup.py build_ext --inplace

# !pip install keras==2.3.1
# !pip install tensorflow==2.1.0

import numpy as np
import matplotlib.pyplot as plt
import requests
import urllib
import os
from PIL import Image

from keras_retinanet import models
from keras_retinanet.utils.image import preprocess_image, resize_image
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color

# https://github.com/fizyr/keras-retinanet/releases
urllib.request.urlretrieve(
    'https://github.com/fizyr/keras-retinanet/releases/download/0.5.1/resnet50_coco_best_v2.1.0.h5',
    'pretrained_model.h5')

model = models.load_model('pretrained_model.h5')

#This pretrained model
class_names = [l.rstrip() for l in open('coco_categories.txt')]
class_names

def show_image_with_predictions(img_path, threshold=0.6):
  im = np.array(Image.open(img_path))
  print("im.shape:", im.shape)

  # if there's a PNG it will have alpha channel. This is an extra dimension
  #that will not be accepted by the

  im = im[:,:,:3]

  ### plot predictions ###

  # get predictions
  imp = preprocess_image(im)
  imp, scale = resize_image(im)

  boxes, scores, labels = model.predict_on_batch(
    np.expand_dims(imp, axis=0)
  )

  # standardize box coordinates
  boxes /= scale

  # loop through each prediction for the input image
  for box, score, label in zip(boxes[0], scores[0], labels[0]):
    # scores are sorted so we can quit as soon
    # as we see a score below threshold
    if score < threshold:
      break

    box = box.astype(np.int32)
    color = label_color(label)
    draw_box(im, box, color=color)

    class_name = class_names[label]
    caption = f"{class_name} {score:.3f}"
    draw_caption(im, box, caption)

  plt.axis('off')
  plt.imshow(im)
  plt.show()

plt.rcParams['figure.figsize'] = [20, 10]


show_image_with_predictions('test_image1.jpg', threshold=0.2)

show_image_with_predictions('test_image2.jpg')

show_image_with_predictions('test_image3.jpg')

show_image_with_predictions('test_image4.jpg')
