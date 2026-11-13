#!/usr/bin/env python3
"""Render compact profile cards from live, public GitHub data. No dependencies."""
import argparse
import collections
import datetime as dt
import html
import json
import os
from pathlib import Path
import urllib.request

BG, BORDER, TEXT, MUTED, CYAN, PURPLE = '#0b1020', '#24324a', '#edf2ff', '#a7b4cc', '#67e8f9', '#b6a0ff'


def text(x, y, value, size=14, color=TEXT, weight=400):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}">{html.escape(str(value))}</text>'


def card(width, height, title, body, stamp):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">
<title>{html.escape(title)}</title><rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="18" fill="{BG}" stroke="{BORDER}"/>
<g font-family="Arial, Helvetica, sans-serif">{text(24, 34, title, 17, CYAN, 600)}{body}{text(24, height-16, stamp, 10, MUTED)}</g></svg>'''


def query_github(username):
    token = os.environ['GH_TOKEN']
    query = '''query($login: String!, $cursor: String) {
      user(login: $login) {
        repositories(first: 100, after: $cursor, ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false) {
          totalCount pageInfo { hasNextPage endCursor }
          nodes { stargazerCount languages(first: 100) { edges { size node { name color } } } }
        }
        contributionsCollection {
          contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
        }
      }
    }'''
    repositories, cursor, calendar = [], None, None
    while True:
        request = urllib.request.Request('https://api.github.com/graphql', data=json.dumps({
            'query': query, 'variables': {'login': username, 'cursor': cursor}
        }).encode(), headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json', 'User-Agent': 'Mezbah-profile-visuals'})
        with urllib.request.urlopen(request, timeout=45) as response:
            result = json.load(response)
        if result.get('errors'):
            raise RuntimeError(json.dumps(result['errors']))
        user = result['data']['user']
        if not user:
            raise RuntimeError('GitHub user was not found')
        connection = user['repositories']
        repositories.extend(connection['nodes'])
        calendar = user['contributionsCollection']['contributionCalendar']
        if not connection['pageInfo']['hasNextPage']:
            return repositories, calendar
        cursor = connection['pageInfo']['endCursor']


def streaks(days):
    """Current streak may end yesterday; longest is limited to the fetched window."""
    longest = running = 0
    for day in days:
        running = running + 1 if day['contributionCount'] else 0
        longest = max(longest, running)
    current = 0
    eligible = days[:-1] if days and days[-1]['contributionCount'] == 0 else days
    for day in reversed(eligible):
        if not day['contributionCount']:
            break
        current += 1
    return current, longest


def render(repositories, calendar, output, username):
    today = dt.datetime.now(dt.timezone.utc).date()
    stamp = f'GITHUB API / UPDATED {today.isoformat()} UTC'
    days = sorted([d for week in calendar['weeks'] for d in week['contributionDays'] if d['date'] <= today.isoformat()], key=lambda d: d['date'])
    if not days or days[-1]['date'] != today.isoformat():
        raise ValueError('Contribution calendar is missing the current day')
    current, longest = streaks(days)
    stats = ''
    for y, value, label in [(80,len(repositories),'Public original repositories'), (126,sum(r['stargazerCount'] for r in repositories),'Stars across these repositories'), (172,calendar['totalContributions'],'Contributions / last 12 months')]:
        stats += text(24,y,f'{value:,}',28,TEXT,700) + text(118,y-5,label,12,MUTED)
    stats += text(24,202,'Owned repositories; forks excluded.',11,MUTED)
    cards = {'stats.svg': card(460,240,'GitHub / '+username,stats,stamp)}
    totals, colors = collections.Counter(), {}
    for repo in repositories:
        for edge in repo['languages']['edges']:
            name = edge['node']['name']
            totals[name] += edge['size']
            colors[name] = edge['node']['color'] or PURPLE
    denominator = sum(totals.values())
    top = totals.most_common(5)
    if len(totals) > 5:
        top.append(('Other', denominator-sum(n for _,n in top)))
    body, x = '', 24
    for name, amount in top:
        width = 412 * amount / denominator
        body += f'<rect x="{x:.2f}" y="55" width="{width:.2f}" height="10" rx="2" fill="{colors.get(name, MUTED)}"/>'
        x += width
    for index,(name,amount) in enumerate(top):
        x, y = 24 + (index % 2)*212, 98 + (index//2)*32
        body += f'<circle cx="{x+4}" cy="{y-4}" r="4" fill="{colors.get(name, MUTED)}"/>'
        body += text(x+16,y,f'{name} {amount/denominator:.1%}',12)
    if not top:
        body += text(24,100,'No language data available yet.',14,MUTED)
    body += text(24,202,'Public, owned, non-fork code / measured in bytes',11,MUTED)
    cards['languages.svg'] = card(460,240,'Languages / in the code',body,stamp)
    recent = days[-31:]
    maximum = max(1,max(d['contributionCount'] for d in recent))
    body = text(24,62,f'{sum(d["contributionCount"] for d in recent)} contributions in the last 31 days',14,MUTED)
    body += text(24,90,f'Current streak: {current} days    /    Longest in the last year: {longest} days',13,PURPLE)
    for tick in range(3):
        y = 122+tick*44
        body += f'<path d="M24 {y}H896" stroke="{BORDER}" stroke-dasharray="3 5"/>'
    for index,day in enumerate(recent):
        x = 24 + index * (872/31)
        count = day['contributionCount']
        height = max(2,88*count/maximum)
        body += f'<rect x="{x:.2f}" y="{210-height:.2f}" width="18" height="{height:.2f}" rx="3" fill="{CYAN if count else BORDER}"><title>{day["date"]}: {count} contributions</title></rect>'
    body += text(24,235,recent[0]['date'],11,MUTED)+text(788,235,recent[-1]['date'],11,MUTED)
    body += text(24,258,f'Bar scale: 0–{maximum} contributions/day · Contributions follow GitHub’s calendar.',11,MUTED)
    cards['activity.svg'] = card(920,295,'Activity / small steps add up',body,stamp)
    output.mkdir(parents=True,exist_ok=True)
    # Render everything before replacing any last-known-good file.
    for name,svg in cards.items():
        pending = output / (name+'.tmp')
        pending.write_text(svg,encoding='utf-8')
        pending.replace(output/name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path('dist'))
    args = parser.parse_args()
    username = os.environ.get('PROFILE_USER','Mezbah143')
    repositories, calendar = query_github(username)
    render(repositories,calendar,args.output,username)
    print(f'Generated profile statistics for {username}')


if __name__ == '__main__':
    main()
