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
from tkinter import simpledialog

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

# 사용자 입력 받기
user_id = simpledialog.askstring(title="Login", prompt="아이디를 입력하세요")
user_pwd = simpledialog.askstring(title="Login", prompt="비밀번호를 입력하세요", show='*')
search_keyword = simpledialog.askstring(title="Search", prompt="뮤지컬명을 입력하세요 (e.g., 프랑켄슈타인):")
wait_time_str = simpledialog.askstring(title="Wait Time", prompt="티켓팅 시간을 입력하세요 (e.g., 11:00):")
theater_name = simpledialog.askstring(title="Theater", prompt="극장 이름을 입력하세요")
# 로그인
driver.find_element(By.LINK_TEXT, '로그인').click()
userId = driver.find_element(By.ID, 'userId')
userId.send_keys(user_id)
userPwd = driver.find_element(By.ID, "userPwd")
userPwd.send_keys(user_pwd)
userPwd.send_keys(Keys.ENTER)

# 입력된 시간을 파싱
target_hour, target_minute = map(int, wait_time_str.split(':'))

# 현재 시간을 가져오는 함수
def get_current_time():
    now = datetime.now()
    return now

# 지정된 시간 2초 전을 기다리는 함수
def wait_until_target_time():
    while True:
        now = get_current_time()
        print(f"now: {now.hour}, {now.minute}, {now.second}")
        if now.hour == (target_hour-1) and now.minute >= 59 and now.second >= 58:
            break
        time.sleep(1)  # 1초마다 한 번씩 체크

# 지정된 시간에 클릭 동작을 수행하는 함수
def click_at_target_time():
    # 기다리기
    print(f"target: {target_hour}, {target_minute}")
    wait_until_target_time()

    # 클릭
    try:
        element = driver.find_element(By.XPATH, '//*[@id="contents"]/div/div/div[2]/div[2]/a[1]')
        element.click()
    except Exception as e:
        print(f"클릭 동작 실패: {e}")

# 검색 수행
search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/header/div[2]/div/div/div[1]/div[3]/div[1]/input')))
search.send_keys(search_keyword)
search.send_keys(Keys.ENTER)
click_at_target_time()

# 예매하기
print('--------------------')
print(driver.window_handles)
driver.switch_to.window(driver.window_handles[-1])
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="popup-prdGuide"]/div/div[3]/div/a'))).click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="productSide"]/div/div[1]/div[1]/div[2]/div/div/div/div/ul[1]/li[3]'))).click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="productSide"]/div/div[1]/div[1]/div[2]/div/div/div/div/ul[1]/li[3]'))).click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="productSide"]/div/div[1]/div[1]/div[2]/div/div/div/div/ul[3]/li[10]'))).click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="productSide"]/div/div[2]/a[1]'))).click()
print('--------------------')
print(driver.window_handles)
driver.switch_to.window(driver.window_handles[-1])

time.sleep(5)
# 좌석 탐색
print('******************************select seat')
print(driver.window_handles)
driver.switch_to.window(driver.window_handles[-1])
iframes = driver.find_elements(By.TAG_NAME, "iframe")
for ifr in iframes:
    if ifr.get_attribute('name') == 'ifrmSeat':
        driver.switch_to.frame(ifr)
        driver.switch_to.frame('ifrmSeatDetail')
        break

# 요소 찾기
available_reserve_seat = driver.find_elements(By.XPATH, "//img[@class='stySeat']")
print("Available reserve seats:")

if(theater_name=='블루스퀘어'): 
    flag = 0
    want_seat_list = []
    for seat in available_reserve_seat:
        alt_text = seat.get_attribute("alt")
        print(f"Seat alt text: {alt_text}")
        # 조건에 맞는 좌석을 필터링
        if "객석1층-" in alt_text:
            print(f"Seat alt text: {alt_text}")
            try:
                seat_info = alt_text.split("객석1층-")[1]
                row_text, seat_num_text = seat_info.split('-')
                row_num = int(row_text.replace("열", ""))  # "22열"에서 "22" 추출
                print(f"row_num={row_num}")
                seat_num = int(seat_num_text)  # 좌석 번호
                if row_num <= 7 and 16 <= seat_num <= 31:
                    want_seat_list.append(seat)
                    flag = 1
                    break
            except ValueError:
            # 예상치 못한 형식의 alt_text를 가진 요소가 있을 경우 무시
                continue
elif(theater_name=='디큐브아트센터'): 
    flag = 0
    want_seat_list = []
    for seat in available_reserve_seat:
        alt_text = seat.get_attribute("alt")
        print(f"Seat alt text: {alt_text}")
        # 조건에 맞는 좌석을 필터링
        if "[VIP석]" in alt_text:
            try:
                area_info = alt_text.split("구역")[1].split()[0]  # 구역 정보 추출
                row_info = int(alt_text.split("열-")[0].split()[-1].replace("열", ""))  # 열 정보 추출
                print(f"area_info={area_info}, row_info={row_info}")
                if area_info == "B구역" and row_info <= 10:
                    want_seat_list.append(seat)
                    flag = 1
                    break
            except (IndexError, ValueError) as e:
                # 예상치 못한 형식의 alt_text를 가진 요소가 있을 경우 무시
                print(f"Error parsing alt text: {e}")
                continue

# 조건에 맞는 좌석이 있으면 클릭
if flag == 1 and want_seat_list:
    target_seat = want_seat_list[0]
    print(f"Clicking on seat with alt text: {target_seat.get_attribute('alt')}")
    # 자바스크립트를 사용하여 요소 클릭
    driver.execute_script("arguments[0].click();", target_seat)
else:
    print("No seats found matching the criteria.")

driver.switch_to.window(driver.window_handles[-1])
iframes = driver.find_elements(By.TAG_NAME, "iframe")

for ifr in iframes:
    if ifr.get_attribute('name') == 'ifrmSeat':
        driver.switch_to.frame(ifr)
        break
if flag == 1:
    next_step_button = driver.find_element(By.XPATH, "//*[@id='NextStepImage']")
    driver.execute_script("arguments[0].click();", next_step_button)
time.sleep(200)
