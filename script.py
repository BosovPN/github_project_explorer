import requests
import json
import os

def get_headers(token):
    """Helper function to add optional authorization header."""
    if token:
        return {'Authorization': f'token {token}'}
    return {}


def get_contents(url, token):
    """Fetch repository contents from the provided URL."""
    try:
        response = requests.get(url, headers=get_headers(token))
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        raise


def fetch_repo_content(url, token, indent=''):
    """Recursively fetch the repo structure and file contents."""
    structure = ''
    file_contents = ''

    contents = get_contents(url, token)

    for item in contents:
        if item['type'] == 'dir' and not item['name'].startswith('.git'):
            structure += f"{indent}├── {item['name']}/\n"
            nested = fetch_repo_content(item['url'], token, indent + '│   ')
            structure += nested['structure']
            file_contents += nested['file_contents']
        elif item['type'] == 'file' and not item['name'].startswith('.git'):
            structure += f"{indent}├── {item['name']}\n"

            file_response = requests.get(item['download_url'], headers=get_headers(token))
            file_content = file_response.text

            if item['name'].endswith('.json'):
                try:
                    parsed_json = json.dumps(json.loads(file_content), indent=2)
                    file_contents += f"{item['path']}\n{parsed_json}\n\n"
                except json.JSONDecodeError:
                    print(f"Error parsing JSON in file {item['path']}")
                    file_contents += f"{item['path']}\n{file_content}\n\n"
            else:
                file_contents += f"{item['path']}\n{file_content}\n\n"

    return {'structure': structure, 'file_contents': file_contents}


def main():
    owner = input("Enter your GitHub username: ")
    repo = input("Enter your repository name: ")
    token = input("Enter your GitHub token (optional): ")

    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"

    print('Fetching repository contents...')
    result = fetch_repo_content(api_url, token)

    choice = input('Do you want to save the output to a file or display in console? (file/console): ')

    if choice.lower() == 'file':
        folder_path = input('Enter the folder path to save the file (or press enter for current directory): ')
        folder_path = folder_path if folder_path else '.'
        file_name = f"{repo.replace(' ', '_')}_details.txt"  # Use repo name as part of the file name
        path = os.path.join(folder_path, file_name)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f"Repository Structure:\n{result['structure']}\nFile Contents:\n{result['file_contents']}")
        print(f"Output saved to {path}")
    else:
        print(f"Repository Structure:\n{result['structure']}\nFile Contents:\n{result['file_contents']}")


if __name__ == '__main__':
    main()