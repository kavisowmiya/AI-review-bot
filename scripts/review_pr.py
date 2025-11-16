import os, requests, openai

repo = os.environ['GITHUB_REPOSITORY']
pr_number = os.environ['GITHUB_REF'].split('/')[-2]  # or pass via env
gh_token = os.environ['GH_TOKEN']

# 1. Get PR files
headers = {'Authorization': f'token {gh_token}'}
pr_files = requests.get(f'https://api.github.com/repos/{repo}/pulls/{pr_number}/files',
                        headers=headers).json()

# 2. Concatenate file diffs
diff_text = "\n".join([f['patch'] for f in pr_files if 'patch' in f])

# 3. Ask GPT for review
openai.api_key = os.environ['OPENAI_API_KEY']
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "system","content":"You are a senior code reviewer."},
              {"role":"user","content": f"Review this code diff:\n{diff_text}"}]
)

review_comment = response['choices'][0]['message']['content']

# 4. Post comment back to PR
requests.post(f'https://api.github.com/repos/{repo}/issues/{pr_number}/comments',
              headers=headers,
              json={'body': review_comment})
