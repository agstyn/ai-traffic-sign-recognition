import cv2
import numpy as np
import tensorflow as tf

from PIL import Image


def make_gradcam(model, pil_img):

    try:

        last_conv_idx = None

        for i, layer in enumerate(model.layers):

            if isinstance(layer, tf.keras.layers.Conv2D):
                last_conv_idx = i

        if last_conv_idx is None:
            return None, None

        conv_layer = model.layers[last_conv_idx]

        conv_model = tf.keras.Model(
            inputs=model.inputs,
            outputs=conv_layer.output
        )

        remain_input = tf.keras.Input(
            shape=conv_layer.output.shape[1:]
        )

        x = remain_input

        for layer in model.layers[last_conv_idx + 1:]:
            x = layer(x)

        head_model = tf.keras.Model(
            inputs=remain_input,
            outputs=x
        )

        img_arr = np.array(
            pil_img.resize((32, 32))
        ) / 255.0

        img_input = tf.cast(
            np.expand_dims(img_arr, axis=0),
            tf.float32
        )

        with tf.GradientTape() as tape:

            conv_out = conv_model(img_input)

            tape.watch(conv_out)

            preds = head_model(conv_out)

            top_idx = tf.argmax(preds[0])

            loss = preds[:, top_idx]

        grads = tape.gradient(loss, conv_out)

        pooled = tf.reduce_mean(
            grads,
            axis=(0, 1, 2)
        )

        cam = tf.reduce_sum(
            tf.multiply(pooled, conv_out[0]),
            axis=-1
        ).numpy()

        cam = np.maximum(cam, 0)

        if cam.max() > 0:
            cam = cam / cam.max()

        cam_up = cv2.resize(cam, (200, 200))

        heatmap_bgr = cv2.applyColorMap(
            np.uint8(255 * cam_up),
            cv2.COLORMAP_JET
        )

        heatmap_rgb = cv2.cvtColor(
            heatmap_bgr,
            cv2.COLOR_BGR2RGB
        )

        orig = np.array(
            pil_img.resize((200, 200))
        )

        blended = cv2.addWeighted(
            orig,
            0.45,
            heatmap_rgb,
            0.55,
            0
        )

        return (
            Image.fromarray(heatmap_rgb),
            Image.fromarray(blended)
        )

    except Exception:
        return None, None
