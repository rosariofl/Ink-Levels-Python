from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from hp_printer_ip_list import ips
from color_printer_xpaths import ink_colors

chromedriver = r"C:\Users\luis\Documents\Projects\Query Printers\chromedriver.exe"

chrome_options = Options()
chrome_options.set_capability("acceptInsecureCerts", True)  # Makes it so Chrome does not show a SSL certificate error
chrome_options.add_argument("--headless")  # Stops Chrome GUI from opening
chrome_options.add_argument(
    '--log-level=3')  # Stops certain errors that do not stop the program from working (cleaner look)

# Assign the path of chromedriver and all the options
driver = webdriver.Chrome(executable_path=chromedriver, options=chrome_options)


def hp_printers():
    """ Print Ink levels of HP printers LaserJet Pro M404dn and LaserJet 500 MFP M525"""

    for ip in ips:
        try:
            print(ip)
            driver.get(ips[ip])
            driver.implicitly_wait(5)
            if ips[ip] == "https://10.200.100.71":
                ink_level = driver.find_element_by_id("SupplyPLR0")
                print(f"Black Ink level is at {ink_level.text.replace('*', '')}")
            else:
                ink_level = driver.find_element_by_xpath('//*[@id="blackInkLevel"]/div[2]/span')
                print(ink_level.get_attribute(
                    "textContent"))  # "textContent" used because text isn't displayed on the website (hidden).
            print("\n")
        except WebDriverException as e:
            print("There was an error.")
            print(f"{e} \n")
        except Exception:
            print("There was an error.")
            print(f"{e} \n")


def color_printer():
    """Prints ink levels of Epson printer HL-L8360CDW"""
    print("Office Color Printer")
    for ink in ink_colors:
        try:
            driver.get("https://10.200.100.73")
            driver.implicitly_wait(5)
            ink_level = driver.find_element_by_xpath(f"{ink_colors[ink]}")
            level = ink_level.get_attribute('height')
            # multiply level times 2, since ink levels go from 50 to 0. This will change to a 0 to 100% scale.
            total_ink_level = int(level) * 2
            print(f'{ink} Ink level is at {total_ink_level}%')
        except WebDriverException as e:
            print("There was an error.")
            print(f"{e} \n")
        except Exception:
            print("There was an error.")
            print(f"{e} \n")
    print("\n")


hp_printers()
color_printer()
driver.quit()

# Ask for input so windows doesn't close after all ink levels are checked.
input("Done?")