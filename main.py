from jinja2 import template
from xhtml2pdf import pisa
from LicenseOCR import LicenseOCR, get_image
from UserDatabase import UserDatabase

import streamlit as st

model_ready = false
st.title('Vehicle Number OCR and Query System')
placeholder = st.empty()

def load_model():
    processor = LicenseOCR()
