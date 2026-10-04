import requests

def send_message(message_text):
    # ضع التوكن الخاص بالبوت هنا (أو اسحبه من بيئة العمل)
    BOT_TOKEN = "8734357312:AAHrVjNLSpOM9fZGSjL94oLUi5odzsg2HDE"
    
    # ضع معرّف قناتك العامة أو الـ Chat ID الخاص بالقناة الخاصة هنا
    CHANNEL_ID = "-1003931694939" 
    
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
