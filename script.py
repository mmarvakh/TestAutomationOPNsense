from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from config import (
    WAN_ADDRESS_OPN,
    USERNAME_OPN,
    PASSWORD_OPN,
    VMNET1_ADDRESS_OPN,
    VMNET2_ADDRESS_OPN,
    NAT_ADDRESS_OPN
)


# Creating and setting up Google Chrome driver
driver_service = Service(ChromeDriverManager().install())
chr_options = Options()
chr_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=driver_service, options=chr_options)


# Apply changes after creating rules
def apply_changes(driver: webdriver) -> None:
    btn_apply = driver.find_element(By.XPATH, "//button[@value='Apply changes']")
    btn_apply.click()


# Save new rule
def save(driver: webdriver) -> None:
    save_btn = driver.find_element(By.NAME, "Submit")
    driver.execute_script("arguments[0].click();", save_btn)


# NAT configuration setup
def nat_config(driver: webdriver, url: str, address_destination: str, port_destination_from: str,
               port_destination_to: str, redirect_target_ip: str, redirect_target_port) -> None:
    driver.get(url)

    btn_destination = driver.find_element(By.XPATH, "//button[@data-id='dst']")
    btn_destination.click()

    destination_input = driver.find_element(By.XPATH, "//form[@id='iform']//tr[24]//input[1]")
    destination_input.send_keys(address_destination)
    destination_input.send_keys(Keys.ENTER)

    btn_destination_port = driver.find_element(By.XPATH, "//button[@data-id='dstbeginport']")
    btn_destination_port.click()

    port_destination_input = driver.find_element(By.XPATH, "//form[@id='iform']//tr[26]//input[1]")
    port_destination_input.send_keys("other")
    port_destination_input.send_keys(Keys.ENTER)

    driver.find_element(By.XPATH, "//input[@for='dstbeginport']").clear()
    port_destination_from_input = driver.find_element(By.XPATH, "//input[@for='dstbeginport']")
    port_destination_from_input.send_keys(port_destination_from)

    driver.find_element(By.XPATH, "//input[@for='dstendport']").clear()
    port_destination_to_input = driver.find_element(By.XPATH, "//input[@for='dstendport']")
    port_destination_to_input.send_keys(port_destination_to)

    redirect_target_ip_input = driver.find_element(By.ID, "target_address")
    redirect_target_ip_input.send_keys(redirect_target_ip)

    btn_redirect_target_port = driver.find_element(By.XPATH, "//button[@data-id='localbeginport']")
    btn_redirect_target_port.click()

    redirect_target_port_input = driver.find_element(By.XPATH, "//form[@id='iform']//tr[30]//input[1]")
    redirect_target_port_input.send_keys(redirect_target_port)
    redirect_target_port_input.send_keys(Keys.ENTER)

    save(driver)
    apply_changes(driver)


# Create new rule with options
def add_rule(driver: webdriver, url: str, protocol: str,
             network_source: str, network_destination: str) -> None:
    driver.get(url)

    btn_protocol = driver.find_element(By.XPATH, "//button[@data-id='proto']")
    btn_protocol.click()

    protocol_input = driver.find_element(By.XPATH, "//form[@id='iform']//tr[17]//input[1]")
    protocol_input.send_keys(protocol)
    protocol_input.send_keys(Keys.ENTER)

    btn_source = driver.find_element(By.XPATH, "//button[@data-id='src']")
    btn_source.click()

    source_input = driver.find_element(By.XPATH, "//form[@id='iform']//tr[25]//input[1]")
    source_input.send_keys(network_source)
    source_input.send_keys(Keys.ENTER)

    btn_destination = driver.find_element(By.XPATH, "//button[@data-id='dst']")
    btn_destination.click()

    destination_input = driver.find_element(By.XPATH, "//form[@id='iform']//tr[33]//input[1]")
    destination_input.send_keys(network_destination)
    destination_input.send_keys(Keys.ENTER)

    save(driver)
    apply_changes(driver)


# Login to OPNsense web GUI
def login(driver: webdriver) -> None:
    driver.get(WAN_ADDRESS_OPN)

    username_input = driver.find_element(By.NAME, "usernamefld")
    username_input.send_keys(USERNAME_OPN)

    password_input = driver.find_element(By.NAME, "passwordfld")
    password_input.send_keys(PASSWORD_OPN)

    btn_log_in = driver.find_element(By.NAME, "login")
    btn_log_in.click()


# Run script
def run() -> None:
    login(driver)
    add_rule(driver, VMNET1_ADDRESS_OPN, "TCP/UDP", "Vmnet1 net", "Vmnet2 net")
    add_rule(driver, VMNET2_ADDRESS_OPN, "TCP/UDP", "Vmnet2 net", "Vmnet1 net")
    nat_config(driver, NAT_ADDRESS_OPN, "WAN address", "81", "81", "192.168.10.1", "HTTP")
