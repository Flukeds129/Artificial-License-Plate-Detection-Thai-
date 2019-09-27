import numpy as np
import os
import tensorflow as tf
from PIL import Image
import cv2
import test_Readplate
import time

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util


def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

def save_image(img_data2,count):
    img = img_data2
    filename2 = os.path.join(f'images{count}.JPG')
    cv2.imwrite(filename2,img)


cap = cv2.VideoCapture('http://192.168.43.1:8080/video')

MODEL_NAME = 'ssdlite_30000'
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
PATH_TO_LABELS = os.path.join('training', 'ssdlite','object-detection.pbtxt')
NUM_CLASSES = 1


detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')


label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(
		label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


with detection_graph.as_default():
  with tf.Session(graph=detection_graph) as sess:
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
    while True:
        for i in range(10):
           cap.grab()
        ret, image_np = cap.read()
        image_np_expanded = np.expand_dims(image_np, axis=0)
        (boxes, scores, classes, num) = sess.run(
			[detection_boxes, detection_scores, detection_classes, num_detections]
			,feed_dict={image_tensor: image_np_expanded})
        
        vis_util.visualize_boxes_and_labels_on_image_array(
           image_np,
           np.squeeze(boxes),
           np.squeeze(classes).astype(np.int32),
           np.squeeze(scores),
           category_index,
           use_normalized_coordinates=True,
           line_thickness=5)
        cv2.imshow('numplate detection', image_np)
        if cv2.waitKey(1) == ord('q'):
           cv2.destroyAllWindows()
           break
        if os.path.isfile('frame1.jpg'):
           count=1
           image = Image.open('frame1.jpg') 
           image_detect = load_image_into_numpy_array(image)
           ymin = boxes[0,0,0]
           xmin = boxes[0,0,1]
           ymax = boxes[0,0,2]
           xmax = boxes[0,0,3]
           (im_width, im_height) = image.size
           (xminn, xmaxx, yminn, ymaxx) = (xmin * im_width, xmax * im_width, ymin * im_height, ymax * im_height)
           cropped_image = tf.image.crop_to_bounding_box(image_detect, int(yminn), int(xminn),int(ymaxx - yminn), int(xmaxx - xminn))
           img_data = sess.run(cropped_image)
           filename = save_image(img_data,count)
           test_Readplate.main(count)
           os.remove('frame0.jpg')
           os.remove('frame1.jpg')
           time.sleep(1.5)
