"""

Common base files for Actors, a category including the player and NPCs.

*All* mobile actors are expected to have entries for these in the state maps
for their class. Attempting to instantiate, and maybe even run the definition
of, a mobile actor that doesn't have these in the state map should return an
error.

"""

# Default non-moving states for actors
STILL_RIGHT = "default_right"
STILL_LEFT = "default_left"


WALK_RIGHT = "walk_right"
WALK_LEFT = "walk_left"





