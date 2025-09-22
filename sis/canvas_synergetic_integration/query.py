import requests

canvas_domain = "https://trinityunimelb.test.instructure.com/"
course_id = "739"
token = "24575~EWQwkl1AYXnBKGHJR3P62ALxOlz6a75XiVxHwWkao0GFVSzsWiBYiHEwJPl43cnb"

url = f"{canvas_domain}/api/v1/courses/{course_id}/enrollments"
headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(url, headers=headers)
enrollments = response.json()

for e in enrollments:
    print("User:", e.get('user', {}).get('name', 'Unknown'))
    print("Workflow State:", e.get('workflow_state', 'Not available'))
    print("---")