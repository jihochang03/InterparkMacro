import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1900, 1000)
interpark_url = 'https://tickets.interpark.com//'

# 웹페이지가 로드될 때까지 2초를 대기
driver.implicitly_wait(time_to_wait=2)
driver.get(url=interpark_url)

# Tkinter 초기화
root = tk.Tk()
root.withdraw()

# 사용자 입력을 위한 새로운 창 생성
input_window = tk.Toplevel(root)
input_window.title("Input Information")

# 스타일 적용
style = ttk.Style()
style.configure('TLabel', 12)
style.configure('TEntry', 12)
style.configure('TButton', 12)
style.configure('TCombobox', 12)

# 입력 필드 라벨과 엔트리 박스 생성
labels = ['아이디:', '비밀번호:', '뮤지컬명:', '날짜 (mm.dd):', '회차:','극장명:']
entries = []

for i, label_text in enumerate(labels):
    label = ttk.Label(input_window, text=label_text)
    label.grid(row=i, column=0, padx=10, pady=10, sticky='e')
    
    if label_text == '뮤지컬명:':
        entry = ttk.Combobox(input_window, values=["프랑켄슈타인", "시카고", "어쩌면 해피엔딩", "하데스타운", "홍련", "4월은 너의 거짓말", "등등곡", "젠틀맨스 가이드", "비밀의 화원", "접변"])
    elif label_text == '극장명:':
        entry = ttk.Combobox(input_window, values=["블루스퀘어", "디큐브 링크아트센터", "예스24 1관", "샤롯데씨어터", "대학로 자유극장", "토월극장", "TOM 1관", "광림아트센터 BBCH홀", "국립정동극장", "TOM 2관"])
    else:
        entry = ttk.Entry(input_window)
        
    entry.grid(row=i, column=1, padx=10, pady=10, sticky='w')
    entries.append(entry)

user_id_entry, user_pwd_entry, search_keyword_entry, target_date_entry, target_number_entry,  theater_name_entry = entries

def submit():
    global user_id, user_pwd, search_keyword, target_date_str,number, theater_name
    user_id = user_id_entry.get()
    user_pwd = user_pwd_entry.get()
    search_keyword = search_keyword_entry.get()
    target_date_str = target_date_entry.get()
    number = target_number_entry.get()
    theater_name = theater_name_entry.get()
    input_window.destroy()

submit_button = ttk.Button(input_window, text="Submit", command=submit)
submit_button.grid(row=len(labels), column=0, columnspan=2, pady=20)

root.wait_window(input_window)

target_month, target_day = map(int, target_date_str.split('.'))


# 현재 시간을 가져오는 함수
def get_current_time():
    now = datetime.now()
    return now

# 지정된 시간에 클릭 동작을 수행하는 함수
def click_at_9am():
    # 기다리기
    while True:
        now = get_current_time()
        if now.hour == 8 and now.minute >= 59  and now.second >= 45:
            break
        time.sleep(1)  # 1초마다 한 번씩 체크

def click_at_8_53():
    # 기다리기
    while True:
        now = get_current_time()
        if now.hour == 8 and now.minute == 52  and now.second >= 58:
            break
        time.sleep(1)  # 1초마다 한 번씩 체크

# 로그인
driver.find_element(By.LINK_TEXT, '로그인').click()
userId = driver.find_element(By.ID, 'userId')
userId.send_keys(user_id)
userPwd = driver.find_element(By.ID, "userPwd")
userPwd.send_keys(user_pwd)
userPwd.send_keys(Keys.ENTER)

# 검색 수행
search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/header/div[2]/div/div/div[1]/div[3]/div[1]/input')))
search.send_keys(search_keyword)
search.send_keys(Keys.ENTER)

if search_keyword=='프랑켄슈타인':
    driver.find_element(By.XPATH, '//*[@id="contents"]/div/div/div[1]/div[2]/a[1]/ul/li[1]').click()
elif search_keyword=='시카고':
    driver.find_element(By.XPATH, '//*[@id="contents"]/div/div/div[3]/div[2]/a/ul/li[1]').click()
elif search_keyword=='어쩌면 해피엔딩':
    driver.find_element(By.XPATH, '//*[@id="contents"]/div/div/div[1]/div[2]/a/ul/li[1]').click() 
