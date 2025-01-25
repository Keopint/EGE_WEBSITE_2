import os
from mdtex2html import convert


def markdown_to_html(md_text):
    return links_converter(convert(md_text))


def links_converter(md_text):
    html_text = ""

    lines = md_text.split('\n')
    inside_table = False
    table_lines = []

    for line in lines:
        if '[[' in line and ']]' in line:
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
    return html_text


def main():
    with open("md_test/file.md", "r") as f:
        m = markdown_to_html(f.read(), "style.css")
    with open("md_test/file.html", "w") as f:
        f.write(m)
        

if __name__ == "__main__":
    main()