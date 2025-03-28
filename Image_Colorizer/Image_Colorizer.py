import numpy as np
import cv2

"""
------------------------------------------------------------------------------

A small project that is an image colorizer
this project transforms black and white photos into vibrant color images
Using a pre-trained deep learning model and OpenCV

-------------------------------------------------------------------------------
Path to needed file

- Points: https://github.com/richzhang/colorization/blob/caffe/colorization/resources/pts_in_hull.npy

- Models:  https://www.dropbox.com/scl/fi/d8zffur3wmd4wet58dp9x/colorization_release_v2.caffemodel?rlkey=iippu6vtsrox3pxkeohcuh4oy&e=1&dl=0
(the model file used to be in the github, but it got deleted)

- Prototxt: https://github.com/richzhang/colorization/blob/caffe/colorization/models/colorization_deploy_v2.prototxt

"""

# Paths to model files and input image
prototxt_path = 'models\colorization_deploy_v2.prototxt'
model_path = 'models\colorization_release_v2.caffemodel'
kernel_path = 'models\pts_in_hull.npy'
image_path = 'input_image\leopard.jpg'

# 1. Load the pre-trained colorization model
net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

# Load and set cluster centers
points = np.load(kernel_path)
points = points.transpose().reshape(2, 313, 1, 1)
net.getLayer(net.getLayerId("class8_ab")).blobs = [points.astype(np.float32)]
net.getLayer(net.getLayerId("conv8_313_rh")).blobs = [np.full([1,313], 2.606, dtype="float32")]

# 2. Prepare the input image (convert to LAB, resize, extract L)
bw_image = cv2.imread(image_path)
normalized = bw_image.astype("float32") / 255.0
lab = cv2.cvtColor(normalized, cv2.COLOR_BGR2LAB)
resized = cv2.resize(lab, (224, 224))
L = cv2.split(resized)[0]
L -= 50

# 3. Run the model to predict ab channels
net.setInput(cv2.dnn.blobFromImage(L))
ab = net.forward()[0, :, :, :].transpose((1,2,0))

# 4. Combine L and predicted ab channels
ab = cv2.resize(ab, (bw_image.shape[1], bw_image.shape[0]))
L = cv2.split(lab)[0]
colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)

# Convert back to BGR and denormalize
colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
colorized = (255.0 * colorized).astype("uint8")

# 5. Display original and colorized images
cv2.imshow("BW Image", bw_image)
cv2.imshow("Colorized", colorized)
cv2.waitKey(0)
cv2.destroyAllWindows()
