# -*- coding: utf-8 -*-
"""DR_75%_VGG16.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1a2XGLyL3_8ni8e6cfZy-IrnbJDI7zRWl
"""

import zipfile
zip_ref = zipfile.ZipFile('/content/train.zip', 'r')
zip_ref.extractall('/content')
zip_ref.close()

import shutil
import os

# Define source and destination paths
src_A = '/content/Mild'  # Change this to the path of folder A
src_B = '/content/Moderate'  # Change this to the path of folder B
src_C = '/content/No_DR'  # Change this to the path of folder A
src_D = '/content/Proliferate_DR'  # Change this to the path of folder B
src_E = '/content/Severe'  # Change this to the path of folder A

dest = '/content/train'  # Destination folder

# Create the destination folder if it doesn't exist
if not os.path.exists(dest):
    os.makedirs(dest)

# Move the A and B folders to the train folder
shutil.move(src_A, dest)
shutil.move(src_B, dest)
shutil.move(src_C, dest)
shutil.move(src_D, dest)
shutil.move(src_E, dest)


print("Folders moved successfully!")

import zipfile
zip_ref = zipfile.ZipFile('/content/test (1).zip', 'r')
zip_ref.extractall('/content')
zip_ref.close()

import shutil
import os

# Define source and destination paths
src_A = '/content/Mild'  # Change this to the path of folder A
src_B = '/content/Moderate'  # Change this to the path of folder B
src_C = '/content/No_DR'  # Change this to the path of folder A
src_D = '/content/Proliferate_DR'  # Change this to the path of folder B
src_E = '/content/Severe'  # Change this to the path of folder A

dest = '/content/test'  # Destination folder

# Create the destination folder if it doesn't exist
if not os.path.exists(dest):
    os.makedirs(dest)

# Move the A and B folders to the train folder
shutil.move(src_A, dest)
shutil.move(src_B, dest)
shutil.move(src_C, dest)
shutil.move(src_D, dest)
shutil.move(src_E, dest)


print("Folders moved successfully!")

import tensorflow
from tensorflow import keras
from keras import Sequential
from keras.layers import Dense,Flatten
from keras.applications.vgg16 import VGG16

conv_base = VGG16(
    weights='imagenet',
    include_top = False,
    input_shape=(150,150,3)
)

model = Sequential()

model.add(conv_base)
model.add(Flatten())
model.add(Dense(256,activation='relu'))
model.add(Dense(5,activation='softmax'))
model.build(input_shape=(None,150, 150, 3))

model.summary()

conv_base.trainable = False

# generators
train_ds = keras.utils.image_dataset_from_directory(
    directory = '/content/train',
    labels='inferred',
    label_mode = 'categorical',
    batch_size=32,
    image_size=(150,150)
)

validation_ds = keras.utils.image_dataset_from_directory(
    directory = '/content/test',
    labels='inferred',
    label_mode = 'categorical',
    batch_size=32,
    image_size=(150,150)
)

# Normalize
def process(image,label):
    image = tensorflow.cast(image/255. ,tensorflow.float32)
    return image,label

train_ds = train_ds.map(process)
validation_ds = validation_ds.map(process)

model.compile(optimizer='Adam',loss='categorical_crossentropy',metrics=['accuracy'])

history = model.fit(train_ds,epochs=10,validation_data=validation_ds)

import matplotlib.pyplot as plt

plt.plot(history.history['accuracy'],color='red',label='train')
plt.plot(history.history['val_accuracy'],color='blue',label='validation')
plt.legend()
plt.show()

plt.plot(history.history['loss'],color='red',label='train')
plt.plot(history.history['val_loss'],color='blue',label='validation')
plt.legend()
plt.show()

history = model.fit(train_ds,epochs=20,validation_data=validation_ds)

import matplotlib.pyplot as plt

plt.plot(history.history['accuracy'],color='red',label='train')
plt.plot(history.history['val_accuracy'],color='blue',label='validation')
plt.legend()
plt.show()

plt.plot(history.history['loss'],color='red',label='train')
plt.plot(history.history['val_loss'],color='blue',label='validation')
plt.legend()
plt.show()

fig1 = plt.gcf()
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.axis(ymin=0.4,ymax=1)
plt.grid()
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epochs')
plt.legend(['train', 'validation'])
plt.show()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.grid()
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epochs')
plt.legend(['train', 'validation'])
plt.show()

#model evaluation on training set
train_loss,train_accuracy = model.evaluate(train_ds)

print("Training Accuracy :",train_accuracy)
print("Training Loss :",train_loss)

#model evaluation on validation set
train_loss,train_accuracy = model.evaluate(validation_ds)

print("Validation Accuracy :",train_accuracy)
print("Validation Loss :",train_loss)

#saving model
model.save('/content/model.h5')

model.save('/content/model.keras')

history.history

#recording history in json
import json
with open('history.json', 'w') as f:
    json.dump(history.history, f)

# Print class names
class_names = train_ds.class_names
print("Class names in training set:", train_ds.class_names)
print("Class names in validation set:", validation_ds.class_names)

test_ds = keras.utils.image_dataset_from_directory(
    directory = '/content/test',
    labels='inferred',
    label_mode = 'categorical',
    batch_size=32,
    image_size=(150,150)
)

Pred = model.predict(test_ds)
Pred,Pred.shape

predicated_classes = tf.argmax(Pred, axis=1)
predicated_classes

true_classes = tf.concat([y for x, y in test_ds], axis=0)
true_classes

Y_true = tf.argmax(true_classes, axis=1)
Y_true

from sklearn.metrics import confusion_matrix, classification_report

print(classification_report(Y_true, predicated_classes,target_names=class_names))

import cv2
image=cv2.imread('/content/image_0_14.jpg')
image_resized= cv2.resize(image, (150,150))
image=np.expand_dims(image_resized,axis=0)
print(image.shape)
plt.imshow(image[0])

pred=model.predict(image)
print(pred)

output_class=class_names[np.argmax(pred)]
print("The predicted class is", output_class)