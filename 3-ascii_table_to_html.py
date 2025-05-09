import os
import re

def is_table_border(line):
    return line.strip().startswith('+') and '-' in line

def is_table_row(line):
    return line.strip().startswith('|')

def parse_ascii_table(table_lines):
    rows = []
    for line in table_lines:
        if is_table_border(line):
            continue
        # Split by `|`, ignore first and last (empty)
        parts = [cell.strip() for cell in line.strip()[1:-1].split('|')]
        rows.append(parts)
    return rows

def to_html_table(rows):
    if not rows:
        return ""

    html = ["<table>", "  <thead>", "    <tr>"]
    for cell in rows[0]:
        html.append(f"      <th>{cell}</th>")
    html += ["    </tr>", "  </thead>", "  <tbody>"]

    for row in rows[1:]:
        html.append("    <tr>")
        for cell in row:
            # Convert Markdown links inside cells to real HTML
            cell = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', cell)
            html.append(f"      <td>{cell}</td>")
        html.append("    </tr>")
    html += ["  </tbody>", "</table>"]
    return '\n'.join(html)

def convert_tables_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    table_buffer = []
    in_table = False

    for line in lines:
        if is_table_border(line):
            if not in_table:
                in_table = True
                table_buffer = [line]
            else:
                table_buffer.append(line)
        elif in_table and is_table_row(line):
            table_buffer.append(line)
        elif in_table:
            # Table ends
            table_html = to_html_table(parse_ascii_table(table_buffer))
            new_lines.append(table_html + "\n\n")
            new_lines.append(line)
            in_table = False
            table_buffer = []
        else:
            new_lines.append(line)

    if in_table:
        table_html = to_html_table(parse_ascii_table(table_buffer))
        new_lines.append(table_html + "\n")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def convert_all_tables(base_dir='docs'):
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.md'):
                convert_tables_in_file(os.path.join(root, file))

convert_all_tables()
print("✅ Done: Converted all ASCII tables to HTML.")
