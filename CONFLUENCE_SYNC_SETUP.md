# Confluence Sync Setup Guide

## Step 1: Get Your Confluence API Token

1. Go to: https://id.atlassian.com/manage/api-tokens
2. Click **Create API token**
3. Give it a name: `healthcare-docs-sync`
4. Copy the token (you'll need it in Step 2)

## Step 2: Create Your Confluence Space

1. Open your Confluence instance
2. Create a new space (or use existing):
   - Space Name: `Healthcare AI Platform Docs`
   - Space Key: `HCA` (used in the sync script)

## Step 3: Install Python Dependencies

```bash
cd c:\Users\sapna.utage\Downloads\healthcare-contact-center-doc

# Activate virtual environment
source venv/Scripts/activate

# Install Confluence sync package
pip install atlassian-python-api markdown
```

## Step 4: Set Environment Variables

### On Windows (PowerShell):
```powershell
$env:CONFLUENCE_URL = 'https://your-domain.atlassian.net'
$env:CONFLUENCE_EMAIL = 'your-email@company.com'
$env:CONFLUENCE_API_TOKEN = 'YOUR_API_TOKEN_HERE'
$env:CONFLUENCE_SPACE = 'HCA'
```

### On Windows (Command Prompt):
```cmd
set CONFLUENCE_URL=https://your-domain.atlassian.net
set CONFLUENCE_EMAIL=your-email@company.com
set CONFLUENCE_API_TOKEN=YOUR_API_TOKEN_HERE
set CONFLUENCE_SPACE=HCA
```

### On Mac/Linux (Bash):
```bash
export CONFLUENCE_URL='https://your-domain.atlassian.net'
export CONFLUENCE_EMAIL='your-email@company.com'
export CONFLUENCE_API_TOKEN='YOUR_API_TOKEN_HERE'
export CONFLUENCE_SPACE='HCA'
```

## Step 5: Run the Sync

```bash
# Activate virtual environment if not already active
source venv/Scripts/activate

# Run the sync script
python sync_to_confluence.py
```

## Expected Output

```
============================================================
🔄 Healthcare AI Documentation → Confluence Sync
============================================================

🔗 Connecting to: https://your-domain.atlassian.net
✅ Connected to Confluence

📄 Setting up parent page: Healthcare AI Contact Center Platform

📚 Found 32 documentation files

Syncing to Confluence:
------------------------------------------------------------
  ✅ Creating: Business Context Overview
  ✅ Creating: Industry Challenges And Business Impact
  ...
  ✅ Creating: Glossary
------------------------------------------------------------

✅ Sync Complete!
   📄 32 pages synced
   🌐 Space: HCA
   📍 View at: https://your-domain.atlassian.net/wiki/spaces/HCA
```

## Verification

1. Open your Confluence space: `https://your-domain.atlassian.net/wiki/spaces/HCA`
2. Verify the page hierarchy:
   - Healthcare AI Contact Center Platform (parent)
     - Business Context
     - Architecture
     - Workflow
     - Component Design
     - State Management
     - Human-in-the-Loop
     - Infrastructure
     - Security & Compliance
     - API Reference
     - Deployment
     - Design Decisions
     - Roadmap
     - Glossary

## Troubleshooting

### ❌ "Failed to connect to Confluence"
- Verify your Confluence URL (no trailing slash)
- Check that your email and API token are correct
- Ensure you have access to the Confluence space

### ❌ "Missing Confluence API token"
- Verify environment variables are set correctly
- Test with: `echo $CONFLUENCE_API_TOKEN` (Mac/Linux) or `echo %CONFLUENCE_API_TOKEN%` (Windows)

### ❌ "Pages not showing up"
- Check the Confluence space key matches `CONFLUENCE_SPACE` env var
- Verify the parent page title: "Healthcare AI Contact Center Platform"
- Check Confluence permissions (your account needs to create pages)

### ⚙️ Update Existing Pages

The script automatically detects existing pages and updates them if:
- The page title matches exactly
- It's in the same space

To re-sync all docs: simply run the script again.

## Automating the Sync

### Option A: GitHub Actions (if using GitHub)
Create `.github/workflows/confluence-sync.yml`:

```yaml
name: Sync Docs to Confluence

on:
  push:
    branches:
      - main
    paths:
      - 'docs/**'

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install atlassian-python-api markdown
      - run: python sync_to_confluence.py
        env:
          CONFLUENCE_URL: ${{ secrets.CONFLUENCE_URL }}
          CONFLUENCE_EMAIL: ${{ secrets.CONFLUENCE_EMAIL }}
          CONFLUENCE_API_TOKEN: ${{ secrets.CONFLUENCE_API_TOKEN }}
          CONFLUENCE_SPACE: 'HCA'
```

### Option B: Scheduled Task (Windows)
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at 9 AM
4. Set action: `python.exe sync_to_confluence.py`
5. Set working directory to project root

## Need Help?

For issues with the sync script, check:
- [atlassian-python-api docs](https://atlassian-python-api.readthedocs.io/)
- [Confluence API docs](https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-pages/)
- Your Confluence space permissions
