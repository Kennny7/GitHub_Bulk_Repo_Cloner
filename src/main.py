import os
import requests
import subprocess
import sys
import logging
from pathlib import Path
from typing import List, Dict, Optional

# Configure the logger
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more detailed logging
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),  # Output to stdout
        logging.FileHandler('app.log')  # Log to file
    ]
)

# Fetch repositories for a given GitHub username
def get_repositories(user: str) -> List[Dict]:
    url = f"https://api.github.com/users/{user}/repos?per_page=100"
    response = requests.get(url)
    
    if response.status_code != 200:
        logging.error(f"[!] Unable to fetch data for user {user}. HTTP Status Code: {response.status_code}")
        sys.exit(1)
    
    logging.info(f"[!] Successfully fetched repositories for user {user}.")
    return response.json()

# Clone repositories from GitHub
def clone_repositories(
    repos: List[Dict], 
    output_folder: Path, 
    clone_all: bool = False, 
    repo_choice: Optional[int] = None
) -> None:
    if clone_all:
        logging.info(f"Cloning all repositories to {output_folder}...")
        for repo in repos:
            repo_url = repo['clone_url']
            repo_name = repo['name']
            repo_path = os.path.join(output_folder, repo_name)
            try:
                subprocess.run(['git', 'clone', repo_url, repo_path], check=True)
                logging.info(f"Cloned {repo_name}")
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to clone {repo_name}. Error: {e}")
    elif repo_choice is not None:
        repo_url = repos[repo_choice]['clone_url']
        repo_name = repos[repo_choice]['name']
        repo_path = os.path.join(output_folder, repo_name)
        try:
            subprocess.run(['git', 'clone', repo_url, repo_path], check=True)
            logging.info(f"Cloned {repo_name}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to clone {repo_name}. Error: {e}")

# Main function to handle user interaction and cloning logic
def main() -> None:
    user_input = input("[+] Enter GitHub username or repository URL: ").strip()
    
    if "github.com" in user_input:
        user = user_input.split('/')[-1]
    else:
        user = user_input

    repos = get_repositories(user)

    if not repos:
        logging.error(f"No repositories found for user {user}.")
        sys.exit(1)

    logging.info(f"\nTop 3 repositories for {user}:")
    for idx, repo in enumerate(repos[:3]):
        logging.info(f"{idx + 1}. {repo['name']} - {repo['html_url']}")

    proceed = input(f"\nDo you want to see all repositories for {user}? (y/n): ").strip().lower()
    if proceed != 'y':
        logging.info("[!] Exiting program.")
        sys.exit(0)

    logging.info(f"\nAll repositories for {user}:")
    for idx, repo in enumerate(repos):
        logging.info(f"{idx + 1}. {repo['name']} - {repo['html_url']}")

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
            logging.error("[!] Invalid repository choice.")
            sys.exit(1)
    else:
        logging.error("[!] Invalid option.")
        sys.exit(1)

    logging.info(f"\nRepositories have been cloned to {output_folder}")

if __name__ == "__main__":
    main()
