from settings import *

# This file will handle the final polish of the "Crown" visual and Portal destruction logic
# which are partly in `enemies.py` and `player.py` but need integration.

def check_win_condition(portals):
    if len(portals) == 0:
        print("VICTORY! All portals destroyed.")
        return True
    return False
