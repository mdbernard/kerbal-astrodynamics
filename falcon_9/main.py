import enum

import krpc
import numpy as np

from Falcon_9 import Falcon_9


def main():
    """
    Launch the rocket and control Stage 1.
    Assumes starting with Kerbal Space Program loaded, with the Falcon 9
    craft loaded and siting passively on the launchpad.
    """
    conn = krpc.connect()
    space_center_api = conn.space_center
    launch_vessel = space_center_api.active_vessel

    f9_stack = Falcon_9(launch_vessel)

    mission_ongoing = True
    while mission_ongoing:
        mission_ongoing = f9_stack.main(space_center_api)


if __name__ == '__main__':
    main()
