import requests

def send_message(message_text):

    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
    
    # الرابط الرسمي لإرسال الرسائل عبر تليجرام API
    url = f"https://telegram.org{BOT_TOKEN}/sendMessage"
    
    # إعداد البيانات المرسلة (دعم صيغة HTML لتنسيق النصوص إن أردت)
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message_text,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        
        if result.get("ok"):
            print("[🚀] تم إرسال التقرير بنجاح إلى قناة تليجرام.")
        else:
            print(f"[-] فشل تليجرام في الإرسال: {result.get('description')}")
            
    except requests.exceptions.RequestException as e:
        print(f"[-] حدث خطأ في الاتصال بسيرفرات تليجرام: {e}")
