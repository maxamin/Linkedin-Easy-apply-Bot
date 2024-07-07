import yaml, pdb
import os
import platform
import requests
import zipfile
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from linkedineasyapply import LinkedinEasyApply
from validate_email import validate_email

def init_browser():
    browser_options = Options()
    options = ['--disable-blink-features', '--no-sandbox', '--start-maximized', '--disable-extensions',
               '--ignore-certificate-errors', '--disable-blink-features=AutomationControlled']

    for option in options:
        browser_options.add_argument(option)

    driver = webdriver.Chrome(chrome_options=browser_options)

    driver.set_window_position(0, 0)
    driver.maximize_window()

    return driver


def validate_yaml():
    with open("config.yaml", 'r') as stream:
        try:
            parameters = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise exc

    mandatory_params = ['email', 'password', 'disableAntiLock', 'remote', 'experienceLevel', 'jobTypes', 'date',
                        'positions', 'locations', 'distance', 'outputFileDirectory', 'checkboxes', 'universityGpa',
                        'languages', 'industry', 'technology', 'personalInfo', 'eeo', 'uploads']

    for mandatory_param in mandatory_params:
        if mandatory_param not in parameters:
            raise Exception(mandatory_param + ' is not inside the yml file!')

    assert validate_email(parameters['email'])
    assert len(str(parameters['password'])) > 0

    assert isinstance(parameters['disableAntiLock'], bool)

    assert isinstance(parameters['remote'], bool)

    assert len(parameters['experienceLevel']) > 0
    experience_level = parameters.get('experienceLevel', [])
    at_least_one_experience = False
    for key in experience_level.keys():
        if experience_level[key]:
            at_least_one_experience = True
    assert at_least_one_experience

    assert len(parameters['jobTypes']) > 0
    job_types = parameters.get('jobTypes', [])
    at_least_one_job_type = False
    for key in job_types.keys():
        if job_types[key]:
            at_least_one_job_type = True
    assert at_least_one_job_type

    assert len(parameters['date']) > 0
    date = parameters.get('date', [])
    at_least_one_date = False
    for key in date.keys():
        if date[key]:
            at_least_one_date = True
    assert at_least_one_date

    approved_distances = {0, 5, 10, 25, 50, 100,1000}
    assert parameters['distance'] in approved_distances

    assert len(parameters['positions']) > 0
    assert len(parameters['locations']) > 0

    assert len(parameters['uploads']) >= 1 and 'resume' in parameters['uploads']

    assert len(parameters['checkboxes']) > 0

    checkboxes = parameters.get('checkboxes', [])
    assert isinstance(checkboxes['driversLicence'], bool)
    assert isinstance(checkboxes['requireVisa'], bool)
    assert isinstance(checkboxes['legallyAuthorized'], bool)
    assert isinstance(checkboxes['urgentFill'], bool)
    assert isinstance(checkboxes['commute'], bool)
    assert isinstance(checkboxes['backgroundCheck'], bool)
    assert 'degreeCompleted' in checkboxes

    assert isinstance(parameters['universityGpa'], (int, float))

    languages = parameters.get('languages', [])
    language_types = {'none', 'conversational', 'professional', 'native or bilingual'}
    for language in languages:
        assert languages[language].lower() in language_types

    industry = parameters.get('industry', [])

    for skill in industry:
        assert isinstance(industry[skill], int)
    assert 'default' in industry

    technology = parameters.get('technology', [])

    for tech in technology:
        assert isinstance(technology[tech], int)
    assert 'default' in technology

    assert len(parameters['personalInfo'])
    personal_info = parameters.get('personalInfo', [])
    for info in personal_info:
        assert personal_info[info] != ''

    assert len(parameters['eeo'])
    eeo = parameters.get('eeo', [])
    for survey_question in eeo:
        assert eeo[survey_question] != ''

    return parameters

def get_latest_chromedriver_version():
    """Fetches the latest version of ChromeDriver."""
    url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    response = requests.get(url)
    response.raise_for_status()
    return response.text.strip()

def get_system_info():
    """Detects the system OS and architecture."""
    system = platform.system()
    arch = platform.machine()
    
    if system == "Linux":
        system = "linux"
        if arch in ["x86_64", "AMD64"]:
            arch = "64"
        elif arch in ["i386", "i686", "x86"]:
            arch = "32"
    elif system == "Darwin":
        system = "mac"
        arch = "64"
    elif system == "Windows":
        system = "win"
        if arch in ["AMD64", "x86_64"]:
            arch = "32" # ChromeDriver for Windows is 32-bit
    else:
        raise Exception(f"Unsupported OS: {system}")

    return system, arch

def download_chromedriver(version, system, arch):
    """Downloads and extracts ChromeDriver."""
    base_url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_{system}{arch}.zip"
    response = requests.get(base_url)
    response.raise_for_status()
    
    with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
        zip_ref.extractall()

def check_chromedriver_present():
    """Checks if ChromeDriver is already present and returns its version if found."""
    try:
        result = subprocess.run(["chromedriver", "--version"], capture_output=True, text=True, check=True)
        version = result.stdout.split()[1]
        return version
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
def start():
    parameters = validate_yaml()
    browser = init_browser()
    bot = LinkedinEasyApply(parameters, browser)
    bot.login()
    bot.security_check()
    bot.start_applying()
if __name__ == '__main__':
    try:
        current_version = check_chromedriver_present()
        if current_version:
            print(f"ChromeDriver is already present with version {current_version}.")
            start()
        else:
            version = get_latest_chromedriver_version()
            system, arch = get_system_info()
            download_chromedriver(version, system, arch)
            print(f"ChromeDriver {version} downloaded and extracted successfully.")
            start()
    except Exception as e:
        print(f"An error occurred: {e}")





