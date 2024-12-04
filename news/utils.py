from kavenegar import KavenegarAPI, APIException, HTTPException

def send_sms(phone_number, message):
    """
    ارسال پیامک با استفاده از سرویس کاوه‌نگار
    :param phone_number: شماره تلفن مقصد
    :param message: متن پیامک
    :return: پاسخ API
    """
    try:
        api = KavenegarAPI('5A526F323961334F783863366A72537149675954337A565257322B744E6850654C32392F3650377A71594D3D')
        params = {
            'receptor': "09227207457", 
            'sender': '1000596446', 
            'message': "salaaam", 
        }

        response = api.sms_send(params)
        return response

    except APIException as e:
        print(f"API Exception: {e}")  
        return None

    except HTTPException as e:
        print(f"HTTP Exception: {e}")
        return None
