import enum


class Stage_1_Profile(enum.Enum):
    """Ascent/landing profiles for Falcon 9 Stage 1."""
    RTLS = 0
    ASDS = 1


class Stage_1_RTLS_Mode(enum.Enum):
    """
    Modes for Falcon 9 Stage 1 with a mission profile that returns
    to the launch site (RTLS).
    """
    PAD_PASSIVE = 0  # pre-flight; don't do anything
    PAD_ACTIVE = 1  # ignite engines, decouple launch tower
    ASCENT_VERTICAL = 2  # ascend vertically
    ASCENT_GRAVITY_TURN = 3  # ascend with gravity turn
    POST_SEP_HOLD = 4  # separation hold
    BOOSTBACK_FLIP = 5  # boostback flip
    BOOSTBACK = 6  # boostback burn
    ENTRY_FLIP = 7  # entry flip
    ENTRY_HOLD = 8  # entry hold
    LANDING = 9  # land!
    TOUCHDOWN_PASSIVE = 10  # post-landing; don't do anything

    ABORT = 11  # aborted launch! shutdown everything


class Stage_1():
    """Attributes and methods for a Falcon 9 first stage."""
    
    def __init__(self, vessel, profile):
        """
        Instantiate a Stage_1 object.

        Args:
            vessel (krpc.Vessel): the first stage of the rocket
            profile (Stage_1_Profile): the ascent/landing profile to use
        """


def perform_pad_passive_ops():
    """
    Perform operations on the launch pad pre-flight (do nothing).
    """
    return None


def perform_pad_active_ops():
    """
    Ignite the engines, separate from the launch tower, and ensure
    ascent begins nominally.
    """



def main():
    pass


if __name__ == '__main__':
    main()
