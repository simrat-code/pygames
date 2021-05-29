
import random

from gamevalue import termcolorF


def colorText(text, color=None):
    """ 
    We cannot apply terminal-color before formating text in print()
    as text would have become 
        == f{'\033[0;33mHeader1\033[0m':<15} ==
    and after fomatting has been applied to this larger text
    terminal will remove the escape characters and thus resultant string 
    will be smaller than expected
    """
    if not color:
        # 'text' itself is color name
        if not termcolorF[text.upper()]: return text
        else: return termcolorF[text.upper()] + text + termcolorF['END']
    else:
        if not termcolorF[color.upper()]: return text
        else: return termcolorF[color.upper()] + text + termcolorF['END']

def rolldice():
    return random.randint(1, 6)

