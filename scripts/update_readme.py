#!/usr/bin/env python3
"""
Dynamic README updater for GitHub profile
Generates statistics, charts, and dynamic content
"""

import os
import sys
from datetime import datetime, timezone
from typing import Dict, List
import requests
from github import Github
import random

# Configuration
GITHUB_USERNAME = "mai-space"
README_PATH = "README.md"
STATS_IMAGE_PATH = "assets/images/stats.svg"


def generate_activity_indicator() -> str:
    """Generate an activity indicator based on time of day (UTC)"""
    current_hour = datetime.now(timezone.utc).hour
    
    if 6 <= current_hour < 12:
        return "🌅 Morning coding session"
    elif 12 <= current_hour < 18:
        return "☀️ Afternoon development"
    elif 18 <= current_hour < 22:
        return "🌆 Evening productivity"
    else:
        return "🌙 Night owl coding"


def get_dev_quote() -> str:
    """Get an inspiring developer quote"""
    quotes = [
        ("Code is like humor. When you have to explain it, it's bad.", "Cory House"),
        ("First, solve the problem. Then, write the code.", "John Johnson"),
        ("Experience is the name everyone gives to their mistakes.", "Oscar Wilde"),
        ("In order to be irreplaceable, one must always be different.", "Coco Chanel"),
        ("Java is to JavaScript what car is to Carpet.", "Chris Heilmann"),
        ("Knowledge is power.", "Francis Bacon"),
        ("Sometimes it pays to stay in bed on Monday, rather than spending the rest of the week debugging Monday's code.", "Dan Salomon"),
        ("Perfection is achieved not when there is nothing more to add, but rather when there is nothing more to take away.", "Antoine de Saint-Exupery"),
        ("Code never lies, comments sometimes do.", "Ron Jeffries"),
        ("Simplicity is the soul of efficiency.", "Austin Freeman"),
        ("Make it work, make it right, make it fast.", "Kent Beck"),
        ("Clean code always looks like it was written by someone who cares.", "Robert C. Martin"),
    ]
    
    quote, author = random.choice(quotes)
    return f'"{quote}" — {author}'


def get_github_stats(token: str) -> Dict:
    """Fetch GitHub statistics using PyGithub"""
    try:
        g = Github(token)
        user = g.get_user(GITHUB_USERNAME)
        
        # Get repositories
        repos = list(user.get_repos())
        
        # Calculate statistics
        total_stars = sum(repo.stargazers_count for repo in repos)
        total_forks = sum(repo.forks_count for repo in repos)
        total_repos = len(repos)
        
        # Get language statistics
        languages = {}
        for repo in repos:
            if not repo.fork:  # Exclude forked repos
                repo_languages = repo.get_languages()
                for lang, bytes_count in repo_languages.items():
                    languages[lang] = languages.get(lang, 0) + bytes_count
        
        # Get recent activity (commits, PRs, issues)
        recent_commits = 0
        for repo in repos[:10]:  # Check last 10 repos
            try:
                commits = repo.get_commits(author=user, since=datetime.now(timezone.utc).replace(day=1))
                recent_commits += commits.totalCount
            except Exception:
                # Skip repos where we can't get commits (permissions, empty repo, etc.)
                pass
        
        return {
            'total_repos': total_repos,
            'total_stars': total_stars,
            'total_forks': total_forks,
            'languages': languages,
            'recent_commits': recent_commits,
            'public_repos': user.public_repos,
            'followers': user.followers,
            'following': user.following,
        }
    except Exception as e:
        print(f"Error fetching GitHub stats: {e}")
        return {}


def generate_language_chart(languages: Dict[str, int]) -> str:
    """Generate a language usage chart as SVG"""
    if not languages:
        return ""
    
    # Sort languages by usage
    sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:8]
    
    # Calculate percentages
    total_bytes = sum(languages.values())
    lang_percentages = [(lang, (bytes_count / total_bytes) * 100) 
                        for lang, bytes_count in sorted_langs]
    
    # Create SVG chart
    svg_parts = [
        '<svg width="500" height="200" xmlns="http://www.w3.org/2000/svg">',
        '  <style>',
        '    .lang-name { font: 12px sans-serif; fill: #666; }',
        '    .lang-bar { fill: #58a6ff; }',
        '    .percentage { font: 11px sans-serif; fill: #666; }',
        '  </style>',
    ]
    
    y_offset = 20
    bar_height = 18
    spacing = 5
    
    for lang, percentage in lang_percentages:
        bar_width = (percentage / 100) * 350
        
        svg_parts.append(f'  <text x="5" y="{y_offset}" class="lang-name">{lang}</text>')
        svg_parts.append(f'  <rect x="90" y="{y_offset - 12}" width="{bar_width}" height="{bar_height}" class="lang-bar" rx="3"/>')
        svg_parts.append(f'  <text x="450" y="{y_offset}" class="percentage">{percentage:.1f}%</text>')
        
        y_offset += bar_height + spacing
    
    svg_parts.append('</svg>')
    
    return '\n'.join(svg_parts)


