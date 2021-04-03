"""

Base classes for entities and animation as well as supporting constants.

This includes the following:
    - NamedAnimatedSprite, the base stateful animated sprite
    - State constants that represent common states used by multiple entities
    - Actor, the baseclass for mobile and other game entities

"""
from collections import defaultdict
from random import choice
from typing import List, Tuple

from arcade import Sprite
from arcade import SpriteList

from CatBurglar.util import CountdownTimer
# Typing annotation that describes a generic mapping
# froms string to list of textures.
from CatBurglar.util.asset_loading import AnimationStateDict

"""

Common animation state constants

All mobile actors are expected to have entries for these in the state maps
for their class. Attempting to instantiate, and maybe even run the definition
of, a mobile actor that doesn't have these in the state map should return an
error.

"""

# ground-based actors

# Default non-moving animation states for actors
STILL_RIGHT = "still_right"
STILL_LEFT = "still_left"

# Walking states
WALK_RIGHT = "walk_right"
WALK_LEFT = "walk_left"

REQUIRED_FOR_ACTORS = [
    STILL_RIGHT,
    STILL_LEFT,
    WALK_RIGHT,
    WALK_LEFT
]

# optional still states, intended to be used for NPC actors
STILL_FACINGCAMERA = "still_facing"
STILL_AWAYCAMERA = "still_awaycamera"

# flying states
FLY_LEFT = "fly_left"
FLY_RIGHT = "fly_right"
FLY_HOVER = "fly_hover"
DRONE_REQUIRED_STATES = [
    FLY_LEFT,
    FLY_RIGHT,
    FLY_HOVER
]

class NamedAnimationsSprite(Sprite):
    """

    Animation support for multiple named states.

    It isn't only for Actors. Non-moving entities can use it too!
    Coffee makers, ringing telephones, and many other items that would need to
    move to attract the player's attention can use this!

    The design expands upon some of the ideas in AnimatedWalkingSprite by
    allowing an arbitrary number of animations to be stored mapped to names,
    aka strings.

    !!! This design is not final !!!

     There are a number of issues with it.
        1. Not sure if the current model of organizing animations makes sense,
            ie is walk_left_0.png worthwhile? should there be more parts to the name?
            or should this baseclass only care about the state name and number, leaving
            validation up to subclasses and helper methods?

        2. Animations might be better encapsulated as objects than they are now.

        3. Restricting to strings might be silly, enums might be better?

    It may also be a good idea to improve upon the animation types that currently
    exist in the doc.

    """

    def reset_animation_to_start(self):
        self.current_animation_frame_index = 0
        self.frame_timer.remaining = self.frame_length
        self.update_animation(0.0)

    @property
    def current_animation_name(self):
        return self._current_animation_name

    @current_animation_name.setter
    def current_animation_name(self, new_animation_name: str) -> str:
        if self._current_animation_name != new_animation_name:
            self._current_animation_name = new_animation_name
            self.current_animation_frames = self.animations[new_animation_name]
            self.reset_animation_to_start()

    @property
    def animation_expiring(self) -> bool:
        """
        Convenience property to tell when the animation is about to end
        :return:
        """
        return\
            self.frame_timer.remaining <= self.frame_length\
            and\
            self.current_animation_frame_index + 1 >= len(self.current_animation_frames)

    def __init__(
            self,
            animations: AnimationStateDict = None,
            alt_table: List[AnimationStateDict] = None,
            default_animation: str = STILL_RIGHT,
            current_animation_name: str = None,
            frame_length: float = 1 / 48
    ):
        """

        Build a stateful animated sprite.

        :param animations: a dict mapping strings to lists of frames
        :param alt_table: a list of animation dicts to choose from
        :param default_animation: which animation will be displayed first
        :param current_animation_name: the name of the current animation
        :param frame_length: how long frames should be displayed for
        """
        super().__init__()

        self.animations: AnimationStateDict = {}

        if animations:
            self.animations = animations
        elif alt_table:
            self.animations = choice(alt_table)
        else:
            raise ValueError(
                "One of the following must be passed:"\
                " an animation atlas or alt table of atlases"
            )

        self.frame_timer = CountdownTimer()

        self.frame_length: float = frame_length
        self.current_animation_frame_index = 0
        self.default_animation: str = default_animation

        self._current_animation_name = None
        self.current_animation_name: str =\
            current_animation_name or default_animation

    def update_animation(self, delta_time: float = 1/60):
        """
        Advance or start the current animation by setting the frame.

        Override of a noop method on base sprite, called by the framework.

        Can be called indirectly when setting animations.

        :param delta_time:
        :return:
        """


        frame_timer: CountdownTimer = self.frame_timer

        frame_timer.update(delta_time)

        # allows this function to set the animation frame on instantiation
        next_frame_index = self.current_animation_frame_index

        # update the current animation frame if the timer has run out
        if frame_timer.remaining == 0.0:

            # only update frames if there's more than one frame
            if len(self.current_animation_frames) > 1:
                next_frame_index += 1
                if next_frame_index >= len(self.current_animation_frames):
                    next_frame_index = 0

                self.current_animation_frame_index = next_frame_index

            self.frame_timer.remaining = self.frame_length

        # otherwise set the current texture
        self.texture = self.current_animation_frames[next_frame_index]


class Actor(NamedAnimationsSprite):
    """
    Baseclass for mobile or otherwise active entities

    """

    @property
    def moving(self) -> bool:
        return self._moving

    def __init__(
            self,
            animations: AnimationStateDict = None,
            alt_table: List[AnimationStateDict] = None,
            default_animation: str = STILL_RIGHT,
            current_animation_name: str = None,
            frame_length: float = 1 / 12,
            stillness_threshold: float = 0.5
    ):
        """

        :param animations: a dict mapping strings to lists of frames
        :param alt_table: a list of animation dicts to choose from
        :param default_animation: which animation will be displayed first
        :param current_animation_name: the name of the current animation
        :param frame_length: how long frames should be displayed for
         """
        # used for movement detection
        self._moving = True

        # may be used in the future to hold sensors, non-drawn collision hulls used
        # for hitscanning and proximity detection?
        self.sensors_by_name = {}
        self.sensor_list = SpriteList()

        super().__init__(
            animations=animations,
            alt_table=alt_table,
            default_animation=default_animation,
            current_animation_name=current_animation_name,
            frame_length=frame_length
        )

    def update(self):
        super(Actor, self).update()

        if abs(self.change_x) > 0.1 and not self.moving:
            self._moving = True

        elif abs(self.change_x) <= 0.1 and self.moving:
            self._moving = False


