import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
from datetime import datetime

# --- Configuration ---
WCA_ID_TO_USE = ""
BIRTH_YEAR = ""
BIRTH_MONTH = ""
BIRTH_DAY = ""
EMAIL_ADDRESS = ""
EVENT_ID_TO_CLICK = ""
start_time=""
user_info = {
    "WCAID":"",
    "birthyear":"",
    "birthmonth":"",
    "birthday":"",
    "email":""
}
all_event = {
    '33':'form_event_33','22':'form_event_22','44':'form_event_44','55':'form_event_55',
    '66':'form_event_66','77':'form_event_77','3bld':'form_event_3bld',
    '3fmc':'form_event_3fmc','3oh':'form_event_3oh','clock':'form_event_clock',
    'mega':'form_event_mega','pyra':'form_event_pyra','skewb':'form_event_skewb',
    'sq1':'form_event_sq1','4bld':'form_event_4bld','5bld':'form_event_5bld',
    'mbld':'form_event_mbld'
}
event_to_click = {
    '33':False,'22':False,'44':False,'55':False,'66':False,'77':False,
    '3bld':False,'3fmc':False,'3oh':False,'clock':False,'mega':False,'pyra':False,
    'skewb':False,'sq1':False,'4bld':False,'5bld':False,'mbld':False
}
WAIT_TIMEOUT = 0.1
SHORT_PAUSE = 0.35  # Seconds
LONGER_PAUSE = 5.0 # Seconds
mag = 10 #webpage size(%)
action_taken = False
wcaid_action = True
send_register = False

# --- time and links ---
TARGET_URL = ""
target_hour = 0
target_minute = 0
starttime=time.time()
starttime_2=time.time()

# --- rickroll ---
print("""Never gonna give you up 
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give you up 
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give never gonna give
Never gonna give never gonna give\n""")

# --- Main Script-1 ---
TARGET_URL = input("The register page(like https://cubing-tw.net/event/xxxx/registration):\n")
# --- Main Script-1 ---

# --- tk's element ---
root = tk.Tk()
root.title("informations")
labels = {}
entries = {}

# --- many time asking [Y/n] ---
def manyinput(question):
    ans=input(question)
    while ans != "Y" and ans!= "y" and ans != "N" and ans != "n":
        print("Please answer again.")
        ans=input(question)
    if ans == "Y" or ans == "y" :
        return True
    else:
        return False

# --- Helper Function for Safe Clicking ---
# Tries standard click, falls back to JavaScript click if intercepted
def safe_click(driver, locator, timeout=WAIT_TIMEOUT):
    try:
        element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
        element.click()
        print(f"Clicked element: {locator}")
        return True
    except:
        pass
    return False

# --- Helper Function for Sending Keys ---
def safe_send_keys(driver, locator, value, timeout=WAIT_TIMEOUT):
    try:
        element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(value)
        print(f"Sent keys '{value}' to element: {locator}")
        return True
    except:
        pass
    return False

# --- Helper Function for Selecting Dropdown Value ---
def safe_select_value(driver, locator, value, timeout=WAIT_TIMEOUT):
    try:
        select_element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
        select_obj = Select(select_element)
        select_obj.select_by_value(value)
        print(f"Selected value '{value}' in dropdown: {locator}")
        return True
    except:
        pass
    return False

# --- wait to start ---
def wait_until_target():
    while True:
        now = datetime.now()
        if now.hour > target_hour or (now.hour == target_hour and now.minute >= target_minute):
            print("Now time: ", now.strftime("%H:%M"))
            print("Code will start now.")
            return
        else:
            print("Now time: ", now.strftime("%H:%M"), f", it's earlier than {target_hour}:{target_minute}.\nWaiting...")
            time.sleep(60)  # check every 60 seconds

# --- item change in tk ---
def toggle_item(item):
    event_to_click[item] = not event_to_click[item]
    if event_to_click[item]:
        labels[item].config(text=f"{item}: True",fg="green")
    else:
        labels[item].config(text=f"{item}: False",fg="red")

