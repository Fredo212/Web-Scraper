# URL to test: https://academiccatalog.umd.edu/undergraduate/approved-courses/inst/

# takes URL,
# returns the list of the rows of the course block
def getHTML(url):
    # search for link values within URL input
    import urllib.request, urllib.parse, urllib.error
    import re
    import ssl
    # ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    # assign page content to container (html)
    html = urllib.request.urlopen(url, context=ctx).read()
    # split the lines of page code into a list
    fullPage = str(html).split('<div class="courseblock">')
    courseBlock = []
    # traverse the lines in the list created on the last line above
    for line in fullPage:
        if '<p class="courseblocktitle noindent">' in line:
            begin = line.find(">INST") + 1
            end = line.find("</strong><", begin)
            # split the lines of the new variable code into a list
            courseBlock.append(line[begin:end])
    return courseBlock


# takes list of rows of the rows of the course block,
# returns dict of course codes, titles and credits
def makeCourseDict(title):
    # create empty course dictionary to hold all INST courses
    courseDict = {}
    # traverse the elements in the dictionary passed to this function
    for i in title:
        courseList = []
        if "INST" in i:
            # Capture course code
            begin1 = i.find("INST")
            end1 = i.find(" ", begin1)
            courseCode = i[begin1:end1]

            # Capture course title
            begin2 = i.find(" ")
            end2 = i.find("(", begin2)
            courseTitle = i[begin2:end2]

            # Capture course credits
            begin3 = i.find("(")
            end3 = i.find("<", begin3)
            courseCredits = i[begin3:end3]

            # Use course code as dictionary key and combine course title and course credits variables for the dictionary value
            courseList.append(courseTitle + courseCredits)
            courseDict[courseCode] = courseList
    return courseDict


# takes dictionary of courses,
# returns list of courses at given level
def atLevel(courseLevel, courseDict):
    # empty course dictionary to hold course at given level
    courseLevelDict = {}
    captureCourseLevel = int(courseLevel)
    # calculate the highest possible number at given level
    highestNum = int(captureCourseLevel) + 99
    # traverse the course dictionary passed to this function
    for key in courseDict:
        courseTitle = key
        # slice course number portion of the course code
        onlyCode = key[4:8]
        # check if the course number is between the start and end numbers at the given level
        if int(onlyCode) in range(int(courseLevel), highestNum):
            # if above condition holds, append entry to the new dictionary
            courseLevelDict[courseTitle] = courseDict[key]
    return courseLevelDict

def main():
    # URL that we are scraping
    captureUrl = "https://academiccatalog.umd.edu/undergraduate/approved-courses/inst/"
    # capture course level (100, 200, 300, 0r 400) from user input
    courseLevel = input('Enter level (100, 200, 300, or 400) - ')
    capUrl = getHTML(captureUrl)
    codeDict = makeCourseDict(capUrl)
    levelDict = atLevel(courseLevel, codeDict)
    # print dictionary of courses at chosen level
    print(levelDict)

main()
