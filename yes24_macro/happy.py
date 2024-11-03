import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import JavascriptException
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1900, 1000)
yes24_url = 'http://ticket.yes24.com/New/Main.aspx'

# 웹페이지가 로드될 때까지 2초를 대기
driver.implicitly_wait(time_to_wait=2)
driver.get(url=yes24_url)

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

labels = ['날짜 (mm.dd):', '회차:' , '티켓팅 시간 (HH:MM):', '극장명:']
entries = []

for i, label_text in enumerate(labels):
    label = ttk.Label(input_window, text=label_text)
    label.grid(row=i, column=0, padx=10, pady=10, sticky='e')
    

    if label_text == '극장명:':
        entry = ttk.Combobox(input_window, values=[ "예스24 1관", "샤롯데씨어터", "대학로 자유극장", "토월극장", "TOM 1관", "광림아트센터 BBCH홀", "국립정동극장", "TOM 2관", "링크아트센터 1관"])
    else:
        entry = ttk.Entry(input_window)
        
    entry.grid(row=i, column=1, padx=10, pady=10, sticky='w')
    entries.append(entry)

target_date_entry, target_number_entry, target_time_entry, theater_name_entry = entries

def submit():
    global target_date_str, number, target_time_str,  theater_name
    target_date_str = target_date_entry.get()
    number = target_number_entry.get()
    target_time_str = target_time_entry.get()
    theater_name = theater_name_entry.get()
    input_window.destroy()

submit_button = ttk.Button(input_window, text="Submit", command=submit)
submit_button.grid(row=len(labels), column=0, columnspan=2, pady=20)

root.wait_window(input_window)

# 입력된 시간을 파싱
target_month, target_day = map(int, target_date_str.split('.'))
target_hour, target_minute = map(int, target_time_str.split(':'))

# 현재 시간을 가져오는 함수
def get_current_time():
    now = datetime.now()
    return now

# 지정된 시간 2초 전을 기다리는 함수
def wait_until_target_time():
    print(f"target hour: {target_hour}, target minute: {target_minute}")
    while True:
        now = get_current_time()
        print(f"{now.hour}:{now.minute}:{now.second}")
        if now.hour == (target_hour - 1) and now.minute == 59 and now.second >= 59:
            break
        elif now.hour == target_hour and now.minute >= target_minute:
            break
        time.sleep(1)  # 1초마다 한 번씩 체크

# 지정된 시간에 클릭 동작을 수행하는 함수
def click_at_target_time():
    # 기다리기
    wait_until_target_time()

    # 클릭
    try:
        driver.execute_script("window.location.reload();")
    except Exception as e:
        print(f"클릭 동작 실패: {e}")

time.sleep(30)
driver.switch_to.window(driver.window_handles[-1])
#WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="popup-prdGuide"]/div/div[3]/div/a'))).click()
click_at_target_time()


# 예매하기
print('--------------------')
print(driver.window_handles)
driver.switch_to.window(driver.window_handles[-1])
nxt_button = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="rncalendar"]/div/div/a[2]/span')))
while True:
    # Extract the text of the current month from the WebElement and convert it to an integer
    cur_month = int(driver.find_element(By.XPATH, '//*[@id="rncalendar"]/div/div/div/span[2]').text)
    
    if cur_month != target_month:
        # Wait until the next button is clickable and click it
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(nxt_button)).click()
    else:
        break
time.sleep(0.3)

print(f"//li[text()={target_day}]")
find_day = driver.find_element(By.XPATH, f"//a[text()={target_day}]")
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(find_day)).click()
time.sleep(0.3)

if number=='1':
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="PerfPlayTime"]/a[1]'))).click()
elif number=='2' :
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="PerfPlayTime"]/a[2]'))).click()
elif number=='3' :
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="PerfPlayTime"]/a[3]'))).click()
if number=='0':
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="PerfPlayTime"]/a'))).click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mainForm"]/div[10]/div/div[4]/a[4]'))).click()
print("let'sgo")

print('--------------------')
print(driver.window_handles)
driver.switch_to.window(driver.window_handles[-1])
time.sleep(1)
seat_select_button= WebDriverWait(driver, 200).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnSeatSelect"]')))
seat_select_button.click()
print("넘어감")

