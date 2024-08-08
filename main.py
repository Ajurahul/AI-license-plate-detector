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
    placeholder.write("Loadimg model. please wait....")
    print("loading models")
    ocr_processor = load_model()
    db = UserDatabase('license_details.sqlite')
    placeholder.write("Models loaded successfully")
    uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])
    if uploaded_file:
        image_holder = st.image(uploaded_file, caption="uploaded Image", use_column_width=True, width=100)
        placeholder.write("")
        with st.spinner("Processing Image"):
            src_img = get_image(uploaded_file)
            ocr_text = ocr_processor.ocr_image(src_img)
            print(ocr_text)
            result = db.get_user_details(ocr_text)
            print("Result"+result)


if __name__ == "main":
    main()
