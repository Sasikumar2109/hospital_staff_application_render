from dotenv import load_dotenv
import os
import base64
import requests

load_dotenv()

machine = os.getenv("MACHINE")
bucket_name = os.getenv("BUCKET_NAME")

photo1_path = "data/optimized_association_photos/photo1.JPG"
photo2_path = "data/optimized_association_photos/photo2.JPG"
photo3_path = "data/optimized_association_photos/photo3.JPG"
photo4_path = "data/optimized_association_photos/photo4.JPG"
photo5_path = "data/optimized_association_photos/photo5.JPG"
photo6_path = "data/optimized_association_photos/photo6.JPG"
photo7_path = "data/optimized_association_photos/photo7.JPG"
photo8_path = "data/optimized_association_photos/photo8.jpg"
photo9_path = "data/optimized_association_photos/photo9.JPG"
photo10_path = "data/optimized_association_photos/photo10.JPG"

logo_path = 'data/icons/logo.png'
hospital_symbol_path = 'data/icons/hospital_symbol.png'
sub_sign_path = 'uploads/signature'
sub_photo_path = 'uploads/photo'
sub_rnrm_path = 'uploads/rnrm'
sub_aadhar_path = 'uploads/aadhar'
sub_term_path = 'data/documents/terms_and_conditions'


if machine=="local":
    photo1 = photo1_path
    photo2 = photo1_path
    photo3 = photo1_path
    photo4 = photo1_path
    photo5 = photo1_path
    photo6 = photo1_path
    photo7 = photo1_path
    photo8 = photo1_path
    photo9 = photo1_path
    photo10 = photo1_path
else:
    photo1 = f"https://storage.googleapis.com/{bucket_name}/{photo1_path}"
    photo2 = f"https://storage.googleapis.com/{bucket_name}/{photo2_path}"
    photo3 = f"https://storage.googleapis.com/{bucket_name}/{photo3_path}"
    photo4 = f"https://storage.googleapis.com/{bucket_name}/{photo4_path}"
    photo5 = f"https://storage.googleapis.com/{bucket_name}/{photo5_path}"
    photo6 = f"https://storage.googleapis.com/{bucket_name}/{photo6_path}"
    photo7 = f"https://storage.googleapis.com/{bucket_name}/{photo7_path}"
    photo8 = f"https://storage.googleapis.com/{bucket_name}/{photo8_path}"
    photo9 = f"https://storage.googleapis.com/{bucket_name}/{photo9_path}"
    photo10 = f"https://storage.googleapis.com/{bucket_name}/{photo10_path}"



if machine=='local':
    logo_path = logo_path
    hospital_symbol_path = hospital_symbol_path
    logo_base64 = base64.b64encode(open(logo_path, 'rb').read()).decode()
    symbol_base64 = base64.b64encode(open(hospital_symbol_path, 'rb').read()).decode()
else:
    logo_path = f"https://storage.googleapis.com/{bucket_name}/{logo_path}"
    hospital_symbol_path = f"https://storage.googleapis.com/{bucket_name}/{hospital_symbol_path}"
    logo_base64 = base64.b64encode(requests.get(logo_path).content).decode()
    symbol_base64 = base64.b64encode(requests.get(hospital_symbol_path).content).decode()