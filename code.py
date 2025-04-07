import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, ElementNotInteractableException
import tkinter as tk

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

# TARGET_URL = "file:///home/linuk/Downloads/TWCA%E5%A0%B1%E5%90%8D%E6%B8%AC%E8%A9%A6%E7%B6%B2%E7%AB%99%E7%AC%AC%E9%9B%B6%E9%83%A8%E5%88%86.html"
# TARGET_URL = "https://cubing-tw.net/event/2025ZhongshanOpen/registration"
TARGET_URL = input("The register page(like https://cubing-tw.net/event/xxxx/registration):\n")

root = tk.Tk()
root.title("imformations")
labels = {}
entries = {}

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

def toggle_item(item):
    event_to_click[item] = True
    labels[item].config(text=f"{item}: True",fg="green")

for idx, item in enumerate(event_to_click):
    frame = tk.Frame(task_frame)
    frame.pack(pady=3)
    label = tk.Label(frame, text=f"{item}: False", font=('Arial', 12),fg="red")
    label.pack(side=tk.LEFT)
    labels[item] = label
    btn = tk.Button(frame, text="button", command=lambda i=item: toggle_item(i))
    btn.pack(side=tk.LEFT, padx=5)

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

tk.Button(root, text="submit", command=submit, bg='lightblue').pack(pady=20)

root.mainloop()
WCA_ID_TO_USE = user_info['WCAID']
BIRTH_YEAR = user_info['birthyear']
BIRTH_MONTH = user_info['birthmonth']
BIRTH_DAY = user_info['birthday']
EMAIL_ADDRESS = user_info['email']

WAIT_TIMEOUT = 0.1
SHORT_PAUSE = 0.35  # Seconds (equiv. to 500ms in JS)
MEDIUM_PAUSE = 1.0 # Seconds (used before clicking Go Button)
LONGER_PAUSE = 3.5 # Seconds (equiv. to 4000ms in JS before Preview)

# --- Helper Function for Safe Clicking ---
# Tries standard click, falls back to JavaScript click if intercepted
def safe_click(driver, locator, timeout=WAIT_TIMEOUT):
    try:
        element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
        element.click()
        print(f"Clicked element: {locator}")
        return True
    
    except TimeoutException:
        print(f"Timeout waiting for element {locator} to be clickable.")
    
    except ElementClickInterceptedException:
        print(f"Element {locator} click intercepted. Trying JavaScript click.")
        try:
            # Find element again without wait, as it must exist if intercepted
            element = driver.find_element(*locator)
            driver.execute_script("arguments[0].click();", element)
            print(f"Clicked element using JavaScript: {locator}")
            return True
        
        except Exception as e_js:
            print(f"JavaScript click also failed for {locator}: {e_js}")
    
    except Exception as e:
        print(f"Error clicking element {locator}: {e}")
    
    return False

# --- Helper Function for Sending Keys ---
def safe_send_keys(driver, locator, value, timeout=WAIT_TIMEOUT):
    try:
        element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(value)
        print(f"Sent keys '{value}' to element: {locator}")
        return True
    
    except TimeoutException:
        print(f"Timeout waiting for element {locator} to be visible.")
    
    except Exception as e:
        print(f"Error sending keys to element {locator}: {e}")
    
    return False

# --- Helper Function for Selecting Dropdown Value ---
def safe_select_value(driver, locator, value, timeout=WAIT_TIMEOUT):
    try:
        select_element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
        select_obj = Select(select_element)
        select_obj.select_by_value(value)
        print(f"Selected value '{value}' in dropdown: {locator}")
        return True
    
    except TimeoutException:
        print(f"Timeout waiting for dropdown element {locator} to be present.")
    
    except NoSuchElementException:
        # This can happen if the specific *value* doesn't exist in the options
        print(f"Could not find option with value '{value}' in dropdown {locator}.")
    
    except ElementNotInteractableException:
         print(f"Dropdown {locator} found but is not interactable.")
    
    except Exception as e:
        print(f"Error selecting value in dropdown {locator}: {e}")
    
    return False

# --- Main Script ---
driver = None
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(2)

print(f"\nNavigating to {TARGET_URL}")
driver.get(TARGET_URL)

action_taken = False # Flag similar to 'reload' variable in JS

# --- Block 1: Check for 'GO' button ---
# JS uses getElementsByClassName, which returns a list. It incorrectly tries
# to click the list. We'll find elements and click the first one if it exists.
# Using CSS Selector for '.btn.btn-primary' is more robust.
# time.sleep(2)

input("Press enter to start")

