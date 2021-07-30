"""Classes of objects used across a Falcon 9 launch vehicle."""

import enum

import krpc


class Stage_1_Profile(enum.Enum):
    """Ascent/landing profiles for Falcon 9 Stage 1."""
    RTLS = 0


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


class Falcon_9:
    """Attributes and methods for a full Falcon 9 stack."""

    def __init__(self, launch_vessel):
        """
        Set the control parts for the Falcon 9 vehicle.

        Args:
            launch_vessel (krpc.Vessel): initial full stack vessel on pad
        """
        parts = launch_vessel.parts.all
        vessel_tags_and_parts = {part.tag: part for part in parts}

        stage_1_tags = (['Interstage', 'Tank'] +
                        [f'Engine_{i}' for i in range(1, 10)])
        stage_1_tags_and_parts = {
            'F9_S1_' + tag: vessel_tags_and_parts['F9_S1_' + tag]
            for tag in stage_1_tags
        }
        self.stage_1 = Stage_1(stage_1_tags_and_parts, Stage_1_Profile.RTLS)

        stage_2_tags_and_parts = {}


class Stage_1:
    """Attributes and methods for a Falcon 9 first stage."""

    CONTROL_PART_TAG = 'F9_S1_Interstage'

    def __init__(self, tag_parts_dict, profile):
        """
        Instantiate a Stage_1 object.

        Args:
            tag_parts_dict (dict of {str: krpc.Part}): Part objects on stage 1
            profile (Stage_1_Profile): the ascent/landing profile to use
        """
        self.parts = tag_parts_dict
        self.profile = profile
        self.control_part = self.parts[self.CONTROL_PART_TAG]
        self.vessel = self.control_part.vessel
        self._determine_init_mode()  # sets self.mode

    def _determine_init_mode(self):
        """
        Determine which mode enumeration to use initially
        based on flight profile.
        """
        if self.profile == Stage_1_Profile.RTLS:
            self.mode = Stage_1_RTLS_Mode.PAD_PASSIVE
        else:
            self.mode = None


class Stage_2:
    """Attributes and methods for a Falcon 9 second stage."""

    def __init__(self, control_part, profile):
        pass
