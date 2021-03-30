from typing import DefaultDict, List, Dict
from collections import defaultdict
from arcade import Texture
from arcade import Sprite
from CatBurglar.util import Timer


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

    @property
    def current_animation_name(self):
        return self._current_animation_name

    @current_animation_name.setter
    def current_animation_name(self, new_animation_name: str) -> str:
        self._current_animation_name = new_animation_name
        self.current_animation_frame_index = 0
        self.frame_timer.remaining = self.frame_length
        self.current_animation_frames = self.animations[new_animation_name]
        self.update_animation(0.0)

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
            animations: Dict[str, List[Texture]] = None,
            default_animation: str = "default_right",
            current_animation_name: str = None,
            frame_length: float = 1 / 12
    ):
        """

        Build a stateful animated sprite.

        :param animations: a dict mapping strings to lists of frames
        :param default_animation: which animation will be displayed first
        :param current_animation_name: the name of the current animation
        :param frame_length: how long frames should be displayed for
        """
        super().__init__()

        self.animations: DefaultDict[str, List[Texture]] = defaultdict(list)

        if animations:
            self.animations.update(animations)

        self.frame_timer = Timer()

        self.frame_length: float = frame_length
        self.default_animation: str = default_animation
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


        frame_timer: Timer = self.frame_timer

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

