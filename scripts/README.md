# Dynamic Profile README Scripts

This directory contains scripts that automatically update the GitHub profile README with dynamic content.

## Overview

The `update_readme.py` script is run automatically by a GitHub Actions workflow every 4 hours. It:

1. Fetches your GitHub statistics (repos, stars, forks, languages, etc.)
2. Generates custom SVG graphics showing:
   - A stats card with key metrics
   - A language usage chart based on your repositories
3. Updates the README.md file with dynamic content including:
   - Custom generated SVG graphics
   - GitHub Streak stats
   - Activity graphs
   - Trophy showcase
   - Timestamp of last update

## Components

### `update_readme.py`

Main script that handles:
- Fetching GitHub API data using PyGithub
- Calculating language statistics across repositories
- Generating SVG charts and cards
- Updating README.md with dynamic content markers

### Generated Assets

The script creates these files in `assets/images/`:
- `stats_card.svg` - Card displaying GitHub statistics
- `language_chart.svg` - Bar chart of language usage

## Dynamic Content Section

The script looks for markers in README.md:
```
<!-- DYNAMIC_CONTENT_START -->
... dynamic content ...
<!-- DYNAMIC_CONTENT_END -->
```

If these markers exist, it replaces the content between them. If not, it inserts the dynamic section before the "My open-source Projects" section.

## GitHub Actions Workflow

The workflow (`.github/workflows/update-readme.yml`) runs:
- Every 4 hours on a cron schedule
- When manually triggered (workflow_dispatch)
- On push to main branch (for testing)

## Local Testing

To test the script locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run with a GitHub token (for real data)
export GITHUB_TOKEN=your_token_here
python scripts/update_readme.py

# Run without token (uses mock data)
python scripts/update_readme.py
```

## Third-Party Services

The dynamic section also includes links to external services:
- [GitHub Readme Streak Stats](https://github.com/DenverCoder1/github-readme-streak-stats)
- [GitHub Activity Graph](https://github.com/Ashutosh00710/github-readme-activity-graph)
- [GitHub Profile Trophy](https://github.com/ryo-ma/github-profile-trophy)

## Customization

You can customize:
- **Update frequency**: Edit the cron schedule in `.github/workflows/update-readme.yml`
- **Stats displayed**: Modify the `generate_stats_card()` function
- **Languages shown**: Adjust the slice `[:8]` in `generate_language_chart()`
- **Theme colors**: Change the color values in the SVG generation functions
- **External services**: Update the URLs in the dynamic section template

## Requirements

- Python 3.11+
- Dependencies listed in `requirements.txt`:
  - requests
  - PyGithub
  - matplotlib
  - Pillow

## How It Works

1. **Schedule Trigger**: GitHub Actions runs on the defined schedule
2. **Fetch Data**: Script authenticates with GitHub API and fetches user statistics
3. **Generate Graphics**: Creates SVG files with statistics
4. **Update README**: Inserts/updates the dynamic content section
5. **Commit & Push**: GitHub Actions commits and pushes changes if README changed

## Features

✨ **Dynamic Statistics**
- Real-time GitHub metrics
- Repository counts
- Star and fork totals
- Monthly commit counts

📊 **Language Analytics**
- Automatic language detection across all repos
- Visual bar chart representation
- Percentage breakdown
- Top 8 languages displayed

🎨 **Visual Elements**
- Custom SVG graphics (no external dependencies)
- GitHub Dark theme compatible
- Responsive design
- Auto-updating timestamp

🤖 **Automation**
- No manual intervention required
- Runs every 4 hours
- Smart change detection (only commits if content changed)
- Manual trigger option available

## Troubleshooting

**Script fails with authentication error:**
- Ensure `GITHUB_TOKEN` has correct permissions in workflow
- Default `secrets.GITHUB_TOKEN` should work for most operations

**SVG graphics not displaying:**
- Check that files were created in `assets/images/`
- Verify paths in README.md are correct
- Ensure SVG files are committed to the repository

**Workflow not running:**
- Check workflow status in Actions tab
- Verify cron syntax is correct
- Ensure repository has Actions enabled

**Data seems stale:**
- Check last run time in Actions tab
- Verify workflow completed successfully
- Look for any error messages in workflow logs

## Future Enhancements

Possible additions:
- WakaTime integration for coding time tracking
- Pull request/issue statistics
- Contribution calendar visualization
- Custom themes/color schemes
- Configurable stats via config file
- More chart types (pie charts, timeline graphs)
