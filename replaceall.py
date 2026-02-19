import os

root_dir = "."  # change to your root folder if needed

old_line = '<a align="right" href="https://scholar.google.com/citations?hl=en&user=hJSy6CYAAAAJ" class="ai ai-google-scholar ai-2x"></a>'
new_line = """<a align="right" href="https://scholar.google.com/citations?hl=en&user=hJSy6CYAAAAJ" class="ai ai-google-scholar ai-2x"></a>
<a align="right" href="https://github.com/shepai" class="fa fa-github"></a>"""

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".html"):
            file_path = os.path.join(root, file)

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            if old_line in content:
                content = content.replace(old_line, new_line)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)

                print(f"Updated: {file_path}")
