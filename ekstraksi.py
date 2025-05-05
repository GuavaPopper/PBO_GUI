from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
import cv2
import numpy as np

# SET PATH TESSERACT DI SINI
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

class EkstraksiTeks:
    def ekstrak(self, path_gambar):
        try:
            # Buka gambar dengan PIL
            pil_img = Image.open(path_gambar)
            
            # Convert ke OpenCV format untuk preprocessing lebih baik
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            
            # Preprocessing untuk meningkatkan akurasi
            # 1. Convert ke grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # 2. Apply thresholding - adaptive lebih baik untuk dokumen/teks
            thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                          cv2.THRESH_BINARY, 11, 2)
            
            # 3. Noise removal
            denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
            
            # 4. Sharpen
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            sharpened = cv2.filter2D(denoised, -1, kernel)
            
            # 5. Convert kembali ke PIL (Tesseract dengan pytesseract lebih suka PIL)
            enhanced_img = Image.fromarray(sharpened)
            
            # Ukuran asli
            orig_width, orig_height = enhanced_img.size
            
            # 6. Jika ukuran terlalu kecil, resize (opsional, tergantung gambar)
            if orig_width < 1000 or orig_height < 1000:
                scale_factor = 2.0  # Coba scale 2x untuk gambar kecil
                enhanced_img = enhanced_img.resize((int(orig_width*scale_factor), 
                                                  int(orig_height*scale_factor)), 
                                                 Image.LANCZOS)
            
            # Ekstraksi dengan beberapa config Tesseract tambahan
            custom_config = r'--oem 3 --psm 6 -l eng+ind'  # PSM 6 untuk blok text
            
            # Coba beberapa PSM mode dan pilih hasil terbaik
            hasil = ""
            psm_modes = [6, 3, 4, 11]  # Mode untuk berbagai tipe dokumen
            
            for psm in psm_modes:
                config = f'--oem 3 --psm {psm} -l eng+ind'
                text = pytesseract.image_to_string(enhanced_img, config=config)
                # Jika hasil cukup bagus, gunakan
                if len(text.strip()) > len(hasil.strip()):
                    hasil = text
            
            return hasil.strip()
            
        except Exception as e:
            return f"Error ekstraksi: {e}"