global okay
okay = 0

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
                    if row_num <= 9 and 16 <= seat_num <= 31:
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
            
    elif theater_name == "예스24 1관" and number=='1':                
        try:
            frame_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="divFlash"]/iframe'))
            )
            driver.switch_to.frame(frame_element)
            print("Successfully switched to iframe.")
        except Exception as e:
            print(f"Failed to switch to iframe: {e}")
        available_reserve_seat = driver.find_elements(By.XPATH, '//div[@class="s8" and @name="tk"]')
#driver.find_element(By.XPATH,'//*[@id="t5700156"]').click()
        print("available_reserve")
        for seat in available_reserve_seat:
            if flag==1: break
            print("seat")
            title_text = seat.get_attribute("title")
            print(f"Seat title text: {title_text}")
            if "2층 " in title_text:
                seat_info = title_text.split("2층 ")[1]  # "1층-" 이후의 문자열을 추출
                print(f"seat_info: {seat_info}")
                row_text, seat_num_text = seat_info.split('열')  # '열'을 기준으로 문자열을 분할  # '열' 이후의 문자열에서 '-'를 제거
                print(f"row_text: {row_text}, seat_num_text: {seat_num_text}")
                
                row_num = alphabet_to_number(row_text.strip())  # 행(row)을 숫자로 변환
                seat_num_text = seat_num_text.replace("번", "").strip()  # 좌석 번호에서 '번'을 제거하고 좌우 공백 제거
                print(f"seat_num_text: {seat_num_text}")

                try:
                    seat_num = int(seat_num_text)  # 좌석 번호를 정수로 변환
                    print(f"row_num: {row_num}, seat_num: {seat_num}")
                except ValueError:
                    print("좌석 번호를 정수로 변환할 수 없습니다.")
                if row_num <= 20 and 1 <= seat_num <= 24:
                    want_seat_list.append(seat)
                    flag = 1  
                    
    elif theater_name == "예스24 1관" and target_people=='2':                
        try:
            frame_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="divFlash"]/iframe'))
            )
            driver.switch_to.frame(frame_element)
            print("Successfully switched to iframe.")
        except Exception as e:
            print(f"Failed to switch to iframe: {e}")
        available_reserve_seat = driver.find_elements(By.XPATH, '//div[@class="s6" and @name="tk"]')
        if not available_reserve_seat:
            return False
        print("available_reserve")
        seat_map = {}
        for seat in available_reserve_seat:
            if flag==1: break
            print("seat")
            title_text = seat.get_attribute("title")
            print(f"Seat title text: {title_text}")
            if "1층 " in title_text:
                seat_info = title_text.split("1층 ")[1]  # "1층-" 이후의 문자열을 추출
                print(f"seat_info: {seat_info}")
                row_text, seat_num_text = seat_info.split('열')  # '열'을 기준으로 문자열을 분할  # '열' 이후의 문자열에서 '-'를 제거
                print(f"row_text: {row_text}, seat_num_text: {seat_num_text}")
                
                row_num = alphabet_to_number(row_text.strip())  # 행(row)을 숫자로 변환
                seat_num_text = seat_num_text.replace("번", "").strip()  # 좌석 번호에서 '번'을 제거하고 좌우 공백 제거
                print(f"seat_num_text: {seat_num_text}")
                seat_num = int(seat_num_text)  # 좌석 번호를 정수로 변환
                print(f"row_num: {row_num}, seat_num: {seat_num}")
                if row_num <= 15 and 1 <= seat_num <= 24:
                    if row_num not in seat_map:
                        seat_map[row_num] = []
                    seat_map[row_num].append((seat_num, seat))
        for row_num in seat_map:
            seat_map[row_num].sort()
        for row_num in seat_map:
            seats_in_row = seat_map[row_num]
            consecutive_seats = []
            for i in range(len(seats_in_row)):
                if i == 0:
                    consecutive_seats.append(seats_in_row[i])
                else:
                    if seats_in_row[i][0] == seats_in_row[i - 1][0] + 1:
                        consecutive_seats.append(seats_in_row[i])
                    else:
                        if len(consecutive_seats) >= 2:  # Adjust the number of seats you need
                            break
                        consecutive_seats = [seats_in_row[i]]

                if len(consecutive_seats) >= 2:  # Adjust the number of seats you need
                    break

            if len(consecutive_seats) >= 2:  # Adjust the number of seats you need
                want_seat_list.extend([seat[1] for seat in consecutive_seats])
                flag = 1
                break

    # Debug: Print want_seat_list
        print("Want seat list:")
        for seat in want_seat_list:
            print(seat.get_attribute("title"))
            
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
    elif theater_name == "링크아트센터 1관":   
        try:
            frame_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="divFlash"]/iframe'))
            )
            driver.switch_to.frame(frame_element)
            print("Successfully switched to iframe.")
        except Exception as e:
            print(f"Failed to switch to iframe: {e}")
        available_reserve_seat = driver.find_elements(By.XPATH, '//div[(contains(@class, "s6") or contains(@class, "s8") or contains(@class, "s4")) and @name="tk"]')

        print("available_reserve")
        for seat in available_reserve_seat:
            if flag==1: break
            print("seat")
            title_text = seat.get_attribute("title")
            if "1층 " in title_text:
                seat_info = title_text.split("1층 ")[1]  # "1층-" 이후의 문자열을 추출
                print(f"seat_info: {seat_info}")
                row_text, seat_num_text = seat_info.split('열')  # '열'을 기준으로 문자열을 분할  # '열' 이후의 문자열에서 '-'를 제거
                print(f"row_text: {row_text}, seat_num_text: {seat_num_text}")
                
                row_num = alphabet_to_number(row_text.strip())  # 행(row)을 숫자로 변환
                seat_num_text = seat_num_text.replace("번", "").strip()  # 좌석 번호에서 '번'을 제거하고 좌우 공백 제거
                print(f"seat_num_text: {seat_num_text}")

                try:
                    seat_num = int(seat_num_text)  # 좌석 번호를 정수로 변환
                    print(f"row_num: {row_num}, seat_num: {seat_num}")
                except ValueError:
                    print("좌석 번호를 정수로 변환할 수 없습니다.")
                if row_num <= 19 and 13 <= seat_num <= 26:
                    want_seat_list.append(seat)
                    flag = 1  
    if flag == 1 and want_seat_list:
        target_seat = want_seat_list[0]
        print(f"Clicking on seat with alt text: {target_seat.get_attribute('title')}")
        # 자바스크립트를 사용하여 요소 클릭
        driver.execute_script("arguments[0].click();", target_seat)
        return True
    else:
        print("No seats found matching the criteria.")
        return False
    
