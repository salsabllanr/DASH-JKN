import requests
from datetime import datetime

# Konstanta URL API
API_URL = "https://salsabllanr-predict-sentimen.hf.space/predict"

def predict_sentiment(text):
    """
    Mengirim teks ke API untuk diprediksi sentimennya.
    Mengembalikan tuple (status, result).
    - status: True jika berhasil, False jika gagal.
    - result: Dictionary hasil prediksi jika berhasil, atau string pesan error jika gagal.
    """
    try:
        response = requests.post(API_URL, json={"content": text})
        response.raise_for_status()  # Akan memunculkan error untuk status code 4xx/5xx
        return True, response.json()
    except requests.exceptions.RequestException as e:
        return False, f"❌ Connection Error: {e}"
    except Exception as e:
        return False, f"❌ An unexpected error occurred: {e}"