# --- submit and close in tk ---
def submit():
    for key in entries:
        user_info[key] = entries[key].get()
    print("\nYour datas\n")
    for key, value in user_info.items():
        print(f"{key}: \"{value}\"")
    print("\nYour events\n")
    for k, v in event_to_click.items():
        if v :
            print(k)
    root.destroy()

def input_user_data():
    tk.Label(root, text="Datas", font=('Arial', 15, 'bold')).pack(pady=10)
    for key in user_info:
        frame = tk.Frame(root)
        frame.pack(pady=5)
        tk.Label(frame, text=key + ":", width=12, anchor='w').pack(side=tk.LEFT)
        entry = tk.Entry(frame, width=25)
        entry.pack(side=tk.LEFT)
        entries[key] = entry
    tk.Label(root, text="Events", font=('Arial', 15, 'bold')).pack(pady=15)
    task_frame = tk.Frame(root)
    task_frame.pack()
    for idx, item in enumerate(event_to_click):
        frame = tk.Frame(task_frame)
        frame.pack(pady=3)
        label = tk.Label(frame, text=f"{item}: False", font=('Arial', 12),fg="red")
        label.pack(side=tk.LEFT)
        labels[item] = label
        btn = tk.Button(frame, text="button", command=lambda i=item: toggle_item(i))
        btn.pack(side=tk.LEFT, padx=5)
    tk.Button(root, text="submit", command=submit, bg='lightblue').pack(pady=20)
    root.mainloop()

# --- Main Script-2 ---
input_user_data()
WCA_ID_TO_USE = user_info['WCAID']
BIRTH_YEAR = user_info['birthyear']
BIRTH_MONTH = user_info['birthmonth']
BIRTH_DAY = user_info['birthday']
EMAIL_ADDRESS = user_info['email']

driver = None
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(2)
print(f"\nNavigating to {TARGET_URL}")
driver.get(TARGET_URL)
driver.execute_script(f"document.body.style.zoom='{mag}%'")

if not manyinput("Do you want to start now [Y/n]? [Y/n] ") :
    start_time=input("Type the time you want to start(in 24-hour system, like xx:xx): ")
    for i in range(len(start_time)):
        if start_time[i] == ":" :
            target_hour=int(start_time[:i])
            target_minute=int(start_time[i+1:])
            break
    wait_until_target()
print("Code start!")

