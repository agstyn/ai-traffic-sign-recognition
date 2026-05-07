import tensorflow as tf
import streamlit as st


@st.cache_resource
def load_model():
    return tf.keras.models.load_model(
        "models/traffic_sign_model.h5"
    )
