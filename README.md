# Moodle Scraper

This script is a Moodle Scraper designed to log into a Moodle instance and extract course and grade data. The data is then formatted into a JSON object for easier viewing or processing.

## How it works

The script performs the following tasks:

1. Accesses the Moodle login page and extracts the login token.
2. Uses the provided username and password to log into Moodle.
3. Checks for successful login. If the login is unsuccessful, it outputs an error message and terminates the script.
4. On successful login, it cleans up the HTML page and extracts the user's first and last names.
5. Extracts all the course links available to the user.
6. For each course, it goes to the grade report page and extracts all grade items along with the associated percentage and feedback.
7. Collects all the extracted data into a JSON object, which includes the user's name, course details, and grade items for each course.

## How to use

To run the script, you need to provide your Moodle username and password as command-line arguments. Here is an example:

```sh
python moodle_scraper.py your_username your_password
