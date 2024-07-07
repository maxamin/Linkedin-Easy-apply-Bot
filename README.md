
## README.md for `LinkedinEasyApply.py`
# Disclaimer

The LinkedIn Easy Apply Bot is For educationaly Reasons only ! . However, please read and understand the following important points before using this tool:

1. **Compliance with LinkedIn Terms of Service**: 
   - Use of this bot must comply with LinkedIn's terms of service and usage policies. Unauthorized automation or scraping can lead to account suspension or termination. Users are responsible for ensuring their actions are in accordance with LinkedIn’s policies.

2. **Accuracy and Effectiveness**: 
   - While this bot aims to streamline the job application process, there is no guarantee of accuracy, completeness, or effectiveness of applications submitted through it. Users should verify all information and ensure it is correct.

3. **Data Privacy**: 
   - The bot may require access to personal information and LinkedIn account details. Users should be aware of the risks involved in sharing such information and ensure they are using the bot in a secure environment.

4. **Liability**: 
   - The developers of this bot are not responsible for any consequences resulting from its use, including but not limited to account suspension, data breaches, or unsuccessful job applications. Users assume all risks associated with using this tool.

5. **Usage at Own Risk**: 
   - By using this bot, you acknowledge that you understand and accept these risks and disclaimers. Use this tool at your own risk.


### Overview

`LinkedinEasyApply.py` is a Python script that automates the process of applying for jobs on LinkedIn. It uses Selenium WebDriver to interact with the LinkedIn website and perform job searches, fill out application forms, and submit applications. The script is designed to handle various edge cases, such as security checks and blacklisted companies or job titles.

### Features

- **Automated Login**: Logs into LinkedIn using provided credentials.
- **Job Search**: Searches for jobs based on specified positions and locations.
- **Application Process**: Applies to jobs, fills out necessary forms, uploads resumes, and submits applications.
- **Blacklist Management**: Skips jobs or companies that match blacklisted titles or names.
- **Error Handling**: Handles common errors and retries failed applications.
- **Customization**: Allows configuration of job search parameters, resume and cover letter uploads, and more.

### Requirements

- Python 3.x
- Selenium
- ChromeDriver (or another WebDriver compatible with Selenium)
- Other required Python packages (specified in `requirements.txt`)

### Installation

1. Clone the repository or download the script.
2. Install the required Python packages using pip:
   ```sh
   pip install -r requirements.txt
   ```

3. Download the appropriate WebDriver (e.g., ChromeDriver) and ensure it's in your PATH.

### Configuration

Create a configuration file (e.g., `config.json`) with the following structure:

```json
{
  "email": "your_email@example.com",
  "password": "your_password",
  "disableAntiLock": false,
  "companyBlacklist": ["Company1", "Company2"],
  "titleBlacklist": ["Intern", "Junior"],
  "outputFileDirectory": "path/to/output",
  "uploads": {
    "resume": "path/to/resume.pdf",
    "coverLetter": "path/to/cover_letter.pdf"
  },
  "universityGpa": 3.5,
  "languages": ["English", "Spanish"],
  "industry": {
    "default": "3-5 years",
    "specific_industry": "2-3 years"
  },
  "technology": {
    "default": "2-3 years",
    "specific_technology": "3-5 years"
  },
  "personalInfo": {
    "Street address": "123 Main St",
    "City": "Anytown",
    "Zip": "12345",
    "State": "CA"
  },
  "eeo": ["Yes", "No"],
  "checkboxes": {
    "driversLicence": true,
    "requireVisa": false,
    "legallyAuthorized": true,
    "urgentFill": false,
    "commute": true,
    "backgroundCheck": true,
    "degreeCompleted": ["Bachelor's", "Master's"]
  }
}
```

### Usage

Run the script with the following command:

```sh
python linkedineasyapply.py --config path/to/config.json
```

### Notes

- Ensure that your WebDriver version matches your browser version.
- This script is intended for educational purposes. Use responsibly and comply with LinkedIn's terms of service.
