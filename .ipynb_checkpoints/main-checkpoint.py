import os
import requests
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Optional

# Fetch repositories for a given GitHub username
def get_repositories(user: str) -> List[Dict]:
    url = f"https://api.github.com/users/{user}/repos?per_page=100"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"[!] Error: Unable to fetch data for user {user}.")
        sys.exit(1)
    
    return response.json()

# Clone repositories from GitHub
def clone_repositories(
    repos: List[Dict], 
    output_folder: Path, 
    clone_all: bool = False, 
    repo_choice: Optional[int] = None
) -> None:
    if clone_all:
        print(f"Cloning all repositories to {output_folder}...")
        for repo in repos:
            repo_url = repo['clone_url']
            repo_name = repo['name']
            repo_path = os.path.join(output_folder, repo_name)
            subprocess.run(['git', 'clone', repo_url, repo_path], check=True)
            print(f"Cloned {repo_name}")
    elif repo_choice is not None:
        repo_url = repos[repo_choice]['clone_url']
        repo_name = repos[repo_choice]['name']
        repo_path = os.path.join(output_folder, repo_name)
        subprocess.run(['git', 'clone', repo_url, repo_path], check=True)
        print(f"Cloned {repo_name}")

# Main function to handle user interaction and cloning logic
def main() -> None:
    user_input = input("[+] Enter GitHub username or repository URL: ").strip()
    
    if "github.com" in user_input:
        user = user_input.split('/')[-1]
    else:
        user = user_input

    repos = get_repositories(user)

    if not repos:
        print(f"No repositories found for user {user}.")
        sys.exit(1)

    print(f"\nTop 3 repositories for {user}:")
    for idx, repo in enumerate(repos[:3]):
        print(f"{idx + 1}. {repo['name']} - {repo['html_url']}")

    proceed = input(f"\nDo you want to see all repositories for {user}? (y/n): ").strip().lower()
    if proceed != 'y':
        print("[!] Exiting program.")
        sys.exit(0)

    print(f"\nAll repositories for {user}:")
    for idx, repo in enumerate(repos):
        print(f"{idx + 1}. {repo['name']} - {repo['html_url']}")

    clone_option = input("\n[?] Would you like to (1) clone all repositories or (2) select a specific one? (1/2): ").strip()

    output_dir = input("\n[+] Enter the path to save the repositories (e.g., C:/Users/YourName/Documents): ").strip()
    output_folder = Path(output_dir) / f"{user}_repos"
    output_folder.mkdir(parents=True, exist_ok=True)

    if clone_option == '1':
        clone_repositories(repos, output_folder, clone_all=True)
    elif clone_option == '2':
        repo_choice = int(input(f"\nEnter the number of the repository to clone (1-{len(repos)}): ").strip()) - 1
        if 0 <= repo_choice < len(repos):
            clone_repositories(repos, output_folder, repo_choice=repo_choice)
        else:
            print("[!] Invalid repository choice.")
            sys.exit(1)
    else:
        print("[!] Invalid option.")
        sys.exit(1)

    print(f"\nRepositories have been cloned to {output_folder}")

if __name__ == "__main__":
    main()