def get_current_iframe_hierarchy(driver):
    current_window = driver.current_window_handle
    frames = []

    while True:
        try:
            parent_frame = driver.execute_script('return window.parent.location.href')
            current_frame = driver.execute_script('return window.location.href')
            frames.append(current_frame)

            if parent_frame == current_frame:
                break

            driver.switch_to.parent_frame()
        except Exception as e:
            break

    driver.switch_to.window(current_window)
    return frames[::-1]  # 위에서부터 아래로 계층을 반환
global sleep
sleep=0
# 메인 로직
while True:
        #wait_for_available_reserve_seat()
        print("wait finished")
        sleep=1
        seat_selected = select_and_click_seat()
        print("seat_selected")
        if seat_selected:
            print("success")
            next_step_button = WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="form1"]/div[3]/div[2]/div/div[2]/p[2]/a/img'))
            )
            driver.execute_script("arguments[0].click();", next_step_button)
            print('okay')
            time.sleep(1)
        
            try:
                driver.switch_to.window(driver.window_handles[-1])
                iframes = driver.find_elements(By.TAG_NAME, "iframe")
                # for ifr in iframes:
                #     if ifr.get_attribute('name') == 'ifrmBookStep':
                #         driver.switch_to.frame(ifr)
                #         break
                #     else: print(f"ifr.get_attribute('name')")

                print("예매화면")
                my_play_date_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="tblPromotionGroup1"]/thead/tr/th[1]'))
                )
                print("잘넘어감")
                time.sleep(200)
            except Exception as e:
                    print("올바른 iframe을 찾지 못함. 다시 시도합니다...")
                    driver.switch_to.default_content()
                    continue
                
        driver.switch_to.window(driver.window_handles[-1])
        iframes = driver.find_elements(By.TAG_NAME, "iframe")

        for ifr in iframes:
            if ifr.get_attribute('name') == 'ifrmSeatFrame':
                driver.switch_to.frame(ifr)
                break

        # Optionally, you can call the function directly if it's still not working
        try:
            driver.execute_script("ChoiceReset();")
            print("ChoiceReset function executed.")
        except JavascriptException as e:
            print(f"Error executing JavaScript: {e}")        

        
print('finish')
time.sleep(200)    