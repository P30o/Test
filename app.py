from flask import Flask, request, jsonify
import os
import subprocess
import shutil
from urllib.parse import urlparse

app = Flask(__name__)

# توكن بوت التليجرام
TELEGRAM_BOT_TOKEN = "7628474532:AAHLQxj2lbrrlcR4j1wjcmFlbWzQtZ4JnsY"

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

    if download_website_with_wget(website_url, full_output_path):
        zip_file_path = zip_directory(full_output_path)
        return jsonify({"message": "تم تحميل الموقع وضغطه بنجاح!", "file": zip_file_path}), 200
    else:
        return jsonify({"error": "حدث خطأ أثناء تحميل الموقع."}), 500

def download_website_with_wget(website_url: str, output_dir: str) -> bool:
    """تنفيذ wget لتحميل الموقع."""
    command = [
        'wget',
        '--mirror',
        '--convert-links',
        '--adjust-extension',
        '--page-requisites',
        '--no-parent',
        '--directory-prefix=' + output_dir,
        website_url
    ]

    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def zip_directory(directory: str) -> str:
    """ضغط المجلد وتحويله إلى ملف ZIP."""
    zip_name = directory + '.zip'
    shutil.make_archive(directory, 'zip', directory)
    return zip_name

if __name__ == '__main__':
    app.run(debug=True)
