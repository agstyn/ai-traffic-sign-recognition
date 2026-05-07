import os
import base64
import streamlit as st

from PIL import Image
from io import BytesIO


@st.cache_data
def load_class_images():

    train_path = "data/GTSRB/Final_Training/Images"

    folders = sorted(os.listdir(train_path))

    result = {}

    for idx, folder in enumerate(folders):

        fp = os.path.join(train_path, folder)

        imgs = [
            f for f in os.listdir(fp)
            if f.endswith(".ppm")
        ]

        if imgs:
            result[idx] = os.path.join(
                fp,
                imgs[len(imgs)//2]
            )

    return result


def to_b64(pil, size=(190, 190)):

    pil = pil.resize(size, Image.LANCZOS)

    buf = BytesIO()

    pil.save(buf, format="PNG")

    return base64.b64encode(
        buf.getvalue()
    ).decode()
