
from pathlib import Path

# Directory containing your generated Sphinx HTML files
DOCS_DIR = Path("C:/Users/dexte/Documents/GitHub/shepai.github.io/docs/tacgym/")

# GitHub Pages static directory
GITHUB_STATIC = "https://shepai.github.io/TacTip-gym/_static/"

def fix_html_paths():
    html_files = list(DOCS_DIR.rglob("*.html"))

    updated = 0

    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")

        # Replace relative Sphinx static paths
        updated_content = content.replace(
            'href="_static/',
            f'href="{GITHUB_STATIC}'
        ).replace(
            'src="_static/',
            f'src="{GITHUB_STATIC}'
        )

        if updated_content != content:
            html_file.write_text(updated_content, encoding="utf-8")
            updated += 1
            print(f"Updated: {html_file}")

    print(f"/nFinished! Updated {updated} HTML files.")
    print(f"Scanned {len(html_files)} HTML files.")

if __name__ == "__main__":
    fix_html_paths()
