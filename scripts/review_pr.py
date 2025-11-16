from openai import OpenAI
import os
import requests

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

repo = os.environ.get("GITHUB_REPOSITORY")
pr_number = os.environ.get("GITHUB_REF", "").split("/")[-1]

gh_token = os.environ["GH_TOKEN"]

headers = {
    "Authorization": f"token {gh_token}",
    "Accept": "application/vnd.github.v3+json"
}

# 1. Get PR files
files_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
files = requests.get(files_url, headers=headers).json()

diff_text = ""
for f in files:
    if "patch" in f:
        diff_text += f"File: {f['filename']}\n{f['patch']}\n\n"

# 2. GPT request using new API
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are an AI code reviewer."},
        {"role": "user", "content": f"Review this pull request diff:\n\n{diff_text[:10000]}"}
    ]
)

review_comment = response.choices[0].message.content

# 3. Post review comment to PR
comments_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
requests.post(comments_url, headers=headers, json={"body": review_comment})
