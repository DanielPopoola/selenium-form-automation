import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fill_google_form():
    driver = webdriver.Chrome()
    form_url = "https://forms.gle/WT68aV5UnPajeoSc8"
    
    data = [
        "Daniel Popoola",
        "9015512956",       
        "iamuchihadaniel236@gmail.com",
        "400001",           
        "06/23/2004",
        "Male",
        "GNFPYC",
    ]
    
    try:
        driver.get(form_url)
        
        # Wait for form to be ready
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "Xb9hP"))
        )

        containers = driver.find_elements(By.CLASS_NAME, "Xb9hP")
        
        input_fields = []
        for container in containers:
            try:
                field = container.find_element(By.TAG_NAME, "input")
                input_fields.append(field)
            except:
                pass
        
        print(f"Found {len(input_fields)} input fields")
        
        for i, (field, value) in enumerate(zip(input_fields, data)):
            try:
                #driver.execute_script("arguments[0].scrollIntoView(true);", field)
                #time.sleep(0.3)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(field))
                field.click()
                if i == 4:
                    driver.execute_script("arguments[0].value = '2004-06-23';", field)
                    driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", field)
                    driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", field)
                else:
                    field.send_keys(value)
                    #print(f"Filled field {i}: {value}")
                
            except Exception as e:
                print(f"Error filling field {i}: {e}")
        
        address_field = driver.find_element(By.CSS_SELECTOR, "textarea.KHxj8b.tL9Q4c")
        address_field.send_keys("123 Main St, City")

        submit_button = driver.find_element(By.XPATH, "//span[text()='Submit']")
        submit_button.click()

        time.sleep(5)

        driver.save_screenshot("screenshots/confirmation.png")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    fill_google_form()