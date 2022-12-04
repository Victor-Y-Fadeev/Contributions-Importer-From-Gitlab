#!/usr/bin/python3

import pathlib
from datetime import datetime
from miromannino.git_contributions_importer import *


class GitlabImporter(Importer):

    def get_all_commits(self, ignore_before_date):
        ''' iter commits coming from any repos '''

        last_date = datetime.fromtimestamp(ignore_before_date
            if not self.ignore_before_date
                or self.ignore_before_date < ignore_before_date
            else self.ignore_before_date)

        commits = []
        for gl in self.repos:
            email = gl.user.commit_email
            for project in gl.projects.list(iterator=True, membership=True,
                    get_all=True, last_activity_after=last_date.isoformat()):

                created_at = datetime.fromisoformat(
                    project.created_at.rstrip('Z'))
                since = last_date if created_at < last_date else created_at
                for commit in project.commits.list(iterator=True, all=True,
                        get_all=True, since=since.isoformat()):

                    if commit.author_email == email:
                        commit.committed_date = datetime.fromisoformat(
                            commit.committed_date).timestamp()
                        commits.append(commit)

        commits.sort(key=lambda commit: commit.committed_date)
        return commits

    def get_changes(self, commit, stats):
        ''' for a specific commit it gets all the changed files '''

        for diff in commit.diff(iterator=True, get_all=True):
            ext = pathlib.Path(diff['new_path']).suffix
            if ext not in self.ignored_file_types:
                insertions = diff['diff'].count('\n+')
                if insertions > 0:
                    stats.add_insertions(ext, insertions)

            ext = pathlib.Path(diff['old_path']).suffix
            if ext not in self.ignored_file_types:
                deletions = diff['diff'].count('\n-')
                if deletions > 0:
                    stats.add_deletions(ext, deletions)

    def set_author(self, author):
        pass
