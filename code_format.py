import tokenize
import io

def tokenize_code(code):
    try:
        tokens = []
        token_gen = tokenize.generate_tokens(io.StringIO(code).readline)
        for toknum, tokval, start, end, line in token_gen:
            tokens.append((toknum, tokval, start, end, line))
        return tokens
    except tokenize.TokenError:
        return None

def untokenize_code(tokens):
    code = io.StringIO()
    last_end = (1, 0)  # Start from the first line, first column
    code.write('<code id="code">')
    code.write("<div>")
    for toknum, tokval, start, end, line in tokens:
        # print(toknum, f'"{tokval}"')
        if tokval == "\n" or toknum == 4:
            code.write("</div><div>")
            last_end = (start[0], 0)
            continue
        if toknum == 5:
            continue
        if start[1] > last_end[1]:
            spaces = '&nbsp;' * (start[1] - last_end[1])
            code.write(spaces)
        code.write(f"<p class=tok_{toknum}>{tokval}</p>")
        last_end = end
    code.write("</div>")
    code.write("</code>")
    return code.getvalue()

def formatcode(code: str) -> str:
    t = tokenize_code(code)
    if t is None:
        return "<h3 class='warning'>Syntax error</h3>" + code
    code = untokenize_code(t)
    return code

if __name__ == "__main__":
    prog_example = """
a = 6
print(a)
for i in range(100):
  if i % 1 == 0:
    print(":", t**2)
    """
    print(formatcode(prog_example))
