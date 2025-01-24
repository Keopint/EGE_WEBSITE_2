import os


def markdown_to_html(md_text):
    html_text = ""

    lines = md_text.split('\n')
    inside_table = False
    table_lines = []

    for line in lines:
        if is_table_separator(line):
            continue
        if line.strip().startswith('|') and line.strip().endswith('|'):
            inside_table = True
            table_lines.append(line)
        else:
            if inside_table:
                html_text += process_table(table_lines)
                table_lines = []
                inside_table = False

            if line.startswith('#'):
                header_level = 0
                while line.startswith('#'):
                    header_level += 1
                    line = line[1:].strip()
                html_text += f"<h{header_level}>{line}</h{header_level}>\n"
            elif '*' in line:
                while '*' in line:
                    start_bold = line.find('*')
                    end_bold = line.find('*', start_bold + 1)
                    if end_bold == -1:
                        break
                    bold_text = line[start_bold + 1:end_bold]
                    line = line[:start_bold] + f"<strong>{bold_text}</strong>" + line[end_bold + 2:]
                html_text += f"<p>{line}</p>\n"
            elif '[[' in line and ']]' in line:
                while '[[' in line and ']]' in line:
                    start_img = line.find('[[')
                    end_img = line.find(']]', start_img)
                    if end_img == -1:
                        break
                    link = line[start_img + 2:end_img].strip()
                    el = ""
                    if "rutube.ru" in link:
                        link = link[link.rfind("/") + 1:]
                        el = f'''<iframe width="720" height="405"
                            src="https://rutube.ru/play/embed/{link}" frameBorder="0" allow="clipboard-write; autoplay"
                            webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>'''
                    elif "youtu.be" in link:
                        link = link[link.rfind("/") + 1:]
                        el = f'''<iframe width="560" height="315" src="https://www.youtube.com/embed/{link}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>'''
                    else:
                        el = f'<img src="{link}" alt="Image">'
                    # img_path = os.path.join("files", img_path[img_path.rfind("/") + 1:])
                    line = line[:start_img] + el + line[end_img + 2:]
                html_text += f"<p>{line}</p>\n"
            else:
                html_text += f"<p>{line}</p>\n"

    if inside_table:
        html_text += process_table(table_lines)
    
    return html_text

def process_table(table_lines):
    html = "<table>\n"
    header_processed = False
    
    for line in table_lines:
        line = line.strip('|').strip()
        columns = [col.strip() for col in line.split('|')]

        if not header_processed:
            html += "  <thead>\n    <tr>\n"
            for col in columns:
                html += f"      <th>{col}</th>\n"
            html += "    </tr>\n  </thead>\n  <tbody>\n"
            header_processed = True
        else:
            html += "    <tr>\n"
            for col in columns:
                html += f"      <td>{col}</td>\n"
            html += "    </tr>\n"
    
    html += "  </tbody>\n</table>\n"
    return html

def is_table_separator(line):
    """
    Check if a line is a table separator line consisting of pipes and dashes.
    """
    parts = line.strip().strip('|').split('|')
    return all(set(part.strip()) <= {'-'} for part in parts)


def main():
    with open("md_test/file.md", "r") as f:
        m = markdown_to_html(f.read(), "style.css")
    with open("md_test/file.html", "w") as f:
        f.write(m)
        

if __name__ == "__main__":
    main()