#!/usr/bin/python3

import os
import git
import gitlab
from GitlabImporter import GitlabImporter


GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_SERVER_URL = os.getenv('GITHUB_SERVER_URL')
GITHUB_REPOSITORY_OWNER = os.getenv('GITHUB_REPOSITORY_OWNER')

CI_SERVER_URL = os.getenv('CI_SERVER_URL')
CI_JOB_TOKEN = os.getenv('CI_JOB_TOKEN')

GITHUB_REPOSITORY_MOCK = os.getenv('GITHUB_REPOSITORY_MOCK', 'gitlab-contributions')


def main():

    print(GITHUB_TOKEN)
    print(GITHUB_SERVER_URL)
    print(GITHUB_REPOSITORY_OWNER)
    print(CI_SERVER_URL)
    print(CI_JOB_TOKEN)
    print(GITHUB_REPOSITORY_MOCK)
    print(os.environ)
    quit()

    # repo = git.Repo.clone_from(url="https://github.com/Victor-Y-Fadeev/gitlab-contributions",
    #                            to_path="mock",
    #                            multi_options=["--depth 1"])

    # quit()

    gl = gitlab.Gitlab(CI_SERVER_URL, private_token=CI_JOB_TOKEN)
    gl.auth()


    mock_repo = git.Repo("D:/Desktop/Contributions-Importer-From-Gitlab/mock")

    importer = GitlabImporter([gl], mock_repo)
    importer.set_max_commits_per_day([20, 20])
    importer.set_start_from_last(True)
    importer.import_repository()

if __name__ == '__main__':
    main()
