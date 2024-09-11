# SPDX-FileCopyrightText: 2024 antlers <antlers@illucid.net>

# SPDX-License-Identifier: GPL-3.0-only

# %% Imports %%
import math
from build123d import *
from ocp_vscode import *

# %% Joystick
switchStickWidth = 2
switchStickHeight = 2.05
baseWidth = 3.15
baseHeight = 1

stemLength = 11.5
stemRadius = 5.5 / 2
initialRadius = stemRadius -0.75
initialRadiusOffset = 1.25

headRadius = 13.5 / 2
headOffset = 3.75

_acc = 0
def acc(n):
  global _acc
  _acc += n
  return _acc

joystick = (
  Circle(initialRadius)
  + Pos(0,0,acc(initialRadiusOffset)) * Circle(stemRadius)
  + Pos(0,0,acc(stemLength)) * Circle(stemRadius)
  + Pos(0,0,acc(headOffset)) * Circle(headRadius)
)

joystick = loft(joystick, ruled=True)

joystickHead = (
  Pos(0,0,acc(0)) * Sphere(headRadius)
  .split(Plane.XY)
)

# Define two rectangular guides, one at the base of the hemisphere
# and one around where the top will be (solving for the intermediate radius)
bottomGuide = Pos(0,0,acc(0)) * Rectangle(headRadius*2, headRadius*2)
topGuideOffset = 5.75
topGuideWidth = 2 * math.sqrt(abs(topGuideOffset**2 - headRadius**2))
topGuide = Pos(0,0,acc(0) + topGuideOffset) * Rectangle(topGuideWidth, topGuideWidth)

# Gonna define a number of spheres for concave fingerpad cutouts
fingerpadRadius = 80 # big and far away
fingerpadOffset = fingerpadRadius - 0.25
fingerpads = []

# One for the top
fingerpads += Pos(0,0,fingerpadOffset - 0.75) * Pos(topGuide.center()) * Sphere(fingerpadRadius)

# One for each cardinal direction
for i in range(4):
  plane = Axis(Edge.make_line(
                 topGuide.edges()[i].center(),
                 bottomGuide.edges()[i].center()
               )
          ).to_plane()
  if i > 1:
    fingerpads += plane * Pos(-fingerpadOffset,0,0) * Sphere(fingerpadRadius)
  else:
    fingerpads += plane * Pos(fingerpadOffset,0,0) * Sphere(fingerpadRadius)

joystick += joystickHead - fingerpads

# 5-Way switch slot (stick + base)
joystick -= [
  Pos(0,0,(baseHeight) / 2) * Cylinder(baseWidth/2,baseHeight),
  Rot(0,0,45) * Pos(0,0,(switchStickHeight + baseHeight) / 2) * Box(switchStickWidth, switchStickWidth, switchStickHeight + baseHeight)
]

show(joystick)

# %%
export_step(joystick, "../STEPs/joystick.step")
export_stl(joystick, "../STLs/joystick.stl")
