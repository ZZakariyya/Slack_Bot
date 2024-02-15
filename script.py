from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from datetime import datetime, timedelta
import re

most_watched_events = [
    'World Cup of Soccer',
    'Tour de France',
    'Wimbledon',
    'Cricket World Cup',
    "Women's World Cup",
    'Summer Games',
    'Winter Games',
    'UEFA Champions League',
    'Super Bowl',
    'NBA Finals',
    'World Cup of Rugby',
    'Kentucky Derby',
    'The Masters',
    'World Series',
    'NCAA Final Four'
]

chrome_driver_path = ChromeDriverManager().install()
service = Service(executable_path=chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

url = 'https://www.scoreandchange.com/sports_events/'

driver.get(url)

events = []

xpath_pattern = '/html/body/div[5]/div/div/div/div/main/div[2]/article/div/p'
elements = driver.find_elements(By.XPATH, xpath_pattern)

for element in elements:
    events.append(element.text)

today = datetime.now()
start_week = today - timedelta(days=today.weekday())
end_week = start_week + timedelta(days=6)

def parse_dates(event_str):
    dates = re.findall(r'\d{1,2} \w+ \d{4}', event_str)
    parsed_dates = [datetime.strptime(date, '%d %B %Y') for date in dates]
    return parsed_dates

def is_event_this_week(event_dates):
    for date in event_dates:
        if start_week <= date <= end_week:
            return True
    return False

events_this_week = []
for event in events:
    event_dates = parse_dates(event)
    if is_event_this_week(event_dates):
        events_this_week.append(event)

for event in events_this_week:
    print(event)

driver.quit()