elif search_keyword=='하데스타운':
    driver.find_element(By.XPATH, '//*[@id="contents"]/div/div/div[1]/div[2]/a/ul/li[1]').click()
elif search_keyword=='홍련':
    driver.find_element(By.XPATH, '//*[@id="contents"]/div/div/div[1]/div[2]/a/ul/li[1]').click()
elif search_keyword=='4월은 너의 거짓말':
    driver.find_element(By.XPATH, '//*[@id="contents"]/div/div/div[1]/div[2]/a/ul/li[1]').click()
elif search_keyword=='등등곡':
    driver.find_element(By.XPATH, '//*[@id="contents"]/div/div/div[1]/div[2]/a[1]/ul/li[1]').click()
elif search_keyword=='젠틀맨스 가이드':
    driver.find_element(By.XPATH, '//*[@id="contents"]/div/div/div[1]/div[2]/a/ul/li[1]').click()
elif search_keyword=='비밀의 화원':
    driver.find_element(By.XPATH, '//*[@id="contents"]/div/div/div[1]/div[2]/a/ul/li[1]').click()
elif search_keyword=='접변':
    driver.find_element(By.XPATH, '//*[@id="contents"]/div/div/div[1]/div[2]/a/ul/li[1]').click()
driver.switch_to.window(driver.window_handles[-1])

# 예매하기
print('--------------------')
print(driver.window_handles)
time.sleep(5)
driver.switch_to.window(driver.window_handles[-1])
nxt_button = driver.find_element(By.XPATH, "//*[@id='productSide']/div/div[1]/div[1]/div[2]/div/div/div/div/ul[1]/li[3]")
while True:
    current_date = driver.find_element(By.XPATH,"//*[@id='productSide']/div/div[1]/div[1]/div[2]/div/div/div/div/ul[1]/li[2]")
    cur_month = int(current_date.text.split(' ')[1])
    if cur_month != target_month:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(nxt_button)).click()
    else:
        break
time.sleep(0.3)
find_day = driver.find_element(By.XPATH, "//li[text()='"+str(target_day)+"']")
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(find_day)).click()

if number=='2' :
    second_button = driver.find_element(By.XPATH, '//*[@id="productSide"]/div/div[1]/div[2]/div[2]/div[1]/ul/li[2]/a/span[1]')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(second_button)).click()
#click_at_8_53()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="productSide"]/div/div[2]/a[1]'))).click()
print('--------------------')
print(driver.window_handles)
driver.switch_to.window(driver.window_handles[-1])

global okay
okay = 0

def wait_for_available_reserve_seat():
    global okay  # okay 변수를 전역 변수로 선언
    while True:
        try:
            driver.switch_to.window(driver.window_handles[-1])
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            for ifr in iframes:
                if ifr.get_attribute('name') == 'ifrmSeat':
                    driver.switch_to.frame(ifr)
                    break

            # 올바른 iframe을 선택했는지 확인
            try:
                if okay <= 1:
                    my_play_date_element = WebDriverWait(driver, 1).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="PlaySeq"]'))
                    )
                    print("좌석창 확인")
                    break
            except selenium.common.exceptions.TimeoutException:
                print("올바른 iframe을 찾지 못함. 다시 시도합니다...")
                driver.switch_to.default_content()
                okay += 1
                continue
        except selenium.common.exceptions.TimeoutException:
            print("대기 중입니다. 계속 시도합니다...")
            driver.refresh()
            continue
        except Exception as e:
            print(f"예외 발생: {e}")
            driver.refresh()
            continue

def alphabet_to_number(alphabet):
    return ord(alphabet.upper()) - ord('A') + 1

