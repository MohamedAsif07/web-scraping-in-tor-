Here’s the README file in a polished and professional markdown format:

```markdown
# Onion Site Login and CAPTCHA Solver

Automates logging into Onion sites using Tor, solves CAPTCHA challenges with Tesseract OCR, and scrapes protected content post-login.

---

## **Features**

- 🌐 **Tor Integration**: Ensures anonymity by routing traffic through Tor.
- 🔄 **Selenium WebDriver**: Automates browser interactions to handle logins and forms.
- 🔍 **CAPTCHA Solving**: Uses OpenCV and Tesseract OCR for CAPTCHA text recognition.
- 📦 **Session Management**: Maintains a session for authenticated scraping with cookies.
- ⚙️ **Customizable**: Easily configure settings for Tor, Tesseract, and target Onion sites.

---

## **Prerequisites**

### **Python Dependencies**
Install the required libraries via pip:
```bash
pip install stem selenium pytesseract Pillow opencv-python requests
```

### **External Tools**
1. **Tor**: Install Tor and configure the control port and SOCKS proxy.
   ```bash
   sudo apt install tor
   ```
   Ensure Tor is running with a control password.

2. **Tesseract OCR**: Install Tesseract for CAPTCHA recognition.
   ```bash
   sudo apt install tesseract-ocr
   ```
   Configure the path to the Tesseract executable in the script (`TESSERACT_CMD`).

3. **Geckodriver**: Install Geckodriver for Selenium's Firefox automation.  
   [Download Geckodriver](https://github.com/mozilla/geckodriver/releases) and add it to your system PATH.

---

## **Setup**

1. Clone or download this repository:
   ```bash
   git clone https://github.com/your-repo/onion-login-captcha-solver.git
   cd onion-login-captcha-solver
   ```

2. Edit the configuration variables in the script:
   - **Tor Control Password**: Replace `TOR_CONTROL_PASSWORD` with your Tor control password.
   - **Onion Site Details**: Replace placeholders with the Onion site's URL, username, and password.
   - **Tesseract Path**: Update `TESSERACT_CMD` to the correct path for Tesseract on your system.

---

## **Usage**

1. **Start Tor Service**:
   ```bash
   sudo service tor start
   ```

2. **Run the Script**:
   ```bash
   python3 onion_login.py
   ```

3. **CAPTCHA Handling**:
   - The script will automatically preprocess CAPTCHA images and attempt to solve them using OCR.
   - Ensure the CAPTCHA format is compatible with Tesseract's training data.

4. **Scrape Protected Content**:
   - After a successful login, the script retrieves the target page's content and displays it in the console.

---

## **Code Structure**

- **`renew_tor_ip()`**: Refreshes the Tor IP address by signaling the Tor control port.
- **`start_selenium_with_tor()`**: Configures Selenium to route traffic through Tor.
- **`preprocess_captcha()`**: Enhances CAPTCHA images for better OCR results.
- **`solve_captcha()`**: Uses Tesseract to extract text from CAPTCHA images.
- **`login_onion_site()`**: Automates the login process, including CAPTCHA submission.
- **`scrape_after_login()`**: Scrapes protected content using the authenticated session.

---

## **Troubleshooting**

- **Tor Connection Issues**: Verify Tor is running on `127.0.0.1:9050` (SOCKS proxy) and `127.0.0.1:9051` (control port).
- **CAPTCHA Accuracy**: Improve OCR results by adjusting image preprocessing or training Tesseract on similar CAPTCHA datasets.
- **Selenium Errors**: Ensure Geckodriver and Firefox are installed and up-to-date.

---

## **Security Notes**

- **Ethical Use Only**: Use this script responsibly and only on sites you own or have permission to access.
- **Protect Credentials**: Avoid sharing sensitive information such as passwords or Tor configurations.

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## **Author**

**Darkstrom**  
Developed for automated login and scraping tasks on Onion sites, ensuring privacy and efficiency.

---

## **Demo**

![Loading Animation](loading_animation.gif)  
*Above: Example of the loading animation in action.*
```

This version is structured, easy to read, and formatted to work well in GitHub or other markdown viewers. Let me know if you’d like to refine it further!