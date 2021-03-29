"""

Common elements for Actors, a category including the player and NPCs.

*All* mobile actors are expected to have entries for these in the state maps
for their class. Attempting to instantiate, and maybe even run the definition
of, a mobile actor that doesn't have these in the state map should return an
error.

"""

# Default non-moving animation states for actors
STILL_RIGHT = "still_right"
STILL_LEFT = "still_left"
STILL_FACINGCAMERA = "still_facing"
STILL_AWAYCAMERA = "still_awaycamera"

# Animation state names that all motile actors are expected to have
WALK_RIGHT = "walk_right"
WALK_LEFT = "walk_left"





