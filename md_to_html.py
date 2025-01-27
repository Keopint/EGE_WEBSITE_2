import re
from code_format import formatcode
from mdtex2html import convert

def latex(latex_code):
    print(latex_code)
    return f"<span class='latex'>{convert('$' + latex_code + '$')}</span>"

def markdown_to_html(markdown):
    code_blocks = re.findall(r'```(.*?)```', markdown, flags=re.DOTALL)
    formatted_code_blocks = [formatcode(block) for block in code_blocks]

    code_placeholders = []
    def replace_code_block(match):
        code_placeholders.append(match.group(0))
        return f'PLACEHOLDER{len(code_placeholders) - 1}'

    markdown = re.sub(r'```(.*?)```', replace_code_block, markdown, flags=re.DOTALL)



    latex_blocks = re.findall(r'\$\$(.*?)\$\$', markdown, flags=re.DOTALL)
    formatted_latex_blocks = [latex(block) for block in latex_blocks]

    latex_placeholders = []
    def replace_latex_block(match):
        latex_placeholders.append(match.group(0))
        return f'LATEXPLACEHOLDER{len(latex_placeholders) - 1}'

    markdown = re.sub(r'\$\$(.*?)\$\$', replace_latex_block, markdown, flags=re.DOTALL)


    # Замена специальных символов
    markdown = markdown.replace('&', '&amp;')
    markdown = markdown.replace('<', '&lt;')
    markdown = markdown.replace('>', '&gt;')
    markdown = markdown.replace('"', '&quot;')
    markdown = markdown.replace("'", '&#39;')
    markdown = markdown.replace("\n", "\n<p></p>\n")

    # Замена LaTeX вставками
    markdown = re.sub(r'\$(.*?)\$', lambda match: latex(match.group(1)), markdown)

    # Заголовки
    markdown = re.sub(r'^(#{1,6})\s+(.*)', lambda match: f"<h{len(match.group(1))}>{match.group(2)}</h{len(match.group(1))}>", markdown, flags=re.MULTILINE)

    # Курсив и жирный шрифт
    markdown = re.sub(r'\*(.*?)\*', r'<em>\1</em>', markdown)
    markdown = re.sub(r'_(.*?)_', r'<em>\1</em>', markdown)
    markdown = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', markdown)
    markdown = re.sub(r'__(.*?)__', r'<strong>\1</strong>', markdown)
    markdown = re.sub(r'\*\*\*(.*?)\*\*\*', r'<em><strong>\1</strong></em>', markdown)
    markdown = re.sub(r'___(.*?)___', r'<em><strong>\1</strong></em>', markdown)

    # Списки
    markdown = re.sub(r'^\d+\.\s+(.*)', r'<li>\1</li>', markdown, flags=re.MULTILINE)
    markdown = re.sub(r'^[*-+]\s+(.*)', r'<li>\1</li>', markdown, flags=re.MULTILINE)

    # Изображения
    markdown = re.sub(r'\!\[(.*?)\]\((.*?)\)', r'<div><img src="\2" alt="\1"></div>', markdown)

    # Ссылки
    markdown = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', markdown)

    # Видео
    markdown = re.sub(r'\[\[(.*?)\]\]', r'''<div><iframe width="720" height="405"
                      src="https://rutube.ru/play/embed/\1" frameBorder="0" allow="clipboard-write; autoplay"
                      webkitAllowFullScreen mozallowfullscreen allowFullScreen>
                      </iframe></div>''', markdown)

    # Цитаты
    markdown = re.sub(r'^>\s+(.*)', r'<div><blockquote>\1</blockquote></div>', markdown, flags=re.MULTILINE)

    # Горизонтальные линии
    markdown = re.sub(r'^(---|\*\*\*|___)', r'<hr>', markdown, flags=re.MULTILINE)

    # Таблицы
    markdown = re.sub(r'^\|(.*)\|', lambda match: "<tr>{}</tr>".format(re.sub(r'\|', '</td><td>', match.group(1))), markdown, flags=re.MULTILINE)
    markdown = re.sub(
        r'^\|(.*?)\|\s*\n\|(.*?)\|',
        lambda match: (
            "<table><thead><tr>{}</tr></thead><tbody><tr>{}</tr></tbody></table>"
            .format(
                re.sub(r'\|', '</th><th>', match.group(1)),
                re.sub(r'\|', '</td><td>', match.group(2))
            )
        ),
        markdown,
        flags=re.MULTILINE
    )

    for i, block in enumerate(formatted_latex_blocks):
        markdown = markdown.replace(f'LATEXPLACEHOLDER{i}', block)

    # Replace placeholders with formatted code blocks
    for i, block in enumerate(formatted_code_blocks):
        markdown = markdown.replace(f'PLACEHOLDER{i}', block)

    return markdown
