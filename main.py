from jinja2 import Template
from xhtml2pdf import pisa
from LicenceOCR import LicenseOCR, get_image
from UserDatabase import UserDatabase

import streamlit as st

model_ready = False
st.title('Vehicle Number OCR and Query System')
placeholder = st.empty()


@st.cache_resource
def load_model():
    processor = LicenseOCR()
    user_db = UserDatabase('license_plate_db.sqlite')
    user_db.add_license_details()
    return processor


def render_html_template(details):
    with open("template.html") as file:
        template = Template(file.read())
        return template.render(license_no=details[2], owner_name=details[3], vehicle_details=details[4],
                               registration_date=details[5],
                               owner_photo=details[7], address=details[6])


def generate_pdf_bytes(html_content):
    with open('results/license_details.pdf', "w+b") as res:
        pisa.CreatePDF(html_content, dest=res)
        res.seek(0)
        return res.read()


def main():
    placeholder.write("Loading Model, Please wait...")
    print("loading models")
    ocr_processor = load_model()
    db = UserDatabase('license_plate_db.sqlite')
    placeholder.write("Models Loaded successfully...")
    uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])
    if uploaded_file is not None:
        image_holder = st.image(uploaded_file, caption="Uploaded Image", use_column_width=True, width=100)
        placeholder.write("")
        with st.spinner('Processing image...'):
            src_img = get_image(uploaded_file)
            ocr_text = ocr_processor.ocr_image(src_img)
            print(ocr_text)
            result = db.get_user_details(ocr_text)
        placeholder.write("")
        image_holder.empty()
        if result:
            st.write(f"Recognized License Plate Number: {result[2]}")
            html_content = render_html_template(result)
            st.markdown(html_content, unsafe_allow_html=True)
            st.download_button(label="Download PDF", data=generate_pdf_bytes(html_content),
                                       file_name=f"license_details_{result[2]}.pdf",
                                       mime="application/octet-stream")


        else:
            st.write("No Information found for this License Plate")


if __name__ == "__main__":
    main()
