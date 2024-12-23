#!/usr/bin/env python3

# borrowed from https://keras.io/examples/vision/image_classification_from_scratch/


import keras
from keras import layers
import os
import matplotlib.pyplot as plt


batch_size = 32
epochs = 25
image_size = (167, 167)
base_dir = "/Users/taylorhogan/Documents/goodchip/generated_images"

def make_model(input_shape, num_classes):
    inputs = keras.Input(shape=input_shape)

    # Entry block
    x = layers.Rescaling(1.0 / 255)(inputs)
    x = layers.Conv2D(128, 3, strides=2, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    previous_block_activation = x  # Set aside residual

    for size in [256, 512, 728]:
        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.MaxPooling2D(3, strides=2, padding="same")(x)

        # Project residual
        residual = layers.Conv2D(size, 1, strides=2, padding="same")(
            previous_block_activation
        )
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x  # Set aside next residual

    x = layers.SeparableConv2D(1024, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    x = layers.GlobalAveragePooling2D()(x)
    if num_classes == 2:
        units = 1
    else:
        units = num_classes

    x = layers.Dropout(0.25)(x)
    # We specify activation=None so as to return logits
    outputs = layers.Dense(units, activation=None)(x)
    return keras.Model(inputs, outputs)


#
# Make the model
#

def train_model():

    model = make_model(input_shape=image_size + (3,), num_classes=2)
    keras.utils.plot_model(model, show_shapes=True)

    print("training")


    train_dataset, validation_dataset = keras.utils.image_dataset_from_directory(
        base_dir,
        validation_split=0.2,
        subset="both",
        seed=1337,
        image_size=image_size,
        batch_size=batch_size
    )

    callbacks = [
        keras.callbacks.ModelCheckpoint("save_at_{epoch}.keras"),
    ]

    model.compile(
        optimizer=keras.optimizers.Adam(3e-4),
        loss=keras.losses.BinaryCrossentropy(from_logits=True),
        metrics=[keras.metrics.BinaryAccuracy(name="acc")],
    )
    history = model.fit(
        train_dataset,
        epochs=epochs,
        callbacks=callbacks,
        validation_data=validation_dataset,
    )
    keras.models.save_model(model, "convnet_from_scratch.keras")

    test_model = keras.models.load_model("convnet_from_scratch.keras")
    test_loss, test_acc = test_model.evaluate(train_dataset)
    print(f"Test accuracy: {test_acc:.3f}")

# evaluating model on test data
def eval_model ():
    model = keras.models.load_model("convnet_from_scratch.keras")
    bad_image_path = os.path.join(base_dir, "bad/t1.png")

    img = keras.utils.load_img(bad_image_path, target_size=image_size)
    plt.imshow(img)

    img_array = keras.utils.img_to_array(img)
    img_array = keras.ops.expand_dims(img_array, 0)  # Create batch axis

    predictions = model.predict(img_array)
    score = float(keras.ops.sigmoid(predictions[0][0]))
    print(f"This image is {100 * (1 - score):.2f}% Bad and {100 * score:.2f}% Good.")

    good_image_path = os.path.join(base_dir, "good/t0.png")

    img = keras.utils.load_img(good_image_path, target_size=image_size)
    plt.imshow(img)

    img_array = keras.utils.img_to_array(img)
    img_array = keras.ops.expand_dims(img_array, 0)  # Create batch axis

    predictions = model.predict(img_array)
    score = float(keras.ops.sigmoid(predictions[0][0]))
    print(f"This image is {100 * (1 - score):.2f}% Bad and {100 * score:.2f}% Good.")

if __name__ == "__main__":
    train_model()
    eval_model()



