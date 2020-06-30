from linkedin_scraper import Person, actions
from selenium import webdriver
from time import sleep
import csv
import config

chromedriver_path = '/usr/local/bin/chromedriver' # Change this to your own chromedriver path
driver = webdriver.Chrome(executable_path=chromedriver_path)

# update linkedin credentials in config.py
email = config.EMAIL
password = config.PASSWORD

# read URLs from file
filepath = 'linkedin_urls.csv'
data_file = open(filepath,'r')
urls = csv.reader(data_file, delimiter=',')
urls = [row[0] for row in urls]
print (urls)

#login
actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
sleep(2)

# loop through the URLs
people = []
for url in urls:
    person = Person(url, driver=driver, close_on_complete=False)
    person_details = [url, person.name, person.experiences[0].institution_name.decode('utf8'),
                        person.experiences[0].position_title.decode('utf8')]
    people.append(person_details)
    person.experiences.clear()
    sleep(2)

print (people)

# write URLs to file
outfilepath = 'linkedin_urls_scraped.csv'
with open(outfilepath, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
    for person in people:
        writer.writerow(person)

driver.quit()
