import requests

def get_repo_structure(user, repo, path=""):
    url = f"https://api.github.com/repos/{user}/{repo}/contents/{path}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.json().get('message', 'Unknown error')}")
        return []
    return response.json()

def generate_html_sitemap(contents, prefix="", base_url="https://github.com/", output=[]):
    for i, item in enumerate(contents):
        char = "└── " if i == len(contents) - 1 else "├── "
        link = f"{base_url}{user}/{repo}/tree/main/{item['path']}" if item['type'] == 'dir' else f"{base_url}{user}/{repo}/blob/main/{item['path']}"
        html_link = f'<a href="{link}" class="{"file" if item["type"] == "file" else "dir"}">{item["name"]}</a>'
        output.append(f"{prefix}{char}{html_link}")
        if item['type'] == 'dir':
            new_prefix = prefix + ("    " if i == len(contents) - 1 else "│   ")
            sub_contents = get_repo_structure(user, repo, item['path'])
            generate_html_sitemap(sub_contents, new_prefix, base_url, output)
    return output

# Replace 'user' and 'repo' with your GitHub username and repository name
user = "ecrawford4"
repo = "ecrawford4.github.io"

# Fetch the repository structure
contents = get_repo_structure(user, repo)

# Generate the HTML content
html_output = generate_html_sitemap(contents)
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sitemap</title>
    <link rel="stylesheet" href="sitemap.css">
</head>
<body>
    <pre>
    <a href="https://github.com/{user}/{repo}">https://github.com/{user}/{repo}</a>
    {"\n".join(html_output)}
    </pre>
</body>
</html>
"""

# Save the HTML content to a file
with open("sitemap.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("Sitemap generated: sitemap.html")
