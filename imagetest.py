import cv2
import numpy as np
import pytesseract
from PIL import Image


def preprocess_image(image_path):
    # 이미지 읽기
    img = cv2.imread(image_path)
    
    # 그레이스케일로 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 노이즈 제거
    denoised = cv2.fastNlMeansDenoising(gray)
    
    # 대비 향상
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(denoised)
    
    # 이진화
    _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return binary

def extract_text(image):
    # Tesseract OCR을 사용하여 텍스트 추출
    text = pytesseract.image_to_string(image)
    return text

def main(image_path):
    # 이미지 전처리
    processed_image = preprocess_image(image_path)
    
    # 텍스트 추출
    extracted_text = extract_text(processed_image)
    
    print("추출된 텍스트:")
    print(extracted_text)
    
    # 추출된 텍스트에서 열차 번호와 시간 정보 찾기
    # 이 부분은 실제 이미지와 텍스트 형식에 따라 조정이 필요할 수 있습니다
    import re
    
    train_number = re.search(r'\b[A-Z0-9]+\b', extracted_text)
    date_time = re.search(r'\d{4}[-/]\d{2}[-/]\d{2}\s+\d{2}:\d{2}:\d{2}', extracted_text)
    
    if train_number and date_time:
        date_time_str = date_time.group().replace('-', '_').replace('/', '_').replace(' ', '_').replace(':', '_')
        flag = f"{date_time_str}_{train_number.group()}"
        print(f"플래그: {flag}")
    else:
        print("열차 번호 또는 날짜/시간을 찾을 수 없습니다.")

if __name__ == "__main__":
    image_path = "/Users/USER/Documents/study/DIMCTF/train.png"
    main(image_path)
