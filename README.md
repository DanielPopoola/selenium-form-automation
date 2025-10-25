# Google Forms Automation & Email Submission

A Python-based automation solution for filling Google Forms and sending assignment submissions via email. Built with Selenium WebDriver for form automation and Flask for programmatic email delivery.

## Overview

This project automates the complete workflow of:
1. Filling out a Google Form with required information
2. Capturing a confirmation screenshot
3. Sending a submission email with attachments via Flask

## Project Structure
```
.
├── selenium_form_filler.py    # Form automation script
├── email_utils.py              # Email sending logic (reusable)
├── app.py                      # Flask application
├── pyproject.toml            # Project dependencies
├── .env                        # Environment variables (not in git)
├── .gitignore                  # Git ignore rules
├── screenshots/                # Form confirmation screenshots
│   └── confirmation.png
└── attachments/                # Email attachments
    └── resume.pdf
```

## Technologies Used

- **Selenium WebDriver** - Browser automation
- **Flask** - Web framework for triggering email
- **smtplib** - Email sending via SMTP
- **python-dotenv** - Environment variable management

## Setup & Installation

### 1. Clone the Repository
```bash
git clone git@github.com:DanielPopoola/selenium-form-automation.git
cd form-automation
```

### 2. Install Dependencies
```bash
pip install .
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:
```env
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

**Note:** You need to generate a Gmail App Password:
1. Enable 2-Factor Authentication on your Google account
2. Go to Google Account → Security → App Passwords
3. Generate a password for "Mail" → "Other"
4. Use this 16-character password in your `.env` file

### 4. Prepare Attachments

- Place your resume as `attachments/resume.pdf`
- The confirmation screenshot will be auto-generated at `screenshots/confirmation.png`

## Usage

### Step 1: Run Form Automation
```bash
python selenium_form_filler.py
```

This will:
- Open Chrome browser
- Navigate to the Google Form
- Fill all required fields
- Submit the form
- Capture a screenshot of the confirmation page
- Save screenshot to `screenshots/confirmation.png`

### Step 2: Send Submission Email

Start the Flask server:
```bash
python app.py
```

Visit `http://localhost:5000/send-email` in your browser, or use curl:
```bash
curl http://localhost:5000/send-email
```

The email will be sent with all required attachments to the specified recipients.

## Technical Approach

### Form Automation Strategy

**Initial Challenge:** Google Forms use dynamic elements with shared CSS classes, making it difficult to target specific fields.

