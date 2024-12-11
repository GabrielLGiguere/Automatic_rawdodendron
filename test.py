import cv2
from cv2 import dnn_superres
from tkinter import filedialog

# Create an SR object
sr = dnn_superres.DnnSuperResImpl_create()

# Read image
file = filedialog.askopenfilename()
image = cv2.imread(file)

# Read the desired model
path = "FSRCNN_x2.pb"
sr.readModel(path)

# Set the desired model and scale to get correct pre- and post-processing
sr.setModel("edsr", 3)

# Upscale the image
result = sr.upsample(image)

# Save the image
cv2.imwrite("./upscaled.png", result)