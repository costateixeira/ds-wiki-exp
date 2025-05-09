import os

BASE_DIR = "docs"
NAV_START = 1

def title_from_filename(filename):
    return os.path.splitext(os.path.basename(filename))[0].replace("-", " ").replace("_", " ").title()

for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".md"):
            filepath = os.path.join(root, file)

            with open(filepath, "r+", encoding="utf-8") as f:
                content = f.read()

                if content.lstrip().startswith('---'):
                    continue  # frontmatter exists

                parts = root[len(BASE_DIR):].strip(os.sep).split(os.sep)
                parent = parts[-1].replace("-", " ").title() if parts else None
                title = title_from_filename(file)

                nav_order = NAV_START

                lines = ["---"]
                lines.append(f"title: {title}")
                if len(parts) == 1 and parent:
                    lines.append(f"parent: {parent}")
                elif len(parts) == 2:
                    lines.append(f"parent: {parts[-1].replace('-', ' ').title()}")
                    lines.append(f"grand_parent: {parts[-2].replace('-', ' ').title()}")
                lines.append(f"nav_order: {nav_order}")
                lines.append("---\n")

                f.seek(0)
                f.write('\n'.join(lines) + '\n' + content)
                f.truncate()

print("✅ Front matter added where missing.")