# 좌석 선택 함수
def select_and_click_seat():
    print('******************************select seat')
    print(driver.window_handles)
    
    global flag
    flag = 0
    want_seat_list = []
    if theater_name == "블루스퀘어":
        driver.switch_to.frame('ifrmSeatDetail')
        available_reserve_seat = driver.find_elements(By.XPATH, "//img[@class='stySeat']")
        # 좌석이 로드될 때까지 대기
        if not available_reserve_seat:
            return False
        print("available_reserve")
        for seat in available_reserve_seat:
            if flag==1: break
            alt_text = seat.get_attribute("alt")
            print(f"Seat alt text: {alt_text}")
            # 조건에 맞는 좌석을 필터링
            if "객석1층-" in alt_text:
                    seat_info = alt_text.split("객석1층-")[1]
                    row_text, seat_num_text = seat_info.split('-')
                    row_num = int(row_text.replace("열", ""))  # "22열"에서 "22" 추출
                    seat_num = int(seat_num_text)  # 좌석 번호
                    if row_num <= 18 and 16 <= seat_num <= 31:
                        want_seat_list.append(seat)
                        flag = 1
                
    elif theater_name == "디큐브 링크아트센터":                
        available_reserve_seat = driver.find_elements(By.XPATH, "//img[@class='stySeat']")
        print("available_reserve")
        for seat in available_reserve_seat:
            if flag==1: break
            alt_text = seat.get_attribute("alt")
            print(f"Seat alt text: {alt_text}")
            # 조건에 맞는 좌석을 필터링
            if "1층-" in alt_text:
                seat_info = alt_text.split("1층-")[1]
                section_info, row_seat_info = seat_info.split('구역 ')
                row_text, seat_num_text = row_seat_info.split('열-')
                section = section_info.strip()  # "A구역" 등 구역 정보
                row_num = int(row_text)  # "10열"에서 "10" 추출
                print(f"section:{section}, row_num:{row_num}")
                # 조건에 맞는 좌석 필터링: 특정 구역, 행, 좌석 번호
                if section == "B" and row_num <= 9:
                    want_seat_list.append(seat)
                    flag = 1
            
    elif theater_name == "예스24 1관":                
        available_reserve_seat = driver.find_elements(By.XPATH, "//img[@class='stySeat']")
        print("available_reserve")
        for seat in available_reserve_seat:
            if flag==1: 
                print("-----------flag=1-------------")
                break
            alt_text = seat.get_attribute("alt")
            print(f"Seat alt text: {alt_text}")
            # 조건에 맞는 좌석을 필터링
            if "1층-" in alt_text:
                print(f"Seat alt text: {alt_text}")
                seat_info = alt_text.split("1층-")[1]
                print(f"seat_info: {seat_info}")
                row_text, seat_num_text = seat_info.split('-')
                print(f"row_text: {row_text}, seat_num_text: {seat_num_text}")
                row_text2 = row_text.replace("열", "")  # "22열"에서 "22" 추출
                print(f"row_text2: {row_text2}")
                row_num = alphabet_to_number(row_text2.strip()) 
                print(f"row_num:{row_num}")
                seat_num = int(seat_num_text)
                print(f"seat_num:{seat_num}")
                # 조건에 맞는 좌석 필터링: 특정 구역, 행, 좌석 번호
                if row_num <=9  and 5 <= seat_num <= 16:
                    want_seat_list.append(seat)
                    flag = 1
    elif theater_name == "샤롯데씨어터":                
        available_reserve_seat = driver.find_elements(By.XPATH, "//img[@class='stySeat']")
        print("available_reserve")
        for seat in available_reserve_seat:
            if flag==1: break
            alt_text = seat.get_attribute("alt")
            print(f"Seat alt text: {alt_text}")
            # 조건에 맞는 좌석을 필터링
            if "2층-" in alt_text:
                seat_info = alt_text.split("2층-")[1]
                section_info, row_seat_info = seat_info.split('구역')
                print(f"section_info: {section_info}, row_seat_info: {row_seat_info}")
                row_text, seat_num_text = row_seat_info.split('열-')
                section = section_info.strip()  # "A구역" 등 구역 정보
                row_num = int(row_text)  # "10열"에서 "10" 추출
                print(f"section:{section}, row_num:{row_num}")
                # 조건에 맞는 좌석 필터링: 특정 구역, 행, 좌석 번호
                if section == "B" and row_num <= 9:
                    want_seat_list.append(seat)
                    flag = 1
    elif theater_name == "대학로 자유극장":                
        available_reserve_seat = driver.find_elements(By.XPATH, "//img[@class='stySeat']")
        print("available_reserve")
        for seat in available_reserve_seat:
            if flag==1: break
            alt_text = seat.get_attribute("alt")
            print(f"Seat alt text: {alt_text}")
            # 조건에 맞는 좌석을 필터링
            row_text, seat_num_text = alt_text.split('-')
            print(f"row_text: {row_text}, seat_num_text: {seat_num_text}")
            row_text2 = row_text.replace("열", "")  # "22열"에서 "22" 추출
            print(f"row_text2: {row_text2}")
            row_num = alphabet_to_number(row_text2.strip()) 
            print(f"row_num:{row_num}")
            seat_num = int(seat_num_text)
            print(f"seat_num:{seat_num}")
            # 조건에 맞는 좌석 필터링: 특정 구역, 행, 좌석 번호
            if row_num <=5 and 5<= seat_num <= 10:
                want_seat_list.append(seat)
                flag = 1     
    elif theater_name == "토월극장":                
        available_reserve_seat = driver.find_elements(By.XPATH, "//img[@class='stySeat']")
        print("available_reserve")
        for seat in available_reserve_seat:
            if flag==1: break
            alt_text = seat.get_attribute("alt")
            print(f"Seat alt text: {alt_text}")
            # 조건에 맞는 좌석을 필터링
            if "1층-" in alt_text:
                seat_info = alt_text.split("1층-")[1]
                section_info, row_seat_info = seat_info.split('블록')
                print(f"section_info: {section_info}, row_seat_info: {row_seat_info}")
                row_text, seat_text = row_seat_info.split('열-')
                section = section_info.strip()  # "A구역" 등 구역 정보
                row_num = int(row_text)  # "10열"에서 "10" 추출
                seat_num = int(seat_text)
                print(f"section:{section}, row_num:{row_num}")
                # 조건에 맞는 좌석 필터링: 특정 구역, 행, 좌석 번호
                if section == "B" and row_num <= 8 and 1 <= seat_num <= 16:
                    want_seat_list.append(seat)
                    flag = 1      
    elif theater_name == "TOM 1관":                
        available_reserve_seat = driver.find_elements(By.XPATH, "//img[@class='stySeat']")
        print("available_reserve")
        for seat in available_reserve_seat:
            if flag==1: break
            alt_text = seat.get_attribute("alt")
            print(f"Seat alt text: {alt_text}")
            # 조건에 맞는 좌석을 필터링
            row_text, seat_num_text = alt_text.split('-')
            print(f"row_text: {row_text}, seat_num_text: {seat_num_text}")
            row_text2 = row_text.replace("열", "")  # "22열"에서 "22" 추출
            print(f"row_text2: {row_text2}")
            row_num = alphabet_to_number(row_text2.strip()) 
            print(f"row_num:{row_num}")
            seat_num = int(seat_num_text)
            print(f"seat_num:{seat_num}")
            # 조건에 맞는 좌석 필터링: 특정 구역, 행, 좌석 번호
            if row_num <=9 and 1<= seat_num <= 20:
                want_seat_list.append(seat)
                flag = 1 
    elif theater_name == "광림아트센터 BBCH홀":                
        available_reserve_seat = driver.find_elements(By.XPATH, "//img[@class='stySeat']")
        print("available_reserve")
        for seat in available_reserve_seat:
            if flag==1: break
            alt_text = seat.get_attribute("alt")
            print(f"Seat alt text: {alt_text}")
            if "1층-" in alt_text:
                seat_info = alt_text.split("1층-")[1]  # "1층-" 이후의 문자열을 추출
                print(f"seat_info: {seat_info}")
                row_text, seat_num_text = seat_info.split('열')  # '열'을 기준으로 문자열을 분할
                seat_num_text = seat_num_text.replace("-", "")  # '열' 이후의 문자열에서 '-'를 제거
                print(f"row_text: {row_text}, seat_num_text: {seat_num_text}")
                row_num = alphabet_to_number(row_text.strip())
                print(f"row_num: {row_num}")
                seat_num = int(seat_num_text)
                print(f"seat_num: {seat_num}")
                if row_num <= 8 and 11 <= seat_num <= 30:
                    want_seat_list.append(seat)
                    flag = 1    
    elif theater_name == "국립정동극장":                
        available_reserve_seat = driver.find_elements(By.XPATH, "//img[@class='stySeat']")
        print("available_reserve")
        for seat in available_reserve_seat:
            if flag==1: break
            alt_text = seat.get_attribute("alt")
            print(f"Seat alt text: {alt_text}")
            if "1층-" in alt_text:
                seat_info = alt_text.split("1층-")[1]  # "1층-" 이후의 문자열을 추출
                print(f"seat_info: {seat_info}")
                row_text, seat_num_text = seat_info.split('열')  # '열'을 기준으로 문자열을 분할
                seat_num_text = seat_num_text.replace("-", "")  # '열' 이후의 문자열에서 '-'를 제거
                print(f"row_text: {row_text}, seat_num_text: {seat_num_text}")
                seat_num = int(seat_num_text)
                print(f"seat_num: {seat_num}")
                if row_text =='B' and 1 <= seat_num <= 9:
                    want_seat_list.append(seat)
                    flag = 1    
    elif theater_name == "TOM 2관":                
        available_reserve_seat = driver.find_elements(By.XPATH, "//img[@class='stySeat']")
        print("available_reserve")
        for seat in available_reserve_seat:
            if flag==1: break
            alt_text = seat.get_attribute("alt")
            print(f"Seat alt text: {alt_text}")
            if "C구역" in alt_text:
                seat_info = alt_text.split("C구역")[1]  # "1층-" 이후의 문자열을 추출
                print(f"seat_info: {seat_info}")
                row_text, seat_num_text = seat_info.split('열')  # '열'을 기준으로 문자열을 분할  # '열' 이후의 문자열에서 '-'를 제거
                print(f"row_text: {row_text}, seat_num_text: {seat_num_text}")
                row_num=int(row_text)
                seat_num_text = seat_num_text.replace("-", "")
                seat_num = int(seat_num_text)
                print(f"row_num: {row_num}, seat_num: {seat_num}")
                if row_num <=4 and 1 <= seat_num <= 17:
                    want_seat_list.append(seat)
                    flag = 1   
                        
    if flag == 1 and want_seat_list:
        target_seat = want_seat_list[0]
        print(f"Clicking on seat with alt text: {target_seat.get_attribute('alt')}")
        # 자바스크립트를 사용하여 요소 클릭
        driver.execute_script("arguments[0].click();", target_seat)
        return True
    else:
        print("No seats found matching the criteria.")
        return False  # 조건에 맞는 좌석이 없을 경우 False 반환

