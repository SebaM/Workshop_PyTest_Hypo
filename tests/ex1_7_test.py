from selenium import webdriver

#TODO:
#Create fixture
#Add comments into code Given / When / Then

def test_google() -> None:
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.google.com/")
    print(f'Title {driver.title}')

def test_pytest() -> None:
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://docs.pytest.org/en/stable/index.html")
    print(f'Title {driver.title}')