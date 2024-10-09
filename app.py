from flask import Flask, request, jsonify
import os
import requests
import shutil
from urllib.parse import urlparse

app = Flask(__name__)

# توكن بوت التليجرام
TELEGRAM_BOT_TOKEN = "7628474532:AAHLQxj2lbrrlcR4j1wjcmFlbWzQtZ4JnsY"
# معرف الدردشة (يمكنك الحصول عليه من رسالة جديدة في البوت)
CHAT_ID = "1051175859"

# المجلد الذي سيتم حفظ المواقع فيه
OUTPUT_DIR = "/path/to/save/websites"

@app.route('/download', methods=['POST'])
def download_website():
    """تحميل موقع بناءً على URL المدخل."""
    data = request.json
    website_url = data.get("url")
    
    if not website_url:
        return jsonify({"error": "يرجى تقديم رابط صالح."}), 400
    
    folder_name = urlparse(website_url).netloc
    full_output_path = os.path.join(OUTPUT_DIR, folder_name)

    if download_website(website_url, full_output_path):
        zip_file_path = zip_directory(full_output_path)
        send_file_to_telegram(zip_file_path)
        return jsonify({"message": "تم تحميل الموقع وضغطه بنجاح!", "file": zip_file_path}), 200
    else:
        return jsonify({"error": "حدث خطأ أثناء تحميل الموقع."}), 500

def download_website(website_url: str, output_dir: str) -> bool:
    """تحميل محتوى الموقع وحفظه في مجلد."""
    try:
        response = requests.get(website_url)
        response.raise_for_status()  # تحقق من نجاح الطلب

        # احفظ المحتوى في ملف HTML
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as file:
            file.write(response.text)
        
        return True
    except Exception as e:
        print(f"حدث خطأ: {e}")
        return False

def zip_directory(directory: str) -> str:
    """ضغط المجلد وتحويله إلى ملف ZIP."""
    zip_name = directory + '.zip'
    shutil.make_archive(directory, 'zip', directory)
    return zip_name

def send_file_to_telegram(file_path: str):
    """إرسال ملف إلى تيليجرام."""
    with open(file_path, 'rb') as file:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument", 
                      data={'chat_id': CHAT_ID}, 
                      files={'document': file})

if __name__ == '__main__':
    app.run(debug=True)
