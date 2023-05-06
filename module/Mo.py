import tensorflow as tf
import tensorflow_hub as hub


def predict_image_class(img_pa):
    model = tf.keras.models.load_model(("model.h5"), custom_objects={
                                       'KerasLayer': hub.KerasLayer})
    img = tf.keras.preprocessing.image.load_img(img_pa, target_size=(299, 299))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = tf.expand_dims(img, 0)  # Create a batch
    img = tf.keras.applications.inception_v3.preprocess_input(img)
    img = tf.image.convert_image_dtype(img, tf.float32)
    predictions = model.predict(img)
    score = predictions.squeeze()
    if score >= 0.6:
        return (f"This image is maybe {100 * score:.2f}% Safe.")
    else:
        return (f"This image is {100 * (1 - score):.2f}% infected.")