global sleep
sleep=0    
# 메인 로직
while True:
    
    try:
        #if sleep==0 : click_at_9am()
        wait_for_available_reserve_seat()
        print("wait finished")
        if search_keyword=="프랑켄슈타인" and sleep==0: time.sleep(5)
        sleep=1
        seat_selected = select_and_click_seat()
        print("seat_selected")
        if seat_selected:
            print("success")
            driver.switch_to.window(driver.window_handles[-1])
            iframes = driver.find_elements(By.TAG_NAME, "iframe")

            for ifr in iframes:
                if ifr.get_attribute('name') == 'ifrmSeat':
                    driver.switch_to.frame(ifr)
                    break
            
            next_step_button = WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='NextStepImage']"))
            )
            driver.execute_script("arguments[0].click();", next_step_button)
            time.sleep(1)
        
            try:
                driver.switch_to.window(driver.window_handles[-1])
                iframes = driver.find_elements(By.TAG_NAME, "iframe")

                for ifr in iframes:
                    if ifr.get_attribute('name') == 'ifrmBookStep':
                        driver.switch_to.frame(ifr)
                        break
                print("예매화면")
                my_play_date_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="PriceRow001"]/td[3]/select'))
                )
                print("잘넘어감")
                time.sleep(200)
            except Exception as e:
                    print("올바른 iframe을 찾지 못함. 다시 시도합니다...")
                    driver.switch_to.default_content()
                    continue
            
        print("--------refresh---------------")
        driver.refresh()
    
    except Exception as e:
        print(f"좌석 선택 또는 예매 실패: {e}")
        driver.refresh()
        continue  # 예외 발생 시 다시 시도
