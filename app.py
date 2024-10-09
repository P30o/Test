from flask import Flask, request, jsonify
import os
import requests
import shutil
from urllib.parse import urlparse
import urllib.parse

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

    if download_website_content(website_url, full_output_path):
        zip_file_path = zip_directory(full_output_path)
        send_file_to_telegram(zip_file_path)
        return jsonify({"message": "تم تحميل الموقع وضغطه بنجاح!", "file": zip_file_path}), 200
    else:
        return jsonify({"error": "حدث خطأ أثناء تحميل الموقع."}), 500

def download_website_content(website_url: str, output_dir: str) -> bool:
    """تحميل محتوى الموقع وحفظه في مجلد."""
    try:
        # احفظ ملف HTML الرئيسي
        response = requests.get(website_url)
        response.raise_for_status()

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as file:
            file.write(response.text)

        # استخدم BeautifulSoup لتحميل الموارد الأخرى
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(response.text, 'html.parser')

        # تحميل جميع الروابط من HTML
        resources = []

        for tag in soup.findAll(['link', 'script', 'img']):
            if tag.name == 'link' and 'href' in tag.attrs:
                resources.append(tag['href'])
            elif tag.name == 'script' and 'src' in tag.attrs:
                resources.append(tag['src'])
            elif tag.name == 'img' and 'src' in tag.attrs:
                resources.append(tag['src'])

        # تحميل كل مورد وحفظه
        for resource in resources:
            resource_url = urllib.parse.urljoin(website_url, resource)
            resource_name = os.path.basename(resource)

            resource_response = requests.get(resource_url)
            resource_response.raise_for_status()

            with open(os.path.join(output_dir, resource_name), 'wb') as resource_file:
                resource_file.write(resource_response.content)

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

@app.route('/webhook', methods=['POST'])
def webhook():
    """التعامل مع الرسائل المستلمة من تيليجرام."""
    data = request.json

    # تأكد من أن الرسالة تحتوي على نص
    if 'message' in data and 'text' in data['message']:
        message_text = data['message']['text']
        chat_id = data['message']['chat']['id']

        # تحقق من وجود الأمر /start
        if message_text == '/start':
            send_message(chat_id, "مرحبًا بك في البوت! أرسل رابطًا لتحميل الموقع.")
        
        # تحقق من وجود رابط
        elif message_text.startswith("http://") or message_text.startswith("https://"):
            url = message_text
            website_url = {"url": url}
            download_website()  # استدعاء الدالة لتحميل الموقع
            
            send_message(chat_id, "تم إرسال الطلب لتحميل الموقع.")
        else:
            send_message(chat_id, "يرجى إرسال رابط صحيح.")

    return jsonify({"status": "ok"}), 200

def send_message(chat_id, text):
    """إرسال رسالة إلى تيليجرام."""
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", 
                  data={'chat_id': chat_id, 'text': text})

if __name__ == '__main__':
    app.run(debug=True)
