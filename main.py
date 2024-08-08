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
        placeholder.write("")
        image_holder.empty()
        if result:
            st.write(f"Recognized License plate number : {result[2]}")
            html_content = render_html_temp(result)
            st.markdown(html_content, unsafe_allow_html=True)
            st.download_button(label="Download PDF", data=generate_pdf(html_content), file_name=f"License_details_{result[2]}.pdf")

        else:
            st.write("No information found for this License plate")


if __name__ == "main":
    main()
