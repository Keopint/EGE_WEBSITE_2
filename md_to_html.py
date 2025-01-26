import os
from mdtex2html import convert
from string import ascii_letters
from random import choices


def markdown_to_html(md_text):
    return convert(links_converter((md_text)))


def get_lexer(nm="md"):
    for e in get_all_lexers():
        ok = False
        for u in e:
            if nm in u:
                ok = True
                break
        if ok:
            return e
    return None


def links_converter(md_text):
    html_text = ""

    lines = md_text.split('\n')
    inside_table = False
    table_lines = []

    iscode = False
    code = ""
    codelang = "python3"
    langs = ["py", "cpp"]

    for line in lines:
        if iscode:
            if "```" in line:
                line = line[line.find("```") + 3:]
                code += line[:line.find("```")] + "\n"
                iscode = False
                if codelang in langs:
                    codelang = "abc" + "." + codelang
                else:
                    codelang = "abc.md"
                p = random_png_filename()
                script2img(code, f"./static/img/code/{p}", codelang)
                html_text += f'<img src="/static/img/code/{p}"></img>'
                code = ""
                codelang = "md"
            else:
                code += line + "\n"
                continue
        elif "```" in line:
            code = ""
            codelang = "md"
            for e in langs:
                if line[line.find("```") + 3:].startswith(e):
                    codelang = e
                    break
            iscode = True
            continue
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
    return html_text


def random_png_filename():
    return "".join(choices(ascii_letters, k=30)) + ".png"


from pathlib import Path
from pygments import highlight
from pygments.formatters import ImageFormatter
from pygments.lexers import get_lexer_for_filename, get_all_lexers, get_lexer_by_name
from pygments.style import Style
import pygments.token as tokens


class MyStyle(Style):
    background_color = '#00122a'

    # Only applies to HtmlFormatter
    line_number_background_color = '#003b6f'
    line_number_color = '#ff69b4'

    styles = {
        tokens.Keyword: f'bold #07487f bg:{background_color}',
        tokens.Name: f'#7b68ee bg:{background_color}',
        tokens.Name.Builtin: 'italic #fb4570',
        tokens.Name.Class: 'bold italic #ffd700',
        tokens.Name.Constant: 'bold',
        tokens.Name.Decorator: 'bold italic',
        tokens.Name.Exception: 'bold italic #ff005d',
        tokens.Name.Function: 'bold italic #134dbc',
        tokens.Name.Namespace: 'bold italic #ffa000',
        tokens.Name.Variable.Class: 'bold',
        tokens.Name.Variable.Global: 'bold',
        tokens.Literal: f'#00ff80 bg:{background_color}',
        tokens.String: f'#20ff40 bg:{background_color}',
        tokens.String.Escape: 'italic #d06000',
        tokens.Number: f'#00c0ff bg:{background_color}',
        tokens.Operator: f'bold #408020 bg:{background_color}',
        tokens.Operator.Word: 'bold #0000f0',
        tokens.Punctuation: f'#ff00c0 bg:{background_color}',
        tokens.Comment: f'italic #800080 bg:{background_color}',
    }


def script2img(text, outpath, codelang="md") -> None:
    formatter = ImageFormatter(
        style=MyStyle, full=True, line_pad=3,
        font_size=16,
        line_number_bold=True,
        line_number_fg=MyStyle.line_number_color,
        line_number_bg=MyStyle.line_number_background_color,
    )
    buffer = highlight(
        code=text,
        lexer=get_lexer_for_filename(codelang),
        formatter=formatter,
    )
    with open(outpath, 'wb') as f:
        f.write(buffer)


def main():
    with open("md_test/file.md", "r") as f:
        m = markdown_to_html(f.read())
    with open("md_test/file.html", "w") as f:
        f.write(m)
        

if __name__ == "__main__":
    # script2img(Path('1.py'))
    main()
    # print(get_lexer("py"))