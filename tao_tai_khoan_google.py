import time
import random
import string
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import json
from datetime import datetime
import unicodedata

class GoogleAccountCreator:
    def __init__(self):
        self.drivers = []
        self.accounts_data = []
        
    def remove_accents(self, text):
        """Loại bỏ dấu tiếng Việt"""
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ascii', 'ignore')
        text = text.decode("utf-8")
        return text
    
    def generate_random_name(self):
        """Tạo họ và tên ngẫu nhiên"""
        first_names = ["An", "Binh", "Chi", "Dung", "Giang", "Hanh", "Khang", "Linh", "Minh", "Nga", "Hoa", "Lan", "Mai", "Phuong", "Quynh"]
        last_names = ["Nguyen", "Tran", "Le", "Pham", "Hoang", "Phan", "Vu", "Dang", "Bui", "Do", "Ngo", "Duong", "Ly", "Doan", "Truong"]
        return random.choice(first_names), random.choice(last_names)
    
    def generate_random_birthdate(self):
        """Tạo ngày tháng năm sinh ngẫu nhiên (trên 18 tuổi)"""
        year = random.randint(1960, 2005)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return day, month, year
    
    def generate_random_password(self):
        """Tạo mật khẩu ngẫu nhiên theo định dạng: 2 chữ in hoa - 6 chữ thường - 3 số - 2 kí tự @#$%"""
        uppercase = ''.join(random.choices(string.ascii_uppercase, k=2))
        lowercase = ''.join(random.choices(string.ascii_lowercase, k=6))
        digits = ''.join(random.choices(string.digits, k=3))
        special_chars = ''.join(random.choices('@#$%', k=2))
        
        password_parts = [uppercase, lowercase, digits, special_chars]
        random.shuffle(password_parts)
        return ''.join(password_parts)
    
    def generate_long_email_prefix(self):
        """Tạo email prefix dài 16-30 ký tự gồm chữ và số"""
        # Độ dài ngẫu nhiên từ 16 đến 30 ký tự
        length = random.randint(16, 30)
        
        # Tạo chuỗi gồm chữ cái thường và số
        characters = string.ascii_lowercase + string.digits
        
        # Tạo prefix ngẫu nhiên
        prefix = ''.join(random.choices(characters, k=length))
        
        # Đảm bảo có ít nhất 1 số và 1 chữ
        if not any(char.isdigit() for char in prefix):
            # Thêm ít nhất 1 số nếu chưa có
            prefix = prefix[:-1] + random.choice(string.digits)
        
        if not any(char.isalpha() for char in prefix):
            # Thêm ít nhất 1 chữ nếu chưa có
            prefix = prefix[:-1] + random.choice(string.ascii_lowercase)
        
        return prefix
    
    def save_account_info(self, account_data):
        """Lưu thông tin tài khoản vào file"""
        self.accounts_data.append(account_data)
        
        with open('google_accounts.json', 'w', encoding='utf-8') as f:
            json.dump(self.accounts_data, f, ensure_ascii=False, indent=2)
        
        with open('google_accounts.txt', 'a', encoding='utf-8') as f:
            f.write(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Họ: {account_data['last_name']}\n")
            f.write(f"Tên: {account_data['first_name']}\n")
            f.write(f"Ngày sinh: {account_data['birth_day']}/{account_data['birth_month']}/{account_data['birth_year']}\n")
            f.write(f"Giới tính: {account_data['gender']}\n")
            f.write(f"Email: {account_data['email']}\n")
            f.write(f"Mật khẩu: {account_data['password']}\n")
            f.write("-" * 50 + "\n")
    
    def handle_email_step(self, driver, first_name, last_name, birth_year):
        """Xử lý bước chọn/nhập email"""
        try:
            # Thử tìm email đề xuất (Dạng 2)
            try:
                time.sleep(2)
                suggested_email = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(@id, "selectionc")]'))
                )
                suggested_email.click()
                print("Đã chọn email đề xuất có sẵn")
                email_used = suggested_email.text.strip()
                
            except:
                # Dạng 1: Nhập email thủ công
                print("Không có email đề xuất, đang nhập email thủ công...")
                
                # Tìm ô nhập email
                email_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[2]/c-wiz/main/div[2]/div/div/div/form/span/section/div/div/div/div[1]/div[1]/div[1]/div/div[1]/input'))
                )
                
                # Tạo và nhập email prefix dài 16-30 ký tự
                email_prefix = self.generate_long_email_prefix()
                email_input.clear()
                
                # Nhập từng ký tự để mô phỏng gõ bàn phím thật
                for char in email_prefix:
                    email_input.send_keys(char)
                    time.sleep(0.05)  # Delay nhỏ để trông tự nhiên
                
                email_used = f"{email_prefix}@gmail.com"
                print(f"Đã nhập email prefix dài {len(email_prefix)} ký tự: {email_prefix}")
            
            # Nhấn nút Tiếp theo
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[1]/div[2]/c-wiz/main/div[3]/div/div[1]/div/div/button'))
            )
            next_button.click()
            
            return email_used
            
        except Exception as e:
            print(f"Lỗi khi xử lý bước email: {str(e)}")
            try:
                next_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/c-wiz/main/div[3]/div/div[1]/div/div/button')
                next_button.click()
                # Tạo email dự phòng
                backup_prefix = self.generate_long_email_prefix()
                return f"{backup_prefix}@gmail.com"
            except:
                raise e
    
    def create_account(self, instance_number):
        """Tạo một tài khoản Google"""
        try:
            options = Options()
            options.add_argument("--width=1000")
            options.add_argument("--height=700")
            options.add_argument(f"--window-position={instance_number*100},{instance_number*100}")
            
            driver = webdriver.Firefox(options=options)
            self.drivers.append(driver)
            
            print(f"[Instance {instance_number}] Đang mở trang đăng ký...")
            driver.get("https://accounts.google.com/signup?utm_source=tuquangnam.pages.dev")
            time.sleep(3)
            
            first_name, last_name = self.generate_random_name()
            birth_day, birth_month, birth_year = self.generate_random_birthdate()
            password = self.generate_random_password()
            gender = random.choice(["Nam", "Nữ"])
            
            # Bước 2: Nhập Họ và Tên
            print(f"[Instance {instance_number}] Đang nhập họ và tên...")
            
            first_name_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="firstName"]'))
            )
            first_name_field.send_keys(first_name)
            
            last_name_field = driver.find_element(By.XPATH, '//*[@id="lastName"]')
            last_name_field.send_keys(last_name)
            
            next_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/c-wiz/main/div[3]/div/div/div/div/button')
            next_button.click()
            time.sleep(2)
            
            # Bước 3: Ngày sinh và giới tính
            print(f"[Instance {instance_number}] Đang nhập thông tin sinh nhật và giới tính...")
            
            day_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="day"]'))
            )
            day_field.send_keys(str(birth_day))
            
            month_dropdown = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/c-wiz/main/div[2]/div/div/div/form/span/section/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/div')
            month_dropdown.click()
            time.sleep(1)
            
            month_option = driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div[2]/c-wiz/main/div[2]/div/div/div/form/span/section/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[2]/ul/li[{birth_month}]')
            month_option.click()
            time.sleep(1)
            
            year_field = driver.find_element(By.XPATH, '//*[@id="year"]')
            year_field.send_keys(str(birth_year))
            
            gender_dropdown = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/c-wiz/main/div[2]/div/div/div/form/span/section/div/div/div[2]/div[1]/div[1]/div/div[1]/div')
            gender_dropdown.click()
            time.sleep(1)
            
            if gender == "Nam":
                gender_option = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/c-wiz/main/div[2]/div/div/div/form/span/section/div/div/div[2]/div[1]/div[1]/div/div[2]/ul/li[2]')
            else:
                gender_option = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/c-wiz/main/div[2]/div/div/div/form/span/section/div/div/div[2]/div[1]/div[1]/div/div[2]/ul/li[1]')
            
            gender_option.click()
            time.sleep(1)
            
            next_button2 = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/c-wiz/main/div[3]/div/div/div/div/button')
            next_button2.click()
            time.sleep(2)
            
            # Bước 4: Email
            print(f"[Instance {instance_number}] Đang xử lý bước email...")
            email_used = self.handle_email_step(driver, first_name, last_name, birth_year)
            time.sleep(2)
            
            # Bước 5: Mật khẩu
            print(f"[Instance {instance_number}] Đang nhập mật khẩu...")
            
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[2]/c-wiz/main/div[2]/div/div/div/form/span/section/div/div/div/div[1]/div/div/div[1]/div/div[1]/div/div[1]/input'))
            )
            password_field.send_keys(password)
            
            confirm_password_field = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/c-wiz/main/div[2]/div/div/div/form/span/section/div/div/div/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            confirm_password_field.send_keys(password)
            next_button3 = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/c-wiz/main/div[3]/div/div/div/div/button')
            next_button3.click()
            # Lưu thông tin
            account_data = {
                "first_name": first_name,
                "last_name": last_name,
                "birth_day": birth_day,
                "birth_month": birth_month,
                "birth_year": birth_year,
                "gender": gender,
                "email": email_used,
                "password": password,
                "instance": instance_number,
                "timestamp": datetime.now().isoformat()
            }
            
            self.save_account_info(account_data)
            
            print(f"[Instance {instance_number}] Đã lưu thông tin tài khoản!")
            print(f"[Instance {instance_number}] Tên: {first_name} {last_name}")
            print(f"[Instance {instance_number}] Sinh nhật: {birth_day}/{birth_month}/{birth_year}")
            print(f"[Instance {instance_number}] Giới tính: {gender}")
            print(f"[Instance {instance_number}] Email: {email_used}")
            print(f"[Instance {instance_number}] Mật khẩu: {password}")
            
            print(f"[Instance {instance_number}] Đã hoàn thành!")
            
            return True
            
        except Exception as e:
            print(f"[Instance {instance_number}] Lỗi: {str(e)}")
            return False
    
    def create_multiple_accounts(self, num_accounts):
        """Tạo nhiều tài khoản"""
        successful_count = 0
        
        for i in range(num_accounts):
            print(f"\n=== Đang tạo tài khoản {i+1}/{num_accounts} ===")
            if self.create_account(i + 1):
                successful_count += 1
            
            if i < num_accounts - 1:
                time.sleep(3)
        
        print(f"\n=== Kết quả ===")
        print(f"Tạo thành công: {successful_count}/{num_accounts} tài khoản")
        print(f"Thông tin đã được lưu vào file: google_accounts.json và google_accounts.txt")
    
    def close_all(self):
        """Đóng tất cả trình duyệt"""
        for driver in self.drivers:
            try:
                driver.quit()
            except:
                pass

def main():
    print("=== TOOL TẠO TÀI KHOẢN GOOGLE TỰ ĐỘNG ===")
    
    try:
        num_accounts = int(input("Nhập số lượng tài khoản muốn tạo: "))
        
        if num_accounts <= 0:
            print("Số lượng tài khoản phải lớn hơn 0!")
            return
        
        creator = GoogleAccountCreator()
        
        try:
            creator.create_multiple_accounts(num_accounts)
        finally:
            input("\nNhấn Enter để đóng tất cả cửa sổ...")
            creator.close_all()
            
    except ValueError:
        print("Vui lòng nhập số hợp lệ!")
    except KeyboardInterrupt:
        print("\nĐã dừng chương trình!")

if __name__ == "__main__":
    main()
