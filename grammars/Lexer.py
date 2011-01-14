import sys
from DFA import SequentialTokenMatcher
import Lua

class Lexer(object):
    def __init__(self, tokens, matcher):
        self.tokens = tokens
        self.matcher = matcher
        self.ignored = ' \t\n\r'

    def setCode(self, code):
        self.code = code
        self.curpos = 0
        self.codelen = len(code)

    def nextToken(self):
        i = 0
        while self.curpos < self.codelen:
            while self.code[self.curpos] in self.ignored:
                self.curpos += 1

            m = self.matcher.match(self.tokens, self.code, self.curpos)
            if not m or m[1] == 0:
                print "Some shit happened! Code:\n" + self.code[self.curpos:self.curpos + 100]
                break

            text = self.code[self.curpos:m[1]]
            self.curpos = m[1]
            return (m[0], text)

        return None


def main():
#    if len(sys.argv) != 2:
#        print "Run as \"python %s <script.lua>\"" % sys.argv[0]
#        sys.exit()
#
#    filename = sys.argv[1]
    filename = 'test.lua'
    codelines = file(filename).readlines()
    code = ''
    for line in codelines: code += line

    l = Lexer(Lua.LuaTokens, SequentialTokenMatcher())
    l.setCode(code)
    while True:
        t = l.nextToken()
        if t is None:
            break
        print "Found %s: \"%s\"" % (t[0], t[1])


if __name__ == '__main__':
    main()
