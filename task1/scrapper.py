from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import time
import os

# Set up Chrome options
def setup_chrome_driver(download_dir):
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Log into the website
def login(driver, username, password):
    driver.get("https://app.cosmosid.com/sign-in")
    time.sleep(5)
    
    # Close initial pop-up
    try:
        close_initial_popup(driver)
    except Exception as e:
        print(f"Initial pop-up not found or failed to close: {e}")
    
    # Enter login credentials
    username_input = driver.find_element(By.ID, "sign-in-form--email")
    password_input = driver.find_element(By.ID, "sign-in-form--password")
    login_button = driver.find_element(By.ID, "sign-in-form--submit")
    
    username_input.send_keys(username)
    password_input.send_keys(password)
    time.sleep(1)
    login_button.click()
    time.sleep(10)
    
    # Close post-login pop-up
    try:
        close_post_login_popup(driver)
    except Exception as e:
        print(f"Failed to close post-login pop-up: {e}")

def close_initial_popup(driver):
    close_button = driver.find_element(By.ID, "new-features-dialog--close")
    close_button.click()
    print("Initial pop-up closed successfully.")
    time.sleep(1)

def close_post_login_popup(driver):
    close_button_post_login = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "intro-tour--functional-2-tour--close-button"))
    )
    close_button_post_login.click()
    print("Post-login pop-up closed successfully.")

def click_on_taxonomy_level(driver):
        div_element = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.ID, "artifact-select-button-biom"))
        )[0]
        div_element.click()
        time.sleep(5)
        div_element = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.ID, "artifact-options-select"))
        )[0]
        div_element.click()
        time.sleep(2)

        ul_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.MuiList-root.MuiList-padding.MuiMenu-list')))

        if ul_elements:
            last_ul_element = ul_elements[-1]
            li_elements = last_ul_element.find_elements(By.CSS_SELECTOR, 'li.MuiButtonBase-root.MuiMenuItem-root')
            for i in range(len(li_elements)):
                if i>0:
                    # after first iteration, reload the full dom to get access
                    div_element = WebDriverWait(driver, 10).until(
                            EC.presence_of_all_elements_located((By.ID, "artifact-options-select"))
                    )[0]
                    div_element.click()
                    time.sleep(2)
                ul_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.MuiList-root.MuiList-padding.MuiMenu-list')))
                last_ul_element = ul_elements[-1]
                li_elements = last_ul_element.find_elements(By.CSS_SELECTOR, 'li.MuiButtonBase-root.MuiMenuItem-root')
                li = li_elements[i]
                li.click()
                print(f'Clicked on level: {li.text}')
                handle_export(driver)
                time.sleep(2)

def click_all_options(driver):
    print('click on click options')
    div_element = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.ID, "analysis-select"))
    )[0]
    div_element.click()
    time.sleep(2)
    div_element = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.ID, "analysis-select"))
        )[0]
    div_element.click()
    time.sleep(2)
    ul_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.MuiList-root.MuiList-padding.MuiMenu-list.css-r8u8y9')))
   
    if ul_elements:
    
        last_ul_element = ul_elements[-1]
  
        li_elements = last_ul_element.find_elements(By.CSS_SELECTOR, 'li.MuiButtonBase-root.MuiMenuItem-root.MuiMenuItem-gutters.MuiMenuItem-root.MuiMenuItem-gutters.css-2aj19w')
        print(len(li_elements))
        for i in range(len(li_elements)):
            if i>0:
                # after first iteration, reload the full dom to get access
                div_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.ID, "analysis-select"))
                )[0]
                div_element.click()
                time.sleep(2)
            ul_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.MuiList-root.MuiList-padding.MuiMenu-list.css-r8u8y9')))
            last_ul_element = ul_elements[-1]
            li_elements = last_ul_element.find_elements(By.CSS_SELECTOR, 'li.MuiButtonBase-root.MuiMenuItem-root.MuiMenuItem-gutters.MuiMenuItem-root.MuiMenuItem-gutters.css-2aj19w')
            li = li_elements[i]
            li.click()
            print(f'Clicked on results: {li.text}')
            if li.text == 'Bacteria':
                print('go to taxonomy switchen')
                click_on_taxonomy_level(driver=driver)
            else:
                print('download the file')
                handle_export(driver)
            time.sleep(2)

def interact_with_table(driver):
    time.sleep(1)
    rows = get_table_rows(driver)

    for category_index in range(len(rows)):
        time.sleep(1)
        rows = get_table_rows(driver)
        category_row = rows[category_index]
        try:
            # Click on the second <td> in the category row
            second_td = WebDriverWait(category_row, 10).until(
                EC.presence_of_element_located((By.XPATH, './td[2]'))
            )
            second_td.click()
            time.sleep(2)

            # Click on the <a> tag inside the second <td>
            a_element = WebDriverWait(second_td, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'a'))
            )
            category = a_element.text
            a_element.click()
            time.sleep(2)

            # Re-fetch the table rows for the current category
            sub_rows = get_table_rows(driver)
            print('Total rows:', len(sub_rows))

            for sub_row_index in range(len(sub_rows)):
                sub_rows = get_table_rows(driver)
                sub_row = sub_rows[sub_row_index]
                try:
                    # Click on the first <td> in the sub row
                    first_td = WebDriverWait(sub_row, 10).until(
                        EC.presence_of_element_located((By.XPATH, './td[1]'))
                    )
                    first_td.click()
                    time.sleep(1)

                    # Click on the second <td> in the sub row
                    second_td = WebDriverWait(sub_row, 10).until(
                        EC.presence_of_element_located((By.XPATH, './td[2]'))
                    )
                    a_element = WebDriverWait(second_td, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, 'a'))
                    )
                    print(f'Downloaded file: ({sub_row_index + 1}) -> {a_element.text}')

                    #comment to check
                    second_td.click()
                    time.sleep(2)

                    click_all_options(driver=driver)

                    driver.back()
                    time.sleep(2)  

                except Exception as e:
                    print(f"Error interacting with sub row {sub_row_index}: {e}")

            print(f'{category} section done...')
            my_samples_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'My Samples')]"))
            )
            my_samples_link.click()
            time.sleep(2)  # Wait for the page to load back

        except Exception as e:
            print(f"Error interacting with category row {category_index}: {e}")

def get_table_rows(driver):
    """Fetches the rows from the table body."""
    table_body = driver.find_element(By.CLASS_NAME, 'MuiTableBody-root')
    return table_body.find_elements(By.CLASS_NAME, 'MuiTableRow-root')
               

# Handle the export functionality
def handle_export(driver):
    try:
        export_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export current results')]"))
        )
        export_button.click()
        print("Export button clicked.")
        time.sleep(2)
    except TimeoutException:
        print("Export button not found, skipping export.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Main execution flow
def main():
    download_folder = os.path.abspath('../task2-3/downloads')
    driver = setup_chrome_driver(download_folder)
    
    try:
        login(driver, "demo_estee2@cosmosid.com", "xyzfg321")
        interact_with_table(driver)
    finally:
        input("Press Enter to close the browser...")
        driver.quit()

if __name__ == "__main__":
    main()
