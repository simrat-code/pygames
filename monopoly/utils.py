
import random
from sys import platform

from gamevalue import termcolorF
from gamevalue import delimiterlist


def colorText(text, color=None):
    """ 
    We cannot apply terminal-color before formating text in print()
    as text would have become 
        == f{'\033[0;33mHeader1\033[0m':<15} ==
    and after fomatting has been applied to this larger text
    terminal will remove the escape characters and thus resultant string 
    will be smaller than expected
    """
    # apply only for linux platform
    if platform != "linux" and platform != "linux2":
        return text
    # return text without processing 
    # if empty or string with whitespace only has been passed
    if len(text.strip()) == 0: return text
    if not color:
        # 'text' itself is color name
        if not termcolorF[text.upper()]: return text
        else: return termcolorF[text.upper()] + text + termcolorF['END']
    else:
        if not termcolorF[color.upper()]: return text
        else: return termcolorF[color.upper()] + text + termcolorF['END']

def highlighter(text):
    finalStr = []
    w = []
    def process():
        if w: finalStr.append( colorText(''.join(w) ))
        if c: finalStr.append(c)
        w.clear()

    for c in text:
        # word-delimiter char found
        if c in delimiterlist: process()
        else: w.append(c)
        c = ""
    # process last word
    else: process()
    return ''.join(finalStr)

def rolldice():
    return random.randint(1, 6)
