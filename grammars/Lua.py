from DFA import DFA, LETTERS, DIGITS, OTHERS

_keywords = ['and', 'break', 'do', 'else', 'elseif', 'end', 'false', 'for',
             'function', 'if', 'in', 'local', 'nil', 'not', 'or', 'repeat',
             'return', 'then', 'true', 'until', 'while']

_operators = ['+', '-', '*', '/', '%', '^', '#', '==', '~\=', '<=', '>=',
              '<', '>', '=', '(', ')', '{', '}', '[', ']', ';', ':',
              '.', '..', '...', ',']

def _IdentifierDFA():
    dfa = DFA()
    dfa.addStates(["id0", "idfin"])
    dfa.state = dfa.states[0]
    dfa.final = dfa.states[-1]
    dfa.addTransition("id0", "idfin", LETTERS + "_")
    dfa.addTransition("idfin", "idfin", DIGITS + LETTERS + "_")
    return dfa

def _NumberDFA():
    dfa = DFA()
    dfa.addStates(["number_0", "NUMBER"])
    dfa.state = dfa.states[0]
    dfa.final = dfa.states[-1]
    dfa.addTransition("number_0", "NUMBER", DIGITS)
    dfa.addTransition("NUMBER", "NUMBER", DIGITS)
    return dfa

def _LineCommentDFA():
    dfa = DFA()
    dfa.addStates(["lc0", "lc1", "lcloop", "lcfin"])
    dfa.state = dfa.states[0]
    dfa.setFinal("lcfin")
    dfa.addTransition("lc0", "lc1", "-")
    dfa.addTransition("lc1", "lcloop", "-")
    dfa.addTransition("lcloop", "lcloop", LETTERS + DIGITS + OTHERS + " \t")
    dfa.addTransition("lcloop", "lcfin", "\n")
    return dfa

def _LiteralDFA():
    dfa = DFA()
    dfa.addStates(["l0", "lloop", "lescape", "lfin"])
    dfa.state = dfa.states[0]
    dfa.setFinal("lfin")
    dfa.addTransition("l0", "lloop", "\"")
    loopchars = (LETTERS + DIGITS + OTHERS + " \n\r\t").replace("\\", "").replace("\"", "")
    dfa.addTransition("lloop", "lloop", loopchars)
    dfa.addTransition("lloop", "lescape", "\\")
    dfa.addTransition("l0", "lescape", "\\")
    dfa.addTransition("lescape", "lloop", "ntr\"\'\\")
    dfa.addTransition("lloop", "lfin", "\"")
    return dfa


def _MultiLineCommentDFA():
    dfa = DFA()
    dfa.addStates(["q0", "q1", "q2", "q3", "qloop", "q4", "q5"])
    dfa.state = "q0"
    dfa.setFinal("q5")
    dfa.addTransition("q0", "q1", "-")
    dfa.addTransition("q1", "q2", "-")
    dfa.addTransition("q2", "q3", "[")
    dfa.addTransition("q3", "qloop", "[")
    loopchars = (LETTERS + DIGITS + OTHERS + " \t\n\r").replace("]", "")
    dfa.addTransition("qloop", "qloop", loopchars)
    dfa.addTransition("qloop", "q4", "]")
    dfa.addTransition("q4", "qloop", loopchars)
    dfa.addTransition("q4", "q5", "]")

    return dfa

LuaTokens = map(lambda str: (str, DFA.createString(str)), _operators + _keywords)
LuaTokens += [("LINE_COMMENT", _LineCommentDFA()),
              ("MULTILINE_COMMENT", _MultiLineCommentDFA()),
              ("NUMBER", _NumberDFA()),
              ("LITERAL", _LiteralDFA()),
              ("IDENTIFIER", _IdentifierDFA())]

#LuaConfig = LexerConfig()
#LuaConfig.addToken(r'--\[\[(.|\n)*\]\]', 'MULTILINE_COMMENT')
#LuaConfig.addToken(r'--.*\n', 'LINE_COMMENT')
#LuaConfig.addToken(r'[a-zA-Z]+\w*', 'IDENTIFIER')
#LuaConfig.addToken(r'[0-9]+', 'NUMBER')
#LuaConfig.addToken(r'\"([^\\\n]|(\\(.|\n)))*?\"', 'STRING')
#[LuaConfig.addKeyword(re.escape(keyword)) for keyword in _keywords]
#[LuaConfig.addKeyword(re.escape(op)) for op in _operators]
