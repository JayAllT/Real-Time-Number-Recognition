import os
import cv2
import numpy as np
from tensorflow import keras


def main():
    images = []
    labels = []

    # get images in data folder
    for num_dir in os.listdir("data"):
        for img in os.listdir(f"data/{num_dir}"):
            images.append(cv2.imread(f"data/{num_dir}/{img}"))

            labels.append(int(num_dir) - 1)

    # convert to grayscale values
    for idx, image in enumerate(images):
        images[idx] = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        images[idx] = images[idx] / 255.0

    # create model
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(32, 32)),
        keras.layers.Dense(128, activation="relu"),
        keras.layers.Dense(64, activation="relu"),
        keras.layers.Dense(9, activation="softmax")
    ])

    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    images = np.array(images)
    labels = np.array(labels)
    model.fit(images, labels, epochs=35)

    model.save("model.h5")


if __name__ == "__main__":
    main()
