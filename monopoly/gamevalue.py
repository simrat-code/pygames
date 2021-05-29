
from collections import defaultdict

cardcolor = ("Red", "Green", "Blue", "Yellow", "Black")
cardtype = ("City", "Corp", "Banker", "Tax")
buyable = ("City", "Corp")

termcolorF = defaultdict(lambda: "\033[0m", {
    "red".upper(): '\033[31;1m',
    "green".upper(): '\033[32;1m',
    "yellow".upper(): '\033;33;1m',
    "blue".upper(): '\033[34;1m',
    "end".upper(): '\033[0m'
})