# 4gewinnt

This is a four-in-a-row bot for [the ai games competition](http://theaigames.com/competitions/four-in-a-row#).
Our stuff is a bit scattered around. You can find the (almost perfect) heuristic in the branch lk_heuristic. A cleand-up and commented version in the tag v26b. And a readme in the master. Sorry about that.

Techniques we used for the bot:
  * minmax search tree
  * alpha-beta pruning (search tree optimization)
  * iterative search depth (the tree is stored between play turns)
  * transposition table (eliminate duplicate board states)
  * zobrist hash function (iterative hash for performance)
  * child order sorting for an optimized alpha-beta pruning
  * time tracking to avoid a timeout during the competition§
