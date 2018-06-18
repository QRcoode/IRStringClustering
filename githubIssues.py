import csv
import requests
import json
import re
import os.path
import sys

'''
This code is for collecting data on the issues located in a specified GitHub repo. As of now, it is only collecting
the body, title and any relevant labels of each issue, but it can be modified appropriately by looking at the JSON files
on the GitHub API.

@param GITHUB_USER = Username of the desired GitHub account.
@param GITHUB_PASSWORD = Password of the desired GitHub account.
@param REPO = Part of the URL that specifies the repo.
@return ISSUE_TEXT_NAME = Filename of the csv file containing all of the issue text.
'''

GITHUB_USER = 'rqin005@aucklanduni.ac.nz' # credentials
GITHUB_PASSWORD = 'qr19890219rain'
REPO = 'k9mail/k-9'  # format is username/repo CHANGE THIS TO SWITCH REPO

#Requires change if not looking for closed issues (for open issues only, the '?state=closed' can be omitted)
ISSUES_FOR_REPO_URL = 'https://api.github.com/repos/%s/issues?state=closed' % REPO
ISSUE_TEXT_NAME = '%s-issues.csv' % (REPO.replace('/', '-')) #decides the name of the file
AUTH = (GITHUB_USER, GITHUB_PASSWORD)

txtout = open('data.json', 'w')

def write_issues(response):
    "output a list of issues to csv"
    if not r.status_code == 200:
        raise Exception(r.status_code) # Usually due to wrong username/password (see variables after imports)

    json.dump(r.json(), txtout, indent=4) #sets up all of the data to extract info from

    for issue in r.json():
        containsLabel = False
        unwantedLabel = False
        labelText = ''

        if len(issue['labels']) > 0: #only get the issues which have labels
            for label in issue['labels']:
                labelName = label['name']

                # checks if the issue has been labelled by one of the following
                # this can be changed depending on what labels are wanted
                if labelName[:3] == "bug" or labelName[:7] == "feature" or labelName == "crash":
                    containsLabel = True
                    labelText += labelName + '+' # Only writes the labels we care about

                if labelName == "wontfix" or labelName == "duplicate" or labelName == "invalid":
                    unwantedLabel = True

            if containsLabel == True and unwantedLabel == False:
                try:
                    if 'pull_request' not in issue: #ignores all pull requests, only gets issues
                        global issues
                        issues += 1 #keeps count of the number of issues gathered
                        #include the title as some issues have some of the issue text within the title
                        bodyText = process_text(issue['body'])
                        issueText = issue['title'] + '. ' + bodyText

                        # To ensure no reports that are suspiciously long make it through. This usually indicates a
                        # crash report log or similar, which we don't need.
                        if len(issueText) < 1000:
                            csvout.writerow([issueText, labelText])

                except (UnicodeEncodeError, AttributeError):
                    pass

# Function to cut off all unnecessary parts of the issue report
def process_text(bodyText):
    # Beware that everything in this function is specific to Brave! This is because Brave GitHub Issues has a template
    # for users to enter their issue details in, which ruins a lot of the text extraction. Other GitHub repos may not
    # need this much processing
    noURLText = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '. ', bodyText) # gets rid of URLs
    processingText = noURLText.replace("\\n", "").replace("\\r", "").replace("\r", "").replace("\n", "") \
        .replace("<!--Have you searched for similar issues? We have received a lot of feedback and bug reports that we "
                 "have closed as duplicates. Before submitting this issue, please visit our community site for common "
                 "ones: . -->", "") \
    .replace("### Description", "") \
    .replace("<!--[Description of the issue]-->", "")\
    .replace("<!--Have you searched for similar issues? We have received a lot of feedback and bug reports that we have "
             "closed as duplicates.Before submitting this issue, please visit our wiki for common ones: . By using "
             "search engines along with GitHub search function, you would be able to find duplicates more efficiently."
             "For more, check out our community site: . -->", "")\
    .replace("<!--Have you searched for similar issues? There is a lot of feedbacks and bug reports we have received "
             "and closed as duplicate.Before submitting this issue, please visit our wiki for common ones: . By using "
             "search engines along with GitHub search function, you would be able to find duplicates more efficiently."
             "For more, check out our community site: . -->", "")
    # All of the above text to replace are parts of issue reports that are commonly found in the beginning of the issue
    # report. To understand what I mean, go to https://github.com/brave/browser-laptop/issues/new to see the default
    # template already placed in the box (make sure you are logged in GitHub).

    hashEnd = processingText.find("# ") # The end of the description is usually defined by the start of a heading '#'
    starEnd = processingText.find("**") # '**' may also be the start of a heading
    similarEnd = processingText.find("- Did you search") # this is also another common passage of text
    descriptionEnd = -1

    # All the code below decides which 'heading' is encountered first
    if (hashEnd != -1 and hashEnd < starEnd) or starEnd == -1:
        if (hashEnd != -1 and hashEnd < similarEnd) or similarEnd == -1:
            descriptionEnd = hashEnd
        else:
            descriptionEnd = similarEnd

    elif starEnd < similarEnd or similarEnd == -1:
        descriptionEnd = starEnd

    if descriptionEnd != -1:
        return processingText[:descriptionEnd] # Returns only the 'description' text
    else:
        return processingText # Returns all text if no ending was found (if all param == -1)

# Ensures that the user has not forgotten to input a username and password
if GITHUB_USER == '' or GITHUB_PASSWORD == '':
    print("Please ensure you have entered your GitHub credentials.")
    sys.exit()

issues = 0
r = requests.get(ISSUES_FOR_REPO_URL, auth=AUTH)

# Ensures that no existing files are overwritten
if os.path.exists(ISSUE_TEXT_NAME):
    print("Please ensure that the file '" + ISSUE_TEXT_NAME + "' does not exist, and try again.")
    sys.exit()

csvfile = open(ISSUE_TEXT_NAME, 'w')
csvout = csv.writer(csvfile)
write_issues(r)

# Code responsible for turning the pages
if 'link' in r.headers:
    pages = dict(
        [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
            [link.split(';') for link in
                r.headers['link'].split(',')]])

    while 'last' in pages and 'next' in pages:
        pages = dict(
            [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
                [link.split(';') for link in
                    r.headers['link'].split(',')]])

        print(pages['next']) #updates the console log to let the user know the progress
        r = requests.get(pages['next'], auth=AUTH)
        write_issues(r)

        if pages['next'] == pages['last']: #when the last page is reached
            break

print('Total number of issues: %s' % issues) # Console output, just telling the user
csvfile.close()
txtout.close()