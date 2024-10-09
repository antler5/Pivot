# SPDX-FileCopyrightText: 2024 antlers <antlers@illucid.net>
# SPDX-License-Identifier: GPL-3.0-only

# %% Imports
import copy
import math
from build123d import *
from ocp_vscode import *

# %% Variables
reset_show()

front_width = 15.35
front_height = 15.5
front_angle = -18
front_thickness = 1.65
front_trap_angle = 82.55

base_depth = 15.5
base_thickness = 1
base_trap_angle = 72

front_excess = 1.65
base_excess = 1.25
support_thickness = 1.65

# Helpers
align_y_min = (Align.CENTER,Align.MIN)

# == Functions
def on_front_plane(obj):
  return Rot(front_angle) * (Plane.XZ * obj)

def split_by_face(obj, face, thickness):
  return obj - extrude(
      Plane(face.faces().first)
      * Rectangle(40,40),
      thickness)

# == Faces

# Base
base_face = Trapezoid(
  front_width,
  base_depth,
  base_trap_angle,
  align=align_y_min)
support_base_face = Trapezoid(
  front_width*2,
  base_depth - base_excess,
  base_trap_angle,
  align=align_y_min)

# Front
front_face_axis = on_front_plane(Circle(1)).location.to_axis() # arbitrary unit circle
front_face = on_front_plane(Trapezoid(
  front_width,
  front_height,
  front_trap_angle,
  align=align_y_min))

# Support
support_front_face = on_front_plane(Trapezoid(
  front_width*2,
  front_height - front_excess,
  front_trap_angle,
  align=align_y_min))
support_base_edge = Pos(0,0,base_thickness/2) * support_base_face.edges()[2]
support_front_edge = support_front_face.edges()[2]

support_face = make_face([
  support_base_edge,
  support_front_edge,
  Line(support_base_edge @ 0,
       support_front_edge @ 0),
  Line(support_base_edge @ 1,
       support_front_edge @ 1),
])

# Side(s)
side1 = make_face([
  base_face.edges()[1],
  front_face.edges()[1],
  Line(base_face.vertices()[2],
       front_face.vertices()[2])
])

# == Solids
bracket = []

# Base
base = extrude(base_face, base_thickness)
base = fillet(base.edges().group_by(Axis.Z)[-1], 0.5)
base = split_by_face(base, front_face, front_thickness)
bracket += [base]

# Front
front_face_2 = chamfer(front_face.vertices().group_by(Axis.Z)[-1], 2.5)
front = extrude(front_face_2, -front_thickness).split(Plane.XY)
front = split_by_face(front, side1, front_thickness)
front = split_by_face(front, side1.mirror(Plane.YZ), front_thickness)
front = fillet(front.edges().group_by(front_face_axis)[0], 0.5)
bracket += [front]

# Support
support = extrude(support_face, -support_thickness)
support = split_by_face(support, front_face, front_thickness)
support = split_by_face(support, base_face, -base_thickness)
support = split_by_face(support, side1, front_width)
support = split_by_face(support, side1.mirror(Plane.YZ), front_width)
support = fillet(support.edges(), 0.5)
bracket += [support]

# Slot
slot = (
  Rot(0,0,90)
  * Pos(base_depth/2.5,0,0)
  * chamfer(Rectangle(5.5,3.6).vertices(), 0.5))
slot = extrude(slot, 1)

# Support Ext. (Underhangs)
def support_ext(face, target, i, j, k):
  support_ext = Line(
    face.edges().group_by(Axis.Y)[i][0].center(),
    (0,0,-k) + slot.faces().group_by(Axis.Y)[i][0].center()
  )
  support_ext = make_face([
    Pos(-1,0,0) * support_ext,
    Pos(1,0,0) * support_ext,
    Line((Pos(-1,0,0) * support_ext) @ 0,
         (Pos(1,0,0) * support_ext) @ 0),
    Line((Pos(-1,0,0) * support_ext) @ 1,
         (Pos(1,0,0) * support_ext) @ 1),
  ])
  support_ext = fillet(support_ext.vertices().group_by(Axis.Y)[j], 0.5)
  support_ext = extrude(
    support_ext,
    target=target,
    until=Until.NEXT
  )
  return support_ext

support_ext_1 = support_ext(support_face, support,-1,0,0)
bracket += [support_ext_1]

support_ext_2 = support_ext(front_face, front,0,-1,base_thickness/2)
bracket += [support_ext_2]

# Switch Stem Holes
offset = front_height - 4.5
big_hole_r = 1 / 2 # radius
small_hole_r = 0.75 / 2
big_hole_d = 0.5 # depth
small_hole_d = 0.4
dist = 2.85

big_hole = on_front_plane(Pos(0,offset,0) * Hole(big_hole_r, big_hole_d))
small_hole = on_front_plane(
  Pos(0,
      offset - dist
             - big_hole_r
             - small_hole_r,
      0)
  * Hole(small_hole_r, small_hole_d))

bracket = Part() + bracket - (slot + big_hole + small_hole)
show_object(bracket)

# %% Export
export_step(bracket, "../STEPs/bracket.step")
export_stl(bracket, "../STLs/bracket.stl")