def generate_stats_card(stats: Dict) -> str:
    """Generate a stats card as SVG"""
    if not stats:
        return ""
    
    svg = f'''<svg width="500" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#58a6ff;stop-opacity:0.1" />
      <stop offset="100%" style="stop-color:#1f6feb;stop-opacity:0.1" />
    </linearGradient>
  </defs>
  
  <rect width="500" height="200" fill="url(#grad1)" rx="10"/>
  <rect width="500" height="200" fill="none" stroke="#30363d" stroke-width="1" rx="10"/>
  
  <text x="250" y="30" font-family="'Segoe UI', sans-serif" font-size="18" font-weight="bold" fill="#58a6ff" text-anchor="middle">
    📊 GitHub Statistics
  </text>
  
  <g transform="translate(50, 60)">
    <text x="0" y="0" font-family="sans-serif" font-size="14" fill="#8b949e">
      <tspan x="0" dy="1.2em">🎯 Public Repositories: <tspan fill="#58a6ff" font-weight="bold">{stats.get('public_repos', 0)}</tspan></tspan>
      <tspan x="0" dy="1.8em">⭐ Total Stars: <tspan fill="#58a6ff" font-weight="bold">{stats.get('total_stars', 0)}</tspan></tspan>
      <tspan x="0" dy="1.8em">🔱 Total Forks: <tspan fill="#58a6ff" font-weight="bold">{stats.get('total_forks', 0)}</tspan></tspan>
      <tspan x="0" dy="1.8em">📝 Commits This Month: <tspan fill="#58a6ff" font-weight="bold">{stats.get('recent_commits', 0)}</tspan></tspan>
    </text>
  </g>
  
  <text x="490" y="190" font-family="sans-serif" font-size="10" fill="#484f58" text-anchor="end">
    Updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}
  </text>
</svg>'''
    
    return svg


def update_readme(stats: Dict):
    """Update README.md with dynamic content"""
    try:
        with open(README_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Generate timestamp
        timestamp = datetime.now(timezone.utc).strftime('%B %d, %Y at %H:%M UTC')
        
        # Generate dynamic sections
        stats_card_svg = generate_stats_card(stats)
        language_chart_svg = generate_language_chart(stats.get('languages', {}))
        dev_quote = get_dev_quote()
        activity_indicator = generate_activity_indicator()
        
        # Save SVG files
        os.makedirs('assets/images', exist_ok=True)
        
        with open('assets/images/stats_card.svg', 'w', encoding='utf-8') as f:
            f.write(stats_card_svg)
        
        with open('assets/images/language_chart.svg', 'w', encoding='utf-8') as f:
            f.write(language_chart_svg)
        
        # Find or create dynamic section markers
        start_marker = "<!-- DYNAMIC_CONTENT_START -->"
        end_marker = "<!-- DYNAMIC_CONTENT_END -->"
        
        dynamic_section = f'''{start_marker}

## 📈 Dynamic Statistics

<div align="center">

![GitHub Stats](assets/images/stats_card.svg)

</div>

### 💻 Language Usage This Year

<div align="center">

![Language Stats](assets/images/language_chart.svg)

</div>

### 📊 Contribution Metrics

<div align="center">

![GitHub Streak](https://github-readme-streak-stats.herokuapp.com/?user={GITHUB_USERNAME}&theme=dark&hide_border=true&date_format=M%20j%5B%2C%20Y%5D)

</div>

<div align="center">

![GitHub Activity Graph](https://github-readme-activity-graph.vercel.app/graph?username={GITHUB_USERNAME}&theme=github-compact&hide_border=true&area=true)

</div>

### 🏆 GitHub Trophies

<div align="center">

![Trophies](https://github-profile-trophy.vercel.app/?username={GITHUB_USERNAME}&theme=darkhub&no-frame=true&no-bg=true&row=1&column=7)

</div>

### 💡 Dev Quote of the Update

<div align="center">

*{dev_quote}*

</div>

---

**{activity_indicator}** | **🤖 Last auto-update:** {timestamp}

{end_marker}'''
        
        # Check if markers exist
        if start_marker in content and end_marker in content:
            # Replace existing dynamic section
            start_idx = content.find(start_marker)
            end_idx = content.find(end_marker) + len(end_marker)
            new_content = content[:start_idx] + dynamic_section + content[end_idx:]
        else:
            # Add dynamic section before the "My open-source Projects" section
            insert_marker = "## 🌍 My open-source Projects"
            if insert_marker in content:
                insert_idx = content.find(insert_marker)
                new_content = content[:insert_idx] + dynamic_section + "\n\n" + content[insert_idx:]
            else:
                # Add at the end before contact section
                insert_marker = "## 🔗 Let's get in touch"
                if insert_marker in content:
                    insert_idx = content.find(insert_marker)
                    new_content = content[:insert_idx] + dynamic_section + "\n\n" + content[insert_idx:]
                else:
                    # Just append to the end
                    new_content = content + "\n\n" + dynamic_section
        
        # Write updated content
        with open(README_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ README updated successfully!")
        
    except Exception as e:
        print(f"❌ Error updating README: {e}")
        sys.exit(1)


def main():
    """Main execution function"""
    print("🚀 Starting dynamic README update...")
    
    # Get GitHub token from environment
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        print("⚠️  GITHUB_TOKEN not found in environment variables")
        print("📊 Using mock data for testing...")
        # Mock data for testing
        stats = {
            'total_repos': 25,
            'total_stars': 42,
            'total_forks': 8,
            'languages': {
                'JavaScript': 35000,
                'Python': 28000,
                'PHP': 45000,
                'TypeScript': 22000,
                'CSS': 15000,
                'HTML': 12000,
                'Shell': 5000,
                'Java': 8000,
            },
            'recent_commits': 15,
            'public_repos': 25,
            'followers': 50,
            'following': 30,
        }
    else:
        # Fetch GitHub statistics
        print("📊 Fetching GitHub statistics...")
        stats = get_github_stats(github_token)
    
    if stats:
        print(f"   - Public repos: {stats.get('public_repos', 0)}")
        print(f"   - Total stars: {stats.get('total_stars', 0)}")
        print(f"   - Languages tracked: {len(stats.get('languages', {}))}")
    
    # Update README
    print("📝 Updating README.md...")
    update_readme(stats)
    
    print("✨ All done!")


if __name__ == "__main__":
    main()
