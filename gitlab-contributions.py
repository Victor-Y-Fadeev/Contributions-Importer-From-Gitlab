#!/usr/bin/python3

import os
from git import Repo, rmtree
from github import Github
from gitlab import Gitlab
from GitlabImporter import GitlabImporter


GITLAB_SERVER_URL = os.environ['GITLAB_SERVER_URL'].split()
GITLAB_TOKEN = os.environ['GITLAB_TOKEN'].split()
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']

GITHUB_USER_LOGIN = Github(GITHUB_TOKEN).get_user().login
GITHUB_USER_NAME = Github(GITHUB_TOKEN).get_user().name
GITHUB_USER_EMAIL = next(email.email for email
                         in Github(GITHUB_TOKEN).get_user().get_emails()
                         if email.primary)

GITHUB_SERVER_URL = os.getenv('GITHUB_SERVER_URL', 'https://github.com'
                             ).replace('://', '://{}@').format(GITHUB_TOKEN)
GITHUB_REPOSITORY_NAME = '{}/{}/{}'.format(GITHUB_SERVER_URL,
                                           GITHUB_USER_LOGIN,
                                           os.getenv('GITHUB_REPOSITORY_NAME',
                                                     'gitlab-contributions'))


def main():
    repo = Repo('mock') if os.path.isdir('mock') else Repo.clone_from(
                url=GITHUB_REPOSITORY_NAME, to_path='mock',
                multi_options=['--depth 1'])
    repo.config_writer().set_value('user', 'name',
                                   GITHUB_USER_NAME).release()
    repo.config_writer().set_value('user', 'email',
                                   GITHUB_USER_EMAIL).release()

    server = [Gitlab(GITLAB_SERVER_URL[i], private_token=GITLAB_TOKEN[i])
              for i in range(len(GITLAB_SERVER_URL))]
    for gl in server:
        gl.auth()

    importer = GitlabImporter(server, repo)
    importer.set_max_commits_per_day([20, 20])
    importer.set_start_from_last(True)
    importer.import_repository()

if __name__ == '__main__':
    main()
