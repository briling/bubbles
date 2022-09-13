#!/usr/bin/env python

# TODO:
# 3) colors
# 4) width

import math
import inkex
from inkex.elements import Group, PathElement
import bubbles

class BubbleBond(inkex.Effect):

    def make_liaison(self, r0, r1, x0, x1, y0, y1, h):
        BW = bubbles.Bubble_World()
        angle, y11 = BW.liaison_angle(x0, x1, y0, y1)
        path       = BW.liaison_path(r0, r1, x0, y0, y11, None, h, True, 1e-4)
        my_shape = PathElement()
        my_shape.path = path
        my_shape.transform.add_rotate(-angle, x0, y0)
        layer = self.svg.add(Group.new('my_label', is_layer=True))
        layer.append(my_shape)
        return

    def get_radius(self, c0):
        if c0.tag_name=='circle':
            return float(c0.radius)
        elif c0.tag_name=='ellipse':
            if abs(c0.radius[0]-c0.radius[1])>1e-4:
                return None
            return float(c0.radius[0])
        else:
            return None

    def effect(self):

     #inkex.utils.debug("yo")

     # check the number of selected objects
     idx = self.options.ids
     if len(idx) != 2:
         inkex.utils.debug('Select two circles!')
         return
     c0, c1 = self.svg.selected[idx[0]], self.svg.selected[idx[1]]

     # check their types and get the radii
     r0 = self.get_radius(c0)
     r1 = self.get_radius(c1)
     if r0 is None or r1 is None:
         inkex.utils.debug('Select two circles!')
         return

     x0 = float(c0.attrib['cx'])
     y0 = float(c0.attrib['cy'])
     x1 = float(c1.attrib['cx'])
     y1 = float(c1.attrib['cy'])

     self.make_liaison(r0, r1, x0, x1, y0, y1, 10)

     return

bb = BubbleBond()
bb.run()
