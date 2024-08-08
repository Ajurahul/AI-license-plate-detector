from jinja2 import Template
from xhtml2pdf import pisa
from LicenseOCR import LicenseOCR, get_image
from UserDatabase import UserDatabase

import streamlit as st

model_ready = False
st.title('Vehicle Number OCR and Query System')
placeholder = st.empty()


def load_model():
    processor = LicenseOCR()
    user_db = UserDatabase('license_details.sqlite')
    user_db.add_license_details()
    return processor


def render_html_temp():
    pass


def generate_pdf():
    pass


def main():
    pass


if __name__ == "main":
    main()
