from linkedin_scraper import Person, actions
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
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

# write URLs to file
def writeScraped(person):
    outfilepath = 'linkedin_urls_scraped.csv'
    with open(outfilepath, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(person)

def writeFailed(person):
    outfilepath = 'linkedin_urls_failed.csv'
    with open(outfilepath, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow([person])

# write URLs to file
def writeInvalid(person):
    outfilepath = 'linkedin_urls_invalid.csv'
    with open(outfilepath, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow([person])

# loop through the URLs
people = []
failed_urls = []
invalid_urls = []
person = None
for url in urls:
    try:
        person = Person(url, experiences=[], driver=driver, close_on_complete=False)
        name = person.name
        title = person.experiences[0].position_title.decode('utf8') if person.experiences[0].position_title is not None else ''
        company = person.experiences[0].institution_name.decode('utf8') if person.experiences[0].institution_name is not None else ''
        person_details = [url, name, company, title]
        writeScraped(person_details)
        people.append(person_details)
        print ("     [OK]", ", ".join([name, company, title]))
        person.experiences.clear()

    except NoSuchElementException as e:
        print ("[Invalid]", url, e)
        writeInvalid(url)

    except Exception as e:
        print ("[Skipped]", person.name, "Experience:", person.experiences, e)
        failed_urls.append(url)
        writeFailed(url)

    # driver.quit()
    # quit()
    sleep(2)

print("\nCould not parse", len(failed_urls), "profiles")
for url in failed_urls:
    print (url)

driver.quit()
