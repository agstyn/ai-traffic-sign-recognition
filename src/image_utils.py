import os
import base64
import streamlit as st

from PIL import Image
from io import BytesIO


@st.cache_data
def load_class_images():

    result = {}

    for i in range(43):

        img_path = f"assets/class_images/{i}.ppm"

        if os.path.exists(img_path):
            result[i] = img_path

    return result


def to_b64(pil, size=(190, 190)):

    pil = pil.resize(size, Image.LANCZOS)

    buf = BytesIO()

    pil.save(buf, format="PNG")

    return base64.b64encode(
        buf.getvalue()
    ).decode()
