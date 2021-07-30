import enum


class Stage_1_RTLS_Mode(enum.Enum):
    """
    Modes for Falcon 9 Stage 1 with a mission profile that returns
    to the launch site (RTLS).
    """
    PAD_PASSIVE = 0  # pre-flight; don't do anything
    PAD_ACTIVE = 1  # ignite engines, decouple launch tower
    ASCENT_VERTICAL  # ascend vertically
    ASCENT_GRAVITY_TURN  # ascend with gravity turn
    POST_SEP_HOLD  # separation hold
    BOOSTBACK_FLIP  # boostback flip
    BOOSTBACK  # boostback burn
    ENTRY_FLIP  # entry flip
    ENTRY_HOLD  # entry hold
    LANDING  # land!
    TOUCHDOWN_PASSIVE  # post-landing; don't do anything
