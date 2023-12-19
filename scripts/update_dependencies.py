import json
import re
import subprocess
import sys
from datetime import datetime

from git import Repo
from github import Github


# main method (toplevel call)
def update_and_create_pr(gh_user, gh_repo_name, gh_token, conan_remote, conanfile='./conanfile.py'):
    # parse & fetch dependency info -> update conanfile
    changes = update_dependencies(conan_remote, conanfile)

    # push changes to branch and create PR
    push_to_branch_and_create_pr(gh_user, gh_repo_name, gh_token, changes)


# secondary function A
def update_dependencies(conan_remote, conanfile='./conanfile.py'):
    # Get the list of dependencies from the conanfile.py using 'conan inspect'
    deps = subprocess.check_output(['conan', 'inspect', '.', '-f', 'json']).decode('utf-8')
    deps = json.loads(deps)['requires']
    # Loop over each dependency
    changes = ""
    for dep in deps:
        try:
            name, version = dep['ref'].split('/')
            # Get the latest version from Conan
            output = subprocess.check_output(['conan', 'search', f'{name}', '-r', conan_remote, '-f', 'json']).decode('utf-8')
            out_obj = json.loads(output)
            versions = list(out_obj[conan_remote].keys())
            _, latest_version = versions[-1].split('/')
            # Check if the latest version is greater than the current version
            if latest_version > version:
                # Replace the version in the conanfile.py
                update_conanfile(conanfile, name, latest_version)
                changes += f"{name}: {version} -> {latest_version}\n"
        except:
            continue
    return changes


# secondary function B
def push_to_branch_and_create_pr(gh_user, gh_repo_name, gh_token, changes=None):
    # Initialize a Git repo
    repo = Repo('.')

    # Create a new branch
    branch_name = 'version-change-' + datetime.now().strftime('%Y-%m-%d_%H%M%S')
    new_branch = repo.create_head(branch_name)
    new_branch.checkout()
        
    # Check if there are changes
    if repo.is_dirty() and changes:
        # Commit the changes
        repo.git.commit('-am', f'Update dependencies to latest versions')

        # Push the branch
        repo.git.push('--set-upstream', 'origin', branch_name)

        # Create a pull request (this requires a GitHub access token)
        g = Github(gh_token)
        repo = g.get_user(gh_user).get_repo(gh_repo_name)
        repo.create_pull(title=f'Update dependencies to latest versions', body='', head=branch_name, base='main')


# helper function
def update_conanfile(conanfile_path, package_name, new_version):
    with open(conanfile_path, 'r') as file:
        content = file.read()
    updated_content = re.sub(f'{package_name}/[^"]*"', f'{package_name}/{new_version}"', content)
    with open(conanfile_path, 'w') as file:
        file.write(updated_content)

# script entry point
if __name__ == '__main__':
    # gh_user, gh_repo_name, gh_token, conan_remote, conanfile
    update_and_create_pr("", "", "", "artifactory")
    # if len(sys.argv) == 4:
    #     update_and_create_pr(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    # elif len(sys.argv) == 5:
    #     update_and_create_pr(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    # else:
    #     print("Please call this script with the following args: github user name, github repo name, github token, conan remote name, conanfile (optional)")

