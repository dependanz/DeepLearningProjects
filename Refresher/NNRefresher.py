import tensorflow as tf
from tensorflow import keras

import numpy as np
import matplotlib.pyplot as plt

#dataset
(train_images, train_labels), (test_images, test_labels) = keras.datasets.fashion_mnist.load_data()
#numpy arrays

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

#scaling pixel values between 0 to 1, divide values by 255
train_images = train_images/255.0
test_images = test_images/255.0

#layers of network (784->128->10) for 10 types of clothes
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28,28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10)
])

#compile model
#loss function
#optimizer
#metrics - used to monitor training and testing steps
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

#train model
#feed the model (model.fit()) fits the model to training data
model.fit(train_images,train_labels, epochs=10)

#evaluate accuracy
test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
print('\nTest Accuracy: ', test_acc)

#make predictions
probability_model = tf.keras.Sequential([model,
                                         tf.keras.layers.Softmax()])
predictions = probability_model.predict(test_images)

#confirm predictions (plot)
plt.grid(False)
plt.xticks([])
plt.yticks([])

plt.imshow(test_images[0])
predicted_label = np.argmax(predictions[0])
color = 'blue' if predicted_label == test_labels[0] else 'red'
plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                100*np.max(predictions[0]),
                                class_names[test_labels[0]]),
                                color=color)
plt.show()

#using hte trained model
img = test_images[1]
#keras models are optimized to make predictions on a batch of examples
#this means we need to add our (28,28) image to a list (1,28,28)
img = (np.expand_dims(img,0))

prediction = probability_model.predict(img)

plt.imshow(test_images[1])
predicted_label = np.argmax(prediction[0])
color = 'blue' if predicted_label == test_labels[1] else 'red'
plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                100*np.max(prediction[0]),
                                class_names[test_labels[1]]),
                                color=color)
plt.show()