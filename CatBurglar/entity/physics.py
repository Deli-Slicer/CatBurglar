from CatBurglar.entity.Player import MoveState, Player
from CatBurglar.input.KeyHandler import KeyHandler


class RunnerPhysicsEngine:
    """

    A physics implementation for runner games with jump canceling.

    Jump cancelling refers to stopping jumping after the jump button is
    pressed. Super Mario Bros is a good example of this style of jump.

    """

    def __init__(
        self,
        player_sprite: Player,
        key_handler: KeyHandler,
        ground_level: int = 16,
        gravity_constant: float = 0.3,
        initial_jump_velocity: float = 5
    ):
        """

        Set initial parameters for physics.

        Units for math and arguments are in unscaled pixels.

        :param player_sprite: the player sprite that will be managed
        :param key_handler: key handler that proxies keys to actions
        :param ground_level: how many pixels up from 0 the ground is
        :param gravity_constant: gravity in px / frame ^ 2
        :param initial_jump_velocity: initial jump velocity in px / frame
        """
        self.player: Player = player_sprite
        self.ground_level: int = ground_level
        self.gravity_constant: float = gravity_constant

        self.initial_jump_velocity = initial_jump_velocity
        self.key_handler: KeyHandler = key_handler

    def update(self, delta_time: float = 1 / 60):
        """

        Update the state based on key and current player state

        :param delta_time:
        :return:
        """

        # start a jump if on the ground
        if self.player.running and self.key_handler.is_pressed("JUMP"):
            self.player.move_state = MoveState.JUMPING
            self.player.change_y = self.initial_jump_velocity

        elif self.player.jumping:
            # continue jumping
            if self.key_handler.is_pressed("JUMP"):
                # continue jumping
                pass

            # stop jumping because the user cancelled it
            else:
                self.player.move_state = MoveState.FALLING
                self.player.change_y = 0

        # if the player is above ground, apply gravity
        if self.player.bottom > self.ground_level:
            self.player.change_y -= self.gravity_constant

            # update coarse movement state if needed
            if self.player.jumping and self.player.change_y < 0:
                self.player.move_state = MoveState.FALLING

        # stop jumping if we've hit the ground or tunneled below it
        if self.player.bottom < self.ground_level:
            self.player.bottom = self.ground_level
            self.player.change_y = 0
            self.player.move_state = MoveState.RUNNING

        self.player.update()

