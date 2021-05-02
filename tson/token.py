import re
import sys

SINGLE_CHAR_ESCAPES = {
    '"': '"',
    '\\': '\\',
    '/': '/',
    'b': '\b',
    'f': '\f',
    'n': '\n',
    'r': '\r',
    't': '\t'
}

LABEL_RE = "[a-zA-Z_][a-zA-Z0-9_]*"
NUMERIC_RE = r"-?[0-9]+(\.[0-9]+)?"

BOOLS = {
    "true": True,
    "false": False,
}

DECLARERS = {
    "type",
    "let",
}


class Token:
    LABEL = "LABEL"
    NUMBER = "NUMBER"
    BOOL = "BOOL"
    STRING = "STRING"
    DECLARER = "DECLARER"
    NULL = "null"
    UNDEFINED = "undefined"

    def __init__(self, line_no, col_no, line, s, ttype, value):
        self.line_no = line_no
        self.col_no = col_no
        self.line = line
        self.s = s
        self.ttype = ttype
        self.value = value

    def raise_error(self, message):
        print(f"Line {self.line_no}, column {self.col_no}")
        print(self.line)
        print(' '*self.line_no + '^' + '~' * (len(self.s) - 1))
        print(message)
        sys.exit()

    def __repr__(self):
        return f"Token(line_no={self.line_no+1}, col_no={self.col_no+1}, s={repr(self.s)}, ttype={repr(self.ttype)}, value={repr(self.value)})"

    @staticmethod
    def resolve_symbol(s):
        if s in BOOLS:
            return BOOLS[s], Token.BOOL

        elif s in DECLARERS:
            return s, Token.DECLARER

        elif s in KEYWORDS:
            return None, s

        else:
            return s, Token.LABEL


KEYWORDS = {
    "let",
    "type",
    "import",
    "export",
    Token.NULL,
    Token.UNDEFINED
}


class Tokenizer:
    def __init__(self, lines):
        self.lines = lines

    def tokens(self):
        self.line_no = 0
        self.col_no = 0

        self.pass_whitespace()

        while not self.eof():
            yield self.grab_token()

    def eof(self):
        return self.line_no == len(self.lines) - 1 and self.eol()

    def eol(self):
        return self.col_no == len(self.current_line())

    def newline(self):
        self.line_no += 1
        self.col_no = 0

    def current_line(self):
        return self.lines[self.line_no]

    def rest(self):
        return self.current_line()[self.col_no:]

    def next(self, i=1):
        return self.current_line()[self.col_no:min(self.col_no+i, len(self.current_line()))]

    def pass_whitespace(self):
        while True:
            if self.eof():
                break

            elif self.eol():
                self.newline()

            elif self.next() in ' \t\r\n':
                self.col_no += 1

            else:
                break

    def grab_token(self):
        line_no = self.line_no
        col_no = self.col_no
        line = self.current_line()

        label = re.match(LABEL_RE, self.rest())
        number = re.match(NUMERIC_RE, self.rest())

        if number:
            s = number.group()
            val = int(s)
            ttype = Token.NUMBER
            self.col_no += len(s)

        elif label:
            s = label.group()
            val, ttype = Token.resolve_symbol(s)
            self.col_no += len(s)

        # TODO: strings

        else:
            s = self.next()
            val = None
            ttype = s
            self.col_no += 1

        self.pass_whitespace()

        return Token(
            line_no=line_no,
            col_no=col_no,
            line=line,
            s=s,
            value=val,
            ttype=ttype,
        )
