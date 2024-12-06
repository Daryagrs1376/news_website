from flask import Flask, request, jsonify
from sms_service import send_sms  # وارد کردن تابع ارسال پیامک
import random

app = Flask(__name__)

# اینجا می‌توانید تنظیمات دیگر مانند اتصال به دیتابیس یا Redis را اضافه کنید

@app.route('/send-code', methods=['POST'])
def send_verification_code():
    data = request.json
    phone_number = data.get('phone_number')

    if not phone_number:
        return jsonify({"error": "شماره موبایل الزامی است"}), 400

    # تولید کد تصادفی
    verification_code = random.randint(1000, 9999)

    # ارسال پیامک
    send_sms(phone_number, verification_code)

    # اینجا می‌توانید کد را در دیتابیس یا Redis ذخیره کنید
    # به عنوان مثال:
    # db.save_verification_code(phone_number, verification_code)

    return jsonify({"message": "کد تایید ارسال شد!"})

if __name__ == "__main__":
    app.run(debug=True)
