import bs4 as bs
import urllib.request
import sqlite3
import os
import attributes

fileDir = os.path.dirname(os.path.realpath('__file__'))

# For accessing the file in a folder contained in the current folder

# Creates or opens a file called uToronto with a SQLite3 DB
db = sqlite3.connect(os.path.join(fileDir, 'data\\' + attributes.torCourseDB))
counter, total = 0, 0
invalids = []

# Creates table
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses(id INTEGER PRIMARY KEY,
    courseCode TEXT,
    title TEXT,
    hours TEXT,
    summary TEXT ,
    prerequisites TEXT,
    exclusions TEXT,
    recommend TEXT,
    distribution TEXT,
    breadth TEXT,
    program TEXT)
''')
db.commit()

# First page
f = open(os.path.join(fileDir, 'data\\' + attributes.torCourseList), "r")
current = f.readline().strip()
print(current)


def insertDB(soup, course):
    global counter, total
    counter += 1
    total += 1

    ################
    titleFind = soup.find('h1', class_='title')
    titleText = titleFind.text.strip()
    parsedTitle = titleText[titleText.find(' ') + 1:]
    hours = soup.find(
        'div', class_='field field-name-field-hours field-type-text field-label-inline clearfix')

    if (hours):
        hours = hours.text[hours.text.find(":") + 2:]
    summary = soup.find(
        'div', class_='field field-name-body field-type-text-with-summary field-label-hidden')
    if summary:
        summary = summary.text.strip()
    prerequisites = soup.find(
        'div', class_='field field-name-field-prerequisite1 field-type-text-with-summary field-label-inline clearfix')
    if (prerequisites):
        prerequisites = prerequisites.text.strip(
        )[prerequisites.text.strip().find(":") + 2:].strip()
    exclusions = soup.find(
        'div', class_='field field-name-field-exclusion1 field-type-text-with-summary field-label-inline clearfix')
    if (exclusions):
        exclusions = exclusions.text.strip(
        )[exclusions.text.strip().find(":") + 2:].strip()
    recommend = soup.find(
        'div', class_='field field-name-field-recommended1 field-type-text-with-summary field-label-inline clearfix')
    if (recommend):
        recommend = recommend.text.strip(
        )[recommend.text.strip().find(":") + 2:].strip()
    distribution = soup.find(
        'div', class_='field field-name-field-distribution-req field-type-list-text field-label-inline clearfix')
    if (distribution):
        distribution = distribution.text[distribution.text.find(":") + 2:]
    breadth = soup.find(
        'div', class_='field field-name-field-breadth-req field-type-list-text field-label-inline clearfix')
    if (breadth):
        breadth = breadth.text[breadth.text.find(":") + 2:]
    program = soup.find(
        'div', class_='field field-name-field-section-link field-type-text-with-summary field-label-inline clearfix')
    if (program):
        program = program.text.strip()[program.text.strip().find(":") + 2:]
    ######

    cursor = db.cursor()
    cursor.execute('''INSERT INTO courses(courseCode, title, hours, summary, prerequisites, exclusions, recommend, distribution, breadth, program)
                  VALUES(?,?,?,?,?,?,?,?,?,?)''', (course,
                                                   parsedTitle if titleFind else "NULL",
                                                   hours if hours else "NULL",
                                                   summary if summary else "NULL",
                                                   prerequisites if prerequisites else "NULL",
                                                   exclusions if exclusions else "NULL",
                                                   recommend if recommend else "NULL",
                                                   distribution if distribution else "NULL",
                                                   breadth if breadth else "NULL",
                                                   program if program else "NULL"))

    db.commit()
    print("{0} inserted".format(course.split()))


if __name__ == "__main__":

    while current:
        source = urllib.request.urlopen(
            'https://fas.calendar.utoronto.ca/course/' + current).read()
        soup = bs.BeautifulSoup(source, 'lxml')

        if soup.title.text[0:5] == "Sorry":  # Error checking
            print("Course Code invalid: {0}\n".format(current))
            invalids.append(current)
            current = f.readline()
            total += 1
        else:
            insertDB(soup, current)
            current = f.readline().strip()
            print(current)

    print("{0} out of {1} successful insert".format(counter, total))
    db.close()
    f.close()
    print("==============DONE==============")
