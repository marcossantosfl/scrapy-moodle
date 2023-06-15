import requests
import json
from bs4 import BeautifulSoup
import sys

def clean_html(soup):
    # Remove script and style elements
    for element in soup(['script', 'style']):
        element.decompose()

    return soup.prettify()

def scrape_moodle(username, password):
    login_url = 'https://moodle.cct.ie/login/index.php'

    # Fetch the login page to get the logintoken
    session = requests.Session()
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    logintoken = soup.find('input', {'name': 'logintoken'})['value']

    # Log in with the provided username and password
    form_data = {
        'username': username,
        'password': password,
        'logintoken': logintoken,
    }
    response = session.post(login_url, data=form_data)

    # Check if logged in successfully
    if "Invalid login" in response.text:
        print(json.dumps({"logged": "no"}))
    else:
        # Clean the HTML page after a successful login
        soup = BeautifulSoup(response.text, 'html.parser')
        cleaned_html = clean_html(soup)

        # Name and surname
        name_string = soup.find('div', class_='logininfo').find('a').text.strip()
        name_list = name_string.split()
        first_name = name_list[0]
        last_name = ' '.join(name_list[1:])

        # Extract course links
        course_links = soup.select('.card-text.content.mt-3 .column.c1 a[href^="https://moodle.cct.ie/course/view.php?id="]')

        profile_link = soup.find('a', {'data-title': 'profile,moodle'})
        user_id = profile_link['href'].split('=')[1]

        data = []

        for course_link in course_links:
            course_url = course_link['href']
            course_name = course_link.text.strip()
            course_id = course_url.split("id=")[1]
            grade_report_url = "https://moodle.cct.ie/course/user.php?mode=grade&id=" + str(course_id) + "&user=" + str(user_id)

            response = session.get(grade_report_url)

            soup = BeautifulSoup(response.text, 'html.parser')

            course_data = {"course": course_name, "courseid": course_id, "items": []}

            for row in soup.select('tr'):
                percentage_element = row.find('td', class_='column-percentage')
                feedback_element = row.find('td', class_='column-feedback')

                if percentage_element and feedback_element:
                    percentage = percentage_element.text.strip()
                    feedback = ' '.join(feedback_element.stripped_strings)
                    grade_item = row.find('th', class_='column-itemname').text.strip()

                    # Create a dictionary for this grade item
                    grade_item_data = {
                        "item": grade_item,
                        "percentage": percentage,
                        "feedback": feedback
                    }

                    # Add the grade item to the list for this course
                    course_data["items"].append(grade_item_data)

            # Add the course data to the overall data list
            data.append(course_data)

        # Return the data as a nicely formatted JSON object
        result = {"logged": "yes",  "name" : first_name, "last_name" :  last_name, "data": data}
        # Train and save the feedback in a separate thread
        print(json.dumps(result, indent=2))

if __name__ == '__main__':
    try:
        # Get the username and password from the command-line arguments
        username = sys.argv[1]
        password = sys.argv[2]

        scrape_moodle(username, password)
    except IndexError:
        print("Please provide a valid username and password as command line arguments.")
    except Exception as e:
        print("An error occurred:"+ str(e))