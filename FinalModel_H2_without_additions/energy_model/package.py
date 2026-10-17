"""Which of the two packages this is. The study comes in two packages that do the same analysis:

* WITHOUT additions: the set-up of 14 October. A hydrogen demand (1.3 Mt/yr) served by SMR (grey), SMR + CCS (blue)
  and the grid electrolyser (green), with the water limit on electrolysers as the scenario, the cost variations and
  the green levers.
* WITH additions: the same, plus the three additions of the group (15 October) in EVERY run: hydrogen storage in salt
  caverns, the pure green route (the electrolyser's own offshore wind and solar) and pink hydrogen (its own nuclear
  plant). The model chooses whether to build them.

The water limit is the same in both packages: in MW of hydrogen output, from Base without additions (2,473 MW in
2050 for Medium). The water available does not change when technologies are added.

The published package keeps hydrogen storage as an optional addition. The
dedicated renewable and nuclear routes are not included here.
"""

ADDITIONS = False
STORAGE = True

SET_NAME = 'with additions' if ADDITIONS else 'without additions'
SET_LONG = ('with additions: H₂ storage, pure green and pink hydrogen in every run' if ADDITIONS
            else 'without additions: SMR, SMR + CCS, the grid electrolyser and optional H₂ storage')