**Solution:** 
- Identified that form fields are wrapped in container divs with class `Xb9hP`
- Extracted all `<input>` elements from these containers
- Filled fields by their index position in the form
- Handled the address field separately (it's a `<textarea>`, not an `<input>`)

**Code snippet:**
```python
# Find all field containers
containers = driver.find_elements(By.CLASS_NAME, "Xb9hP")

# Extract input fields from containers
input_fields = []
for container in containers:
    try:
        field = container.find_element(By.TAG_NAME, "input")
        input_fields.append(field)
    except:
        pass  # Skip containers without inputs

# Fill by index
for i, (field, value) in enumerate(zip(input_fields, data)):
    field.send_keys(value)
```

### Email Automation Strategy

**Design Decision:** Separated email logic from Flask routes for:
- Reusability across different contexts
- Easier testing without running Flask
- Cleaner code organization

**Architecture:**
- `email_utils.py` - Pure Python functions (no Flask dependency)
- `app.py` - Thin Flask wrapper that calls email functions

This follows the "separation of concerns" principle, making the codebase more maintainable.

## Problems Encountered & Solutions

### Problem 1: Date Field Not Accepting Input

**Issue:** When using `send_keys("06/23/2004")` on the date field, only the year (2004) was being filled, showing as `mm/dd/2004` instead of the complete date.

**Root Cause:** HTML `<input type="date">` fields have strict format requirements. While manual typing of `06/23/2004` worked, Selenium's `send_keys()` wasn't properly triggering the field's internal parsing.

**Solution:** Used JavaScript to directly set the date value in ISO format (YYYY-MM-DD):
```python
# Instead of send_keys, use JavaScript
driver.execute_script("arguments[0].value = '2004-06-23';", date_field)

# Trigger validation events
driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", date_field)
driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", date_field)
```

**Why this works:** 
- HTML date inputs internally store dates in ISO format (YYYY-MM-DD)
- JavaScript sets the value directly, bypassing input parsing issues
- Triggering `input` and `change` events ensures Google Forms' validation runs correctly

### Problem 2: Class Name Selector Not Working

**Issue:** Using `By.CLASS_NAME` with `"whsOnd zHQkBf"` (two classes) failed to find elements.

**Root Cause:** Selenium's `CLASS_NAME` selector only accepts a single class name, not multiple classes separated by spaces.

**Attempted Solutions:**
1. ❌ `By.CLASS_NAME, "whsOnd zHQkBf"` - Failed (space means two classes)
2. ✓ `By.CLASS_NAME, "Xb9hP"` - Worked (found container divs)
3. ✓ Alternative: `By.CSS_SELECTOR, ".whsOnd.zHQkBf"` - Would also work (dot notation for multiple classes)

**Final Approach:** Found container divs (`Xb9hP`), then extracted input elements from within them. This proved more reliable than targeting the inputs directly.

### Problem 3: Screenshot Timing Issues

**Issue:** Screenshots were either blank or showing the form page instead of the confirmation page.

**Root Cause:** Taking the screenshot immediately after clicking submit didn't give the confirmation page time to load.

**Solution:** Implemented explicit wait for a confirmation element:
```python
# Wait for confirmation text to appear
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[contains(text(), 'recorded')]")
    )
)

# Additional buffer for rendering
time.sleep(2)

# Now take screenshot
driver.save_screenshot("screenshots/confirmation.png")
```

**Key Learning:** Always wait for specific elements rather than arbitrary time delays. This makes the code more reliable across different network speeds.

### Problem 4: Address Field Different Structure

**Issue:** The address field wasn't being caught by the input field extraction logic.

**Root Cause:** The address field is a `<textarea>` element, not an `<input>` element.

**Solution:** Handled it separately using its unique class:
```python
# Handle textarea separately
address_field = driver.find_element(By.CSS_SELECTOR, "textarea.KHxj8b.tL9Q4c")
address_field.send_keys("123 Main St, City")
```

**Lesson:** Always inspect the actual HTML structure rather than assuming all form fields use the same element type.

## Key Technical Decisions

### 1. Separation of Concerns
Split email logic (`email_utils.py`) from Flask routes (`app.py`) for testability and reusability.

### 2. Explicit Waits Over Implicit Waits
Used `WebDriverWait` with specific conditions rather than blanket `time.sleep()` calls for more reliable automation.

### 3. JavaScript Execution for Edge Cases
When standard Selenium methods failed (date field), fell back to JavaScript execution for direct DOM manipulation.

### 4. Environment Variables for Secrets
Used `.env` file and `python-dotenv` to keep credentials out of source code.

## Testing Recommendations

1. **Test email locally first:** Change recipients to your own email before sending to actual addresses
2. **Verify screenshot:** Check that `screenshots/confirmation.png` shows the confirmation message
3. **Check attachments:** Ensure resume and screenshot are both attached to the email

## Common Issues & Troubleshooting

### "SMTP Authentication Error"
- Verify you're using an App Password, not your regular Gmail password
- Check that 2FA is enabled on your Google account
- Ensure credentials in `.env` are correct

### "Element not found" errors
- Form structure may have changed
- Check class names are still correct
- Increase wait timeouts if network is slow

### Date field shows "Invalid date"
- Verify date format is YYYY-MM-DD in the JavaScript execution
- Check that the date is valid (not Feb 30, etc.)

## License

MIT

## Author

Daniel Popoola

---

**Note:** This project was created as part of a technical assignment to demonstrate web automation and email integration skills.