"""Classes of objects used across a Falcon 9 launch vehicle."""

import enum
import time

import krpc
import numpy as np

import constants


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
        self.stage_1 = Stage_1(stage_1_tags_and_parts)

        stage_2_tags_and_parts = {}
        self.stage_2 = Stage_2()

    def main(self, space_center_api):
        status = self.stage_1.main(space_center_api)
        status = self.stage_2.main(space_center_api, status)
        return status


class Stage_1:
    """Attributes and methods for a Falcon 9 first stage."""

    PART_PREFIX = 'F9_S1_'
    CONTROL_PART_TAG = PART_PREFIX + 'Interstage'
    CENTER_ENGINE_TAG = PART_PREFIX + 'Engine_1'

    def __init__(self, tag_parts_dict):
        """
        Instantiate a Stage_1 object.

        Args:
            tag_parts_dict (dict of {str: krpc.Part}): Part objects on stage 1
        """
        self.parts = tag_parts_dict
        self.control_part = self.parts[self.CONTROL_PART_TAG]
        self.vessel = self.control_part.vessel
        self.mode = Stage_1_RTLS_Mode.PAD_PASSIVE

    def main(self, space_center_api):
        status = True
        if self.mode == Stage_1_RTLS_Mode.PAD_PASSIVE:
            print('Falcon 9 is in startup.')
            for i in range(10):
                print(f'T-{10 - i}')
                time.sleep(1)
            self.mode = Stage_1_RTLS_Mode.PAD_ACTIVE
            print('Stage 1 Mode Change: PAD_ACTIVE')

        elif self.mode == Stage_1_RTLS_Mode.PAD_ACTIVE:
            # TODO: turn on SAS and set initial control pitch and heading before ignition
            self.vessel.control.sas = True
            self.vessel.control.throttle = 1.0
            self.vessel.control.activate_next_stage()
            time.sleep(constants.DT_COMMAND)
            self.vessel.control.activate_next_stage()
            print('Liftoff!')

            while not (np.linalg.norm(
                self.parts[self.CENTER_ENGINE_TAG].center_of_mass(
                    space_center_api.bodies['Kerbin'].reference_frame
                )) > constants.R0_DRAGON):
                time.sleep(0.1)
            print('Tower cleared!')

            self.mode = Stage_1_RTLS_Mode.ASCENT_VERTICAL
            print('Stage 1 Mode Change: ASCENT_VERTICAL')

        elif self.mode == Stage_1_RTLS_Mode.ASCENT_VERTICAL:
            if np.linalg.norm(self.vessel.flight(
                space_center_api.bodies['Kerbin'].reference_frame
            ).velocity) > 100:
                self.mode = Stage_1_RTLS_Mode.ASCENT_GRAVITY_TURN
                print('Stage 1 Mode Change: ASCENT_GRAVITY_TURN')

        else:
            status = False

        return status

class Stage_2:
    """Attributes and methods for a Falcon 9 second stage."""

    def __init__(self, tag_parts_dict=None, profile=None):
        # TODO: remove default None from args once __init__ is implemented
        pass

    def main(self, space_center_api, stage_1_status):
        return stage_1_status
