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
print (str(len(urls)), "profiles")

#login
actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
sleep(2)

# loop through the URLs
people = []
failed_urls = []
person = None
for url in urls:
    try:
        person = Person(url, experiences=[], driver=driver, close_on_complete=False)
        name = person.name
        title = person.experiences[0].position_title.decode('utf8') if person.experiences[0].position_title is not None else ''
        company = person.experiences[0].institution_name.decode('utf8') if person.experiences[0].institution_name is not None else ''
        person_details = [url, name, company, title]
        people.append(person_details)
        print ("     [OK]", ", ".join([name, company, title]))
        person.experiences.clear()
    except Exception as e:
        print ("[Skipped]", person.name, "Experience:", person.experiences, e)
        failed_urls.append(url)
    # driver.quit()
    # quit()
    sleep(2)

# write URLs to file
outfilepath = 'linkedin_urls_scraped.csv'
with open(outfilepath, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
    for person in people:
        writer.writerow(person)

print("\nCould not parse", len(failed_urls), "profiles")
for url in failed_urls:
    print (url)

driver.quit()
