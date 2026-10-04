import secrets
import string
import os
import glob

from notifier import send_message

def generate_app_code():
    characters = string.ascii_uppercase + string.digits
    part1 = ''.join(secrets.choice(characters) for _ in range(4))
    part2 = ''.join(secrets.choice(characters) for _ in range(4))
    part3 = ''.join(secrets.choice(characters) for _ in range(4))
    return f"{part1}-{part2}-{part3}"

# تحديد الفولدر الذي ستُحفظ فيه الأكواد داخل الجيت هاب
output_folder = "generated_vault"
os.makedirs(output_folder, exist_ok=True)

# 1. قراءة كافة الأكواد السابقة من جميع الملفات لمنع التكرار وحساب السطور
existing_codes = set()
all_files = glob.glob(os.path.join(output_folder, "codes_part_*.txt"))

print("[+] جاري قراءة الملفات السابقة من المستودع لحساب السطور ومنع التكرار...")
for file_path in all_files:
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            code = line.strip()
            if code:
                existing_codes.add(code)

total_lines_saved = len(existing_codes)
print(f"[📊] إجمالي عدد السطور (الأكواد المستخرجة سابقاً): {total_lines_saved} سطر.")
print("="*60)

# تحديد رقم الجزء الحالي بناءً على الملفات الموجودة
part_number = len(all_files) if len(all_files) > 0 else 1
current_file_path = os.path.join(output_folder, f"codes_part_{part_number}.txt")

# حساب كم سطر موجود في الملف الحالي
current_file_lines = 0
if os.path.exists(current_file_path):
    with open(current_file_path, "r", encoding="utf-8") as f:
        current_file_lines = sum(1 for l in f)

print(f"[*] جاري البدء في التوليد المستمر... الملف الحالي: codes_part_{part_number}.txt وفيه {current_file_lines} سطر.")

# الدوران والتوليد المستمر (سيغلقه جيت هاب تلقائياً بعد 6 ساعات)
try:
    file_handler = open(current_file_path, "a", encoding="utf-8")
    
    while True:
        new_code = generate_app_code()
        
        if new_code not in existing_codes:
            existing_codes.add(new_code)
            file_handler.write(f"{new_code}\n")
            current_file_lines += 1
            total_lines_saved += 1
            
            # طباعة إحصائية كل 50,000 كود في الـ Logs الخاصة بجيت هاب
            if total_lines_saved % 50000 == 0:
                print(f"[+] تم الوصول إلى {total_lines_saved} سطر إجمالي...")

            # 🛑 استراتيجية التقسيم الذكي: إذا وصل الملف الحالي لـ 1,000,000 سطر، اقفله وافتح جزء جديد
            if current_file_lines >= 1000000:
                file_handler.close()
                print(f"[💾] الملف الحالي وصل لمليون سطر. جاري الانتقال للجزء التالي...")
                part_number += 1
                current_file_path = os.path.join(output_folder, f"codes_part_{part_number}.txt")
                file_handler = open(current_file_path, "a", encoding="utf-8")
                current_file_lines = 0

except KeyboardInterrupt:
    print("\n[!] تم الإيقاف.")
finally:
    if 'file_handler' in locals() and not file_handler.closed:
        file_handler.close()
    send_message(f"[🎉] انتهت جلسة اليوم. إجمالي السطور النهائي في المستودع: {total_lines_saved} سطر.")
    print(f"[🎉] انتهت جلسة اليوم. إجمالي السطور النهائي في المستودع: {total_lines_saved} سطر.")
