from kavenegar import *
from kavenegar import KavenegarAPI, APIException, HTTPException


def send_sms(phone_number, verification_code):
    try:
        api = KavenegarAPI('Your-API-Key')  # کلید API کاوه‌نگار
        params = {
            'receptor': phone_number,  # شماره موبایل گیرنده
            'message': f'کد تایید شما: {verification_code}',  # متن پیامک
        }
        response = api.sms_send(params)
        print(f"SMS Response: {response}")
    except APIException as e:
        print(f"API Exception: {e}")
    except HTTPException as e:
        print(f"HTTP Exception: {e}")
