# URL to test: https://academiccatalog.umd.edu/undergraduate/approved-courses/inst/


inst_dict = {"INST201": "https://planetterp.com/course/INST201"}


# takes URL,
# returns the list of the rows of the course block
def get_html(url):
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
    inspect_code = str(html).split('<div class="courseblock">')
    course_block = []
    # traverse the lines in the list created on the last line above
    for line in inspect_code:
        if '<p class="courseblocktitle noindent">' in line:
            begin = line.find(">INST") + 1
            end = line.find("</strong><", begin)
            # split the lines of the new variable code into a list
            course_block.append(line[begin:end])
    return course_block


# takes list of rows of the rows of the course block,
# returns dict of course codes, titles and credits
def make_course_dict(title):
    # create empty course dictionary to hold all INST courses
    course_dict = {}
    # traverse the elements in the dictionary passed to this function
    for i in title:
        course_list = []
        if "INST" in i:
            # Capture course code
            begin1 = i.find("INST")
            end1 = i.find(" ", begin1)
            course_code = i[begin1:end1]

            # Capture course title
            begin2 = i.find(" ")
            end2 = i.find("(", begin2)
            course_title = i[begin2:end2]

            # Capture course credits
            begin3 = i.find("(")
            end3 = i.find("<", begin3)
            course_credits = i[begin3:end3]

            # Use course code as dictionary key and combine course title and course credits variables for the dictionary value
            course_list.append(course_title + course_credits)
            course_dict[course_code] = course_list
    return course_dict


# takes dictionary of courses,
# returns list of courses at given level
def at_level(course_level, course_dict):
    # empty course dictionary to hold course at given level
    course_level_dict = {}
    capture_course_level = int(course_level)
    # calculate the highest possible number at given level
    highest_num = int(capture_course_level) + 99
    # traverse the course dictionary passed to this function
    for key in course_dict:
        course_title = key
        # slice course number portion of the course code
        only_code = key[4:8]
        # check if the course number is between the start and end numbers at the given level
        if int(only_code) in range(int(course_level), highest_num):
            # if above condition holds, append entry to the new dictionary
            course_level_dict[course_title] = course_dict[key]
    return course_level_dict


# Takes a string
# matches the input with dictionary key and returns url for selected course
def course_match(url2):
    for url2 in inst_dict:
        analysis_site = inst_dict[url2]
    return analysis_site


def main():
    # URL that we are scraping
    capture_url = "https://academiccatalog.umd.edu/undergraduate/approved-courses/inst/"
    # capture course level (100, 200, 300, or 400) from user input
    course_level = input('Enter level (100, 200, 300, or 400) - ')
    cap_url = get_html(capture_url)
    code_dict = make_course_dict(cap_url)
    level_dict = at_level(course_level, code_dict)
    # print dictionary of courses at chosen level
    print(level_dict)

    flag = True
    while flag is True:

        continue_scraping = input('Do you want an analysis on a specific course? ')

        if continue_scraping.lower() == "yes":
            course_analysis = input("Type which course you want an analysis on - ").lower()

            y = course_match(course_analysis)
            print(y)

        else:
            print("Analysis complete!")
            break


main()
