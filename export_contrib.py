import argparse
import csv
import datetime
import github
import os

token = os.environ.get("GITHUB_TOKEN")
parser = argparse.ArgumentParser(
    prog='export_contrib.py',
    description='Export contributor stats to csv')
parser.add_argument('--org')
args = parser.parse_args()
org_name = args.org
g = github.Github(token)

org = g.get_organization(org_name)
repos = org.get_repos()

with open("contribs.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["repo", "author", "date", "commits", "additions", "deletions"])
    for repo in repos:
        print(f"Processing repo: {repo.name}")
        contributors = repo.get_stats_contributors()
        if contributors is None:
            print(f'*** ERROR: {repo.name} is probably empty and has no contributors ***')
            continue
        for c in contributors:
            for w in c.weeks:
                if w.c > 0:
                    writer.writerow([repo.name, c.author.login, w.w.strftime('%Y-%m-%d'), w.c, w.a, w.d])

