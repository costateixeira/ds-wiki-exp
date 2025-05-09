import os
import xml.etree.ElementTree as ET
import subprocess

EXPORT_FILE = "Digital+Square-20250509074433.xml"
OUTPUT_DIR = "_docs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

tree = ET.parse(EXPORT_FILE)
root = tree.getroot()

# Extract the namespace from the root tag
ns = {'mw': root.tag.split('}')[0].strip('{')}

page_count = 0

for page in root.findall("./mw:page", ns):
    title_elem = page.find("./mw:title", ns)
    text_elem = page.find("./mw:revision/mw:text", ns)

    if title_elem is None or text_elem is None or text_elem.text is None:
        continue

    title = title_elem.text
    content = text_elem.text
    safe_title = title.replace(" ", "_").replace("/", "_")
    wiki_file = f"tmp/{safe_title}.wiki"
    md_file = os.path.join(OUTPUT_DIR, f"{safe_title}.md")

    print(f"Converting: {title}")
    page_count += 1

    with open(wiki_file, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        subprocess.run([
            "pandoc", "-f", "mediawiki", "-t", "markdown", wiki_file, "-o", md_file
        ], check=True)
    except subprocess.CalledProcessError:
        print(f"⚠️ Pandoc failed on: {title}")
        continue

    with open(md_file, "r+", encoding="utf-8") as f:
        existing = f.read()
        f.seek(0, 0)
        f.write(f"---\ntitle: {title}\nnav_order: 1\n---\n\n{existing}")

if page_count == 0:
    print("❌ No pages found. Check if your XML file has a namespace or is empty.")
else:
    print(f"✅ Done. Converted {page_count} pages.")
