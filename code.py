import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, ElementNotInteractableException
import tkinter as tk
from datetime import datetime

# --- Configuration ---
WCA_ID_TO_USE = ""
BIRTH_YEAR = ""
BIRTH_MONTH = ""
BIRTH_DAY = ""
EMAIL_ADDRESS = ""
EVENT_ID_TO_CLICK = ""
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
SHORT_PAUSE = 0.35  # Seconds (equiv. to 500ms in JS)
MEDIUM_PAUSE = 1.0 # Seconds (used before clicking Go Button)
LONGER_PAUSE = 3.5 # Seconds (equiv. to 4000ms in JS before Preview)
action_taken = False # Flag similar to 'reload' variable in JS

# --- time and links ---
TARGET_URL = ""
target_hour = 0
target_minute = 00
start_time=time.time()

# --- tk's element ---
root = tk.Tk()
root.title("imformations")
labels = {}
entries = {}

# --- many time asking [Y/n] ---
def manyinput(question):
    ans=""
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
    #--- debuger ---
    # except TimeoutException:
    #     print(f"Timeout waiting for element {locator} to be clickable.")
    # except ElementClickInterceptedException:
    #     print(f"Element {locator} click intercepted. Trying JavaScript click.")
    #     try:
    #         # Find element again without wait, as it must exist if intercepted
    #         element = driver.find_element(*locator)
    #         driver.execute_script("arguments[0].click();", element)
    #         print(f"Clicked element using JavaScript: {locator}")
    #         return True
    #     except Exception as e_js:
    #         print(f"JavaScript click also failed for {locator}: {e_js}")
    # except Exception as e:
    #     print(f"Error clicking element {locator}: {e}")
    #--- debuger ---

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
    #--- debuger ---
    # except TimeoutException:
    #     print(f"Timeout waiting for element {locator} to be visible.")
    # except Exception as e:
    #     print(f"Error sending keys to element {locator}: {e}")
    #--- debuger ---
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
    #--- debuger ---
    # except TimeoutException:
    #     print(f"Timeout waiting for dropdown element {locator} to be present.")
    # except NoSuchElementException:
    #     # This can happen if the specific *value* doesn't exist in the options
    #     print(f"Could not find option with value '{value}' in dropdown {locator}.")
    # except ElementNotInteractableException:
    #      print(f"Dropdown {locator} found but is not interactable.")
    # except Exception as e:
    #     print(f"Error selecting value in dropdown {locator}: {e}")
    #--- debuger ---
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

# --- Main Script ---
TARGET_URL = input("The register page(like https://cubing-tw.net/event/xxxx/registration):\n")

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

if not manyinput("Do you want to start now[Y/n]?") :
    target_hour = int(input("Type the hour you want to start(in 24-hour system): "))
    target_minute = int(input("Type the minute you want to start: "))
    wait_until_target()
    print("Code start!")
else:
    print("Code start!")

# time.sleep(2)
try:
    while 'payment' not in driver.current_url:
        WebDriverWait(driver, 10)
        action_taken = False

        # --- Block 1: Check for 'GO' button ---
        # JS uses getElementsByClassName, which returns a list. It incorrectly tries
        # to click the list. We'll find elements and click the first one if it exists.
        # Using CSS Selector for '.btn.btn-primary' is more robust.
        if driver.current_url == TARGET_URL:
            print("\nChecking for 'START' button...")
            try:
                notyet = driver.find_elements(By.CSS_SELECTOR, '.btn.btn-secondary.disabled')
                if notyet:
                    print("Register not start. The page will refresh.")
                    time.sleep(WAIT_TIMEOUT)
                    driver.refresh()
                    continue
                start_time=time.time()
                go_buttons = driver.find_elements(By.CSS_SELECTOR, '.btn.btn-primary')
                if go_buttons:
                    print("Found 'START' button.")
                    if safe_click(driver, (By.CSS_SELECTOR, '.btn.btn-primary'), timeout=WAIT_TIMEOUT):
                        action_taken = True
                        print("'START' button clicked successfully.")
                        continue
                    else:
                        print("Failed to click 'START' button.")
                else:
                    print("'START' button not found.")
        
            # --- debuger ---
            # except Exception as e:
            #     # Catch broad exceptions since find_elements itself shouldn't raise NoSuchElement
            #     print(f"An error occurred while checking/clicking the 'GO' button: {e}")
            # --- debuger ---
            except:
                pass
        
        # --- Block 2: Check for WCA ID Input ---
        # Only proceed if the previous action wasn't taken
        if 'select' in driver.current_url:
            print("\nChecking for WCA ID input section...")
            try:
                WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.ID, 'WCAID_input_MD2fg5')))
                print("Found WCA ID input field.")
                action_taken = True # Mark action as potentially taken
                time.sleep(SHORT_PAUSE) # Mimic first 500ms timeout
                if not safe_click(driver, (By.ID, 'WCAID_input_MD2fg5')): action_taken = False
                if action_taken and not safe_send_keys(driver, (By.ID, 'WCAID_input_MD2fg5'), WCA_ID_TO_USE): action_taken = False
                if action_taken:
                    time.sleep(1.5) # Mimic second 1500ms timeout
                    if not safe_click(driver, (By.ID, 'WCAID_Button')):
                        action_taken = False
                        print("Failed to click WCAID_Button.")
                    else: print("WCA ID submitted successfully.")
                else: print("WCA ID section interaction failed.")
            
            # --- debuger ---
            # except (NoSuchElementException, TimeoutException):
            #     print("WCA ID input section not found or timed out.")
            #     action_taken = False # Ensure flag is false if elements not found
            # except Exception as e:
            #     print(f"An error occurred during WCA ID processing: {e}")
            #     action_taken = False
            # --- debuger ---
            except:
                pass

        # --- Block 3: Check for Preview Button (Main Form) ---
        if 'form' in driver.current_url:
            print("\nChecking for information fields and preview button...")
            try:
                WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.ID, 'BTN_Preview')))
                print("Fields and button Found. Proceeding with form fill.")
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
                    time.sleep(LONGER_PAUSE) # Mimic 3500ms timeout
                    if safe_click(driver, (By.ID, 'BTN_Send')):
                        action_taken = True
                        print("Clicked Send successfully. Registration likely submitted.")
                        continue
                    else:
                        print("Failed to click Send button.")
                        # action_taken = False
                else:
                    print("Failed to click Preview button.")
                    # action_taken = False
            # else:
            #     print("Failed to fill one or more form fields or click event.")
            #     action_taken = False
            
            # --- debuger ---
            # except (NoSuchElementException, TimeoutException):
            #     print("Preview button / main form section not found or timed out.")
            #     action_taken = False
            # except Exception as e:
            #     print(f"An error occurred during form filling/preview/send: {e}")
            #     action_taken = False
            # --- debuger ---
            except:
                pass
        
        # --- Block 4: Reload if no action was taken ---
        if not action_taken:
            print(f"\nNo specific actions were successfully completed. Reloading page in {WAIT_TIMEOUT}s...")
            time.sleep(WAIT_TIMEOUT)
            driver.refresh()
            print("Page reloaded.")

# --- debuger ---
except Exception as e:
    print(f"\nAn unexpected error occurred in the main script: {e}")
# --- debuger ---

finally:
    print(f"\nAll finished successfully.\nTotal time: {time.time()-start_time}.")
    input("""You can pay money for the contest now.
          \nPress enter to stop the code.""")
    print("Closing WebDriver...")
    driver.quit()
