#!/usr/bin/env python3
"""
Sync MkDocs documentation to Confluence
Converts markdown pages and preserves the documentation hierarchy
"""

import os
import sys
from pathlib import Path
from atlassian import Confluence
import markdown
import re

# ===== CONFIGURATION =====
CONFLUENCE_URL = os.getenv('CONFLUENCE_URL', 'https://your-domain.atlassian.net')
CONFLUENCE_EMAIL = os.getenv('CONFLUENCE_EMAIL', '[REDACTED_EMAIL_ADDRESS_1]')
CONFLUENCE_API_TOKEN = os.getenv('CONFLUENCE_API_TOKEN', 'YOUR_API_TOKEN')
SPACE_KEY = os.getenv('CONFLUENCE_SPACE', 'HCA')  # Space key
PARENT_PAGE_TITLE = 'Healthcare AI Contact Center Platform'

# ===== SECTION TO PARENT PAGE MAPPING =====
SECTION_HIERARCHY = {
    'docs/index.md': None,  # Root home page
    'docs/business-context': 'Business Context',
    'docs/architecture': 'Architecture',
    'docs/workflow': 'Workflow',
    'docs/components': 'Component Design',
    'docs/state': 'State Management',
    'docs/hitl': 'Human-in-the-Loop',
    'docs/infrastructure': 'Infrastructure',
    'docs/security': 'Security & Compliance',
}

def convert_markdown_to_confluence(md_content):
    """Convert markdown to Confluence markup format"""
    # Convert markdown headers to Confluence format
    content = re.sub(r'^# (.*?)$', r'h1. \1', md_content, flags=re.MULTILINE)
    content = re.sub(r'^## (.*?)$', r'h2. \1', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.*?)$', r'h3. \1', content, flags=re.MULTILINE)

    # Convert **bold** to *bold*
    content = re.sub(r'\*\*(.*?)\*\*', r'*\1*', content)

    # Convert code blocks
    content = re.sub(
        r'```(\w+)?\n(.*?)\n```',
        r'{code:\1}\n\2\n{code}',
        content,
        flags=re.DOTALL
    )

    # Convert inline code
    content = re.sub(r'`(.*?)`', r'{{\1}}', content)

    # Convert links [text](url) to [text|url]
    content = re.sub(r'\[(.*?)\]\((.*?)\)', r'[\1|\2]', content)

    # Convert bullet lists - already compatible
    # Convert numbered lists - already compatible

    # Convert tables (basic support)
    # Confluence tables need special formatting - keep as is for now

    return content

def get_parent_page_id(confluence, parent_title):
    """Get page ID of parent page, create if doesn't exist"""
    try:
        pages = confluence.get_all_pages_from_space(SPACE_KEY, limit=500)
        for page in pages:
            if page['title'] == parent_title:
                return page['id']

        # Create parent page if it doesn't exist
        print(f"  ℹ️  Creating parent page: {parent_title}")
        new_page = confluence.create_page(
            space=SPACE_KEY,
            title=parent_title,
            body='Overview of the Healthcare AI Contact Center Platform documentation.'
        )
        return new_page['id']
    except Exception as e:
        print(f"  ⚠️  Error getting parent page: {e}")
        return None

def get_section_parent_id(confluence, section_path):
    """Get parent page ID for a section"""
    for pattern, section_name in SECTION_HIERARCHY.items():
        if pattern != 'docs/index.md' and str(section_path).startswith(pattern):
            if section_name:
                try:
                    pages = confluence.get_all_pages_from_space(SPACE_KEY, limit=500)
                    for page in pages:
                        if page['title'] == section_name:
                            return page['id']
                    # Create section parent if it doesn't exist
                    parent_id = get_parent_page_id(confluence, PARENT_PAGE_TITLE)
                    print(f"  ℹ️  Creating section: {section_name}")
                    new_page = confluence.create_page(
                        space=SPACE_KEY,
                        title=section_name,
                        body='',
                        parent_id=parent_id
                    )
                    return new_page['id']
                except Exception as e:
                    print(f"  ⚠️  Error getting section parent: {e}")
    return get_parent_page_id(confluence, PARENT_PAGE_TITLE)