# time.sleep(2)
try:
    while 'payment' not in driver.current_url:
        WebDriverWait(driver, 10)
        action_taken = False

        # --- Block 1: Check for 'GO' button ---
        if driver.current_url == TARGET_URL:
            driver.execute_script(f"document.body.style.zoom='{mag}%'")
            print("\nChecking for 'START' button...")
            try:
                notyet = driver.find_elements(By.CSS_SELECTOR, '.btn.btn-secondary.disabled')
                if notyet:
                    print("Register not start. The page will refresh.")
                    time.sleep(WAIT_TIMEOUT)
                    driver.refresh()
                    driver.execute_script(f"document.body.style.zoom='{mag}%'")
                    continue
                starttime=time.time()
                go_buttons = driver.find_elements(By.CSS_SELECTOR, '.btn.btn-primary')
                if go_buttons:
                    print("Found 'START' button.")
                    starttime_2=time.time()
                    if safe_click(driver, (By.CSS_SELECTOR, '.btn.btn-primary'), timeout=WAIT_TIMEOUT):
                        action_taken = True
                        print("'START' button clicked successfully.")
                        continue
                    else:
                        print("Failed to click 'START' button.")
                else:
                    print("'START' button not found.")
            except:
                pass
        
        # --- Block 2: Check for WCA ID Input ---
        if 'select' in driver.current_url:
            driver.execute_script(f"document.body.style.zoom='{mag}%'")
            print("\nChecking for WCA ID input section...")
            try:
                WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"]')))
                print("Found WCA ID input field.")
                wcaid_action = True # Mark action as potentially taken
                time.sleep(SHORT_PAUSE) # Mimic first 350ms timeout
                if not safe_send_keys(driver, (By.CSS_SELECTOR, 'input[type="text"]'), WCA_ID_TO_USE):
                    print("Input WCAID to 'WCAID_input' failed.")
                    wcaid_action = False
                if wcaid_action:
                    print("Waiting for WCAID checking...")
                    WebDriverWait(driver, 5).until(lambda d: "is-valid" in d.find_element(By.CSS_SELECTOR, 'input[type="text"]').get_attribute("class"))
                    if not safe_click(driver, (By.ID, 'WCAID_Button')):
                        print("Failed to click WCAID_Button.")
                        # action_taken = False
                    else:
                        print("WCA ID submitted successfully.")
                else: 
                    print("WCA ID section interaction failed.")
            except:
                pass

        # --- Block 3: Check for Preview Button (Main Form) ---
        if 'form' in driver.current_url:
            driver.execute_script(f"document.body.style.zoom='{mag}%'")
            print("\nChecking for information fields and preview button...")
            try:
                WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.ID, 'BTN_Preview')))
                print("Fields and button Found.\nProceeding with form fill.")
                # form_filled_successfully = True
                print("Filling form...")
                if not safe_select_value(driver, (By.ID, 'form_birthday_year'), BIRTH_YEAR):
                    print("Filled 'form_birthday_year' failed.")
                    # form_filled_successfully = False
                if not safe_select_value(driver, (By.ID, 'form_birthday_month'), BIRTH_MONTH):
                    print("Filled 'form_birthday_month' failed.")
                    # form_filled_successfully = False
                if not safe_select_value(driver, (By.ID, 'form_birthday_day'), BIRTH_DAY):
                    print("Filled 'form_birthday_day' failed.")
                    # form_filled_successfully = False
                if not safe_send_keys(driver, (By.ID, 'form_email'), EMAIL_ADDRESS):
                    print("Filled 'form_email' failed.")
                    # form_filled_successfully = False
                # Click the event checkbox
                for k,b in event_to_click.items():
                    if b:
                        EVENT_ID_TO_CLICK = all_event[k]
                        if not safe_click(driver, (By.ID, EVENT_ID_TO_CLICK)): 
                            print(f"Click {EVENT_ID_TO_CLICK} failed.")
                            # form_filled_successfully = False

            # if form_filled_successfully: (this chunck miss a tab.
                print(f"Form fields filled/clicked. Waiting {SHORT_PAUSE}s before clicking Preview.")
                time.sleep(SHORT_PAUSE) # Mimic 350ms timeout
                if safe_click(driver, (By.ID, 'BTN_Preview')):
                    print(f"Clicked Preview. Waiting {LONGER_PAUSE}s before clicking Send.")
                    time.sleep(LONGER_PAUSE) # Mimic 5000ms timeout
                    if safe_click(driver, (By.ID, 'BTN_Send')):
                        action_taken = True
                        send_register = True
                        print("Clicked Send successfully. Registration likely submitted.")
                        continue
                    else:
                        print("Failed to click Send button.")
                        action_taken = False
                else:
                    print("Failed to click Preview button.")
                    # action_taken = False
            # else:
            #     print("Failed to fill one or more form fields or click event.")
            #     action_taken = False
            
            except:
                pass
        
        # --- Block 4: Reload if no action was taken ---
        if not action_taken:
            print(f"\nNo specific actions were successfully completed. Reloading page in {WAIT_TIMEOUT}s...")
            time.sleep(WAIT_TIMEOUT)
            driver.refresh()
            driver.execute_script(f"document.body.style.zoom='{mag}%'")
            print("Page reloaded.")

except:
    pass

finally:
    if send_register :
        print(f"\nAll finished successfully.\nTotal time: {time.time()-starttime}s.\nRegister time: {time.time()-starttime_2}s.")
        print("You can pay money for the contest now.")
    else :
        print(f"\nRegister failed.\nTotal time: {time.time()-starttime}s.\nRegister time: {time.time()-starttime_2}s.")
    input("\nPress Enter to stop the code.")
    print("Closing WebDriver...")
    driver.quit()
