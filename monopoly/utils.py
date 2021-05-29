
import random

from gamevalue import termcolorF


def getColorText(text, color):
    return termcolorF[color.upper()] + text + termcolorF['END']

def rolldice():
    return random.randint(1, 6)