def get_existing_page_id(confluence, title):
    """Check if page already exists and return its ID"""
    try:
        pages = confluence.get_all_pages_from_space(SPACE_KEY, limit=500)
        for page in pages:
            if page['title'] == title:
                return page['id']
    except Exception as e:
        print(f"  ⚠️  Error checking existing pages: {e}")
    return None

def sync_file_to_confluence(confluence, file_path, title, parent_id):
    """Sync a single markdown file to Confluence"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Convert markdown to Confluence format
        confluence_content = convert_markdown_to_confluence(md_content)

        # Check if page exists
        existing_id = get_existing_page_id(confluence, title)

        if existing_id:
            print(f"  ♻️  Updating: {title}")
            confluence.update_page(
                page_id=existing_id,
                title=title,
                body=confluence_content
            )
        else:
            print(f"  ✅ Creating: {title}")
            confluence.create_page(
                space=SPACE_KEY,
                title=title,
                body=confluence_content,
                parent_id=parent_id
            )
    except Exception as e:
        print(f"  ❌ Error syncing {title}: {e}")

def main():
    """Main sync function"""
    print("\n" + "="*60)
    print("🔄 Healthcare AI Documentation → Confluence Sync")
    print("="*60 + "\n")

    # Validate configuration
    if CONFLUENCE_API_TOKEN == 'YOUR_API_TOKEN':
        print("❌ ERROR: Missing Confluence API token!")
        print("\nSet environment variables:")
        print("  export CONFLUENCE_URL='https://your-domain.atlassian.net'")
        print("  export CONFLUENCE_EMAIL='your-email@example.com'")
        print("  export CONFLUENCE_API_TOKEN='your-api-token'")
        print("  export CONFLUENCE_SPACE='HCA'")
        print("\nGet your API token: https://id.atlassian.com/manage/api-tokens")
        sys.exit(1)

    # Initialize Confluence client
    try:
        print(f"🔗 Connecting to: {CONFLUENCE_URL}")
        confluence = Confluence(
            url=CONFLUENCE_URL,
            username=CONFLUENCE_EMAIL,
            password=CONFLUENCE_API_TOKEN,
            cloud=True
        )
        print("✅ Connected to Confluence\n")
    except Exception as e:
        print(f"❌ Failed to connect to Confluence: {e}")
        print("\nVerify your credentials and try again.")
        sys.exit(1)

    # Create/get parent page
    print(f"📄 Setting up parent page: {PARENT_PAGE_TITLE}\n")
    parent_id = get_parent_page_id(confluence, PARENT_PAGE_TITLE)

    if not parent_id:
        print("❌ Failed to create parent page")
        sys.exit(1)

    # Sync all markdown files
    docs_path = Path('docs')
    md_files = sorted(docs_path.glob('**/*.md'))

    if not md_files:
        print("❌ No markdown files found in docs/ directory")
        sys.exit(1)

    print(f"📚 Found {len(md_files)} documentation files\n")
    print("Syncing to Confluence:")
    print("-" * 60)

    synced_count = 0
    for md_file in md_files:
        # Skip index files handled separately
        if md_file.name == 'index.md':
            continue

        # Generate page title from filename
        title = md_file.stem.replace('-', ' ').title()

        # Get appropriate parent page
        section_parent_id = get_section_parent_id(confluence, md_file.parent)

        # Sync to Confluence
        sync_file_to_confluence(confluence, md_file, title, section_parent_id)
        synced_count += 1

    print("-" * 60)
    print(f"\n✅ Sync Complete!")
    print(f"   📄 {synced_count} pages synced")
    print(f"   🌐 Space: {SPACE_KEY}")
    print(f"   📍 View at: {CONFLUENCE_URL}/wiki/spaces/{SPACE_KEY}")
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    main()
