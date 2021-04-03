import random
from arcade import SpriteList, lerp

from CatBurglar.entity.cop import BasicRunnerCop, Drone
from CatBurglar.entity.terrain import TILE_SIZE_PX, WIDTH_IN_TILES, HEIGHT_IN_TILES
from CatBurglar.util import StopwatchTimer, CountdownTimer


class EnemySpawner:
    def __init__(
            self,
            enemy_list: SpriteList,
            global_time_elapsed: StopwatchTimer,
            min_enemy_gap_sec=1.0,
            max_enemy_gap_sec=2.0,
            # 5 minutes till escape density reached
    ):
        self.enemy_list = enemy_list

        self.drone_list = SpriteList(use_spatial_hash=False)
        self.cop_list = SpriteList(use_spatial_hash=False)

        self.last_enemy = None

        # State timers used to determine time till next enemy
        self.global_time_elapsed = global_time_elapsed
        self.time_since_last_enemy = StopwatchTimer()

        self.min_enemy_gap_sec = min_enemy_gap_sec
        self.max_enemy_gap_sec = max_enemy_gap_sec

        # give some breathing room before the enemies start coming
        self.time_till_next = CountdownTimer(remaining=5.0)

    def update(self, delta_time: float = 1 / 60):

        self.time_till_next.update(delta_time)

        if self.time_till_next.remaining <= 0:
            enemy_list = self.enemy_list

            new_enemy = None
            y_position = None
            x_position = (WIDTH_IN_TILES + 1) * TILE_SIZE_PX

            if random.random() > 0.5:
                new_enemy = BasicRunnerCop()
                y_position = TILE_SIZE_PX * 2

            else:
                new_enemy = Drone()
                y_position = random.uniform(TILE_SIZE_PX * 1.5, TILE_SIZE_PX * HEIGHT_IN_TILES)

            new_enemy.set_position(x_position, y_position)

            enemy_list.append(new_enemy)
            self.time_till_next.remaining = random.uniform(
                self.min_enemy_gap_sec,
                lerp(
                    self.max_enemy_gap_sec,
                    self.min_enemy_gap_sec,
                    self.global_time_elapsed.completion
                )
            )

