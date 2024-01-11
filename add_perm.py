import argparse
import github
import os

token = os.environ.get("GITHUB_TOKEN")

parser = argparse.ArgumentParser(
    prog='add_perm.py',
    description='Give permission to a team to all repos in an org')
parser.add_argument('--org')
parser.add_argument('--team')
args = parser.parse_args()
org = args.org
team_name = args.team
perms = "push"

g = github.Github(token)

orgs = g.get_organization(org)
team = None
for t in orgs.get_teams():
    if t.name == team_name:
        team = t
        break

if not team:
    print(f"Team '{team_name}' not found")
    exit()

repos = orgs.get_repos()
for repo in repos:
    team.update_team_repository(repo, perms)
    print(f"Gave '{team_name}' team '{perms}' access to '{repo.name}'")

print(f"Gave '{team_name}' team '{perms}' access to all repos in '{org}'")
