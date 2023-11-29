#!/usr/bin/env python3

import os
import requests
import json
import base64

def get_user_input(prompt, default=None):
    user_input = input(prompt)
    return user_input if user_input.strip() != "" else default

def create_jira_issue(api_key, base_url, project, issue_type, summary, description, assignee_email):
    url = f"{base_url}/rest/api/3/issue"
    token = base64.b64encode(api_key.encode()).decode()
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Basic {token}"
    }
    payload = json.dumps({
        "fields": {
            "project": {
                "key": project
            },
            "issuetype": {
                "name": issue_type
            },
            "summary": summary,
            "description": description,
            "assignee": {
                "emailAddress": assignee_email
            }
        }
    })
    try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code != 201:
            print(f"Error creating issue: {response.status_code} - {response.text}")
            return None
        return response.json()
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

# Load environment variables
api_key = os.getenv('JIRA_API_KEY')
base_url = os.getenv('ERGEON_JIRA_URL')
email = os.getenv('WORK_EMAIL')

# Get user input
project = get_user_input("Jira project: ")
issue_type = get_user_input("Jira Issue Type (e.g., 'Bug', 'Story'): ")
summary = get_user_input("Summary: ")
description = get_user_input("Description: ")
assignee_email = get_user_input("Assignee (email): ", default=email)

# Create Jira issue
issue = create_jira_issue(api_key, base_url, project, issue_type, summary, description, assignee_email)
if issue:
    print(f"Ok thank you, your Jira issue code is {issue['key']} and you can visit it at this link: {base_url}/browse/{issue['key']}")
else:
    print("Error: Issue not created.")