try:
    start_time=time.time()
    while True :
        WebDriverWait(driver, 10)
        action_taken = False
        try:
            if driver.current_url == TARGET_URL:
                notyet = driver.find_elements(By.CSS_SELECTOR, '.btn.btn-secondary.disabled')
                if notyet:
                    print("Register not start.The page will refresh.")
                    time.sleep(WAIT_TIMEOUT)
                    driver.refresh()
                    continue
                print("Checking for 'GO' button (class='btn btn-primary')...")
                go_buttons = driver.find_elements(By.CSS_SELECTOR, '.btn.btn-primary')
                if go_buttons:
                    print("Found 'GO' button(s). Attempting to click the first one.")
                    if safe_click(driver, (By.CSS_SELECTOR, '.btn.btn-primary'), timeout=WAIT_TIMEOUT):
                        action_taken = True
                        print("'GO' button clicked successfully.")
                    else:
                        print("Failed to click 'GO' button.")
                else:
                    print("'GO' button not found.")
        
        except Exception as e:
            # Catch broad exceptions since find_elements itself shouldn't raise NoSuchElement
            print(f"An error occurred while checking/clicking the 'GO' button: {e}")

        # --- Block 2: Check for WCA ID Input ---
        # Only proceed if the previous action wasn't taken
        if not action_taken:
            print("\nChecking for WCA ID input section...")
            try:
                WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.ID, 'WCAID_input')))
                print("Found WCA ID input field.")
                action_taken = True # Mark action as potentially taken
                time.sleep(SHORT_PAUSE) # Mimic first 500ms timeout
                if not safe_click(driver, (By.ID, 'WCAID_input')): action_taken = False
                if action_taken and not safe_send_keys(driver, (By.ID, 'WCAID_input'), WCA_ID_TO_USE): action_taken = False
                if action_taken:
                    time.sleep(1.5) # Mimic second 1500ms timeout
                    if not safe_click(driver, (By.ID, 'WCAID_Button')):
                        action_taken = False
                        print("Failed to click WCAID_Button.")
                    else: print("WCA ID submitted successfully.")
                else: print("WCA ID section interaction failed.")
            
            except (NoSuchElementException, TimeoutException):
                print("WCA ID input section not found or timed out.")
                action_taken = False # Ensure flag is false if elements not found
            
            except Exception as e:
                print(f"An error occurred during WCA ID processing: {e}")
                action_taken = False

        # --- Block 3: Check for Preview Button (Main Form) ---
        if not action_taken:
            print("\nChecking for Preview button (main registration form)...")
            try:
                WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.ID, 'BTN_Preview')))
                print("Found Preview button. Proceeding with form fill.")
                action_taken = True # Mark action as potentially taken
                form_filled_successfully = True
                print("Filling form...")
                # if not safe_click(driver, (By.ID, 'form_birthday_year')): form_filled_successfully = False
                # if not safe_send_keys(driver, (By.ID, 'form_birthday_year'), BIRTH_YEAR): form_filled_successfully = False
                # if not safe_click(driver, (By.ID, 'form_birthday_minth')): form_filled_successfully = False
                # if not safe_send_keys(driver, (By.ID, 'form_birthday_month'), BIRTH_MONTH): form_filled_successfully = False
                # if not safe_click(driver, (By.ID, 'form_birthday_day')): form_filled_successfully = False
                # if not safe_send_keys(driver, (By.ID, 'form_birthday_day'), BIRTH_DAY): form_filled_successfully = False
                # if not safe_click(driver, (By.ID, 'form_email')): form_filled_successfully = False
                # if not safe_send_keys(driver, (By.ID, 'form_email'), EMAIL_ADDRESS): form_filled_successfully = False

                if not safe_select_value(driver, (By.ID, 'form_birthday_year'), BIRTH_YEAR): form_filled_successfully = False
                if not safe_select_value(driver, (By.ID, 'form_birthday_month'), BIRTH_MONTH): form_filled_successfully = False
                if not safe_select_value(driver, (By.ID, 'form_birthday_day'), BIRTH_DAY): form_filled_successfully = False
                # --- Use safe_send_keys for regular input ---
                if not safe_send_keys(driver, (By.ID, 'form_email'), EMAIL_ADDRESS): form_filled_successfully = False
                # Click the event checkbox
                for k,b in event_to_click.items():
                    if b:
                        EVENT_ID_TO_CLICK = all_event[k]
                        if not safe_click(driver, (By.ID, EVENT_ID_TO_CLICK)): form_filled_successfully = False

                if form_filled_successfully:
                    print(f"Form fields filled/clicked. Waiting {LONGER_PAUSE}s before clicking Preview.")
                    time.sleep(SHORT_PAUSE) # Mimic 500ms timeout
                    if safe_click(driver, (By.ID, 'BTN_Preview')):
                        print(f"Clicked Preview. Waiting {SHORT_PAUSE}s before clicking Send.")
                        time.sleep(LONGER_PAUSE) # Mimic 4000ms timeout
                        if safe_click(driver, (By.ID, 'BTN_Send')):
                            print("Clicked Send successfully. Registration likely submitted.")
                        else:
                            print("Failed to click Send button.")
                            action_taken = False
                    else:
                        print("Failed to click Preview button.")
                        action_taken = False
                else:
                    print("Failed to fill one or more form fields or click event.")
                    action_taken = False
            
            except (NoSuchElementException, TimeoutException):
                print("Preview button / main form section not found or timed out.")
                action_taken = False
            
            except Exception as e:
                print(f"An error occurred during form filling/preview/send: {e}")
                action_taken = False
        
        # --- Block 4: Reload if no action was taken ---
        if not action_taken:
            print(f"\nNo specific actions were successfully completed. Reloading page in {WAIT_TIMEOUT}s...")
            time.sleep(WAIT_TIMEOUT)
            driver.refresh()
            print("Page reloaded.")
        else:
            print("\nScript finished actions.")
            print(f"Total time: {time.time()-start_time}")
        # if TARGET_URL not in driver.current_url:
        #     print("Finish successfully!")
        #     break

except Exception as e:
    print(f"\nAn unexpected error occurred in the main script: {e}")

finally:
    if driver:
        print("Closing WebDriver.")
        driver.quit()