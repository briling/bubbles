#!/usr/bin/env python

# TODO:
# 4) width
# 5) behind the circles

from simplestyle import *
from simpletransform import *

import math
import inkex
from inkex.elements import Group, PathElement
import bubbles
from lxml import etree

class BubbleBond(inkex.Effect):

    def __init__(self):
        inkex.Effect.__init__(self)
        self.arg_parser.add_argument('-l', '--label', action='store',
                                     type=str, dest='label',
                                     default='thermometer',
                                     help='Shape Label?')
    def checkGradient(self, gid):
        try:
            retval = self.document.xpath('//svg:linearGradient[@id="%s"]' % gid, namespaces=inkex.NSS)[0]
        except:
            return False
        return True

    def addLinearGradient(self, colors, gid):
        defs = self.svg.getElement('/svg:svg//svg:defs')
        if defs is None:
            defs = etree.SubElement(self.document.getroot(),inkex.addNS('defs','svg'))
        gradient = etree.SubElement(defs,inkex.addNS('linearGradient','svg'))
        gradient.set('id', gid)
        for (off,color) in colors:
            lg_stop = etree.Element(inkex.addNS('stop','svg'))
            lg_stop.set('style', str(inkex.Style(color)))
            lg_stop.set('offset', '%f' % off)
            gradient.append(lg_stop)
        gradient.set('x1', '0')
        gradient.set('y1', '0')
        gradient.set('x2', '0')
        gradient.set('y2', '1')
        defs.append(gradient)

    def addPath(self, group, style, d, nodetypes=None, label=None):
        path = etree.Element(inkex.addNS('path','svg'))
        path.set('style', str(inkex.Style(style)))
        path.set('d', d)
        if not label==None:
            path.set(inkex.addNS('label','inkscape'),label)
        if not nodetypes==None:
            path.set(inkex.addNS('nodetypes', 'sodipodi'), nodetypes)
        group.append(path)



    def make_liaison(self, r0, r1, x0, x1, y0, y1, h, gradient):
        BW = bubbles.Bubble_World()
        angle, y11 = BW.liaison_angle(x0, x1, y0, y1)
        path       = BW.liaison_path(r0, r1, x0, y0, y11, None, h, True, 1e-4)
        my_shape = PathElement()
        my_shape.path = path
        style = {   'stroke'        : 'none',
                    'stroke-width'  : '0',
                    'fill'          : gradient,
                }
        my_shape.style = str(inkex.styles.Style(style))

        my_shape.transform.add_rotate(-angle, x0, y0)
        layer = self.svg.add(Group.new('my_label', is_layer=True))
        layer.append(my_shape)
        return

    def get_radius(self, c0, st0):
        if c0.tag_name=='circle':
            r0 = c0.radius
        elif c0.tag_name=='ellipse':
            if abs(c0.radius[0]-c0.radius[1])>1e-4:
                return None
            r0 = c0.radius[0]
        else:
            return None
        return r0 + float(st0['stroke-width'])/2

    def get_style_dict(self, c0):
        st0_str = c0.attrib['style']
        st0_obj = inkex.styles.Style.parse_str(st0_str)
        st0_dict = {}
        for key,val in st0_obj:
            st0_dict[key] = val
        return st0_dict

    def make_gradient(self, offset, str0, str1):
        c0 = (offset[0], { 'stop-color' : str0 , 'stop-opacity' : '1' })
        c1 = (offset[1], { 'stop-color' : str1 , 'stop-opacity' : '1' })
        gi = 0
        while True:
            gname = f'BubbleBondLinearGradient{gi}'
            if not self.checkGradient(gname):
                self.addLinearGradient((c0, c1), gname)
                break
            gi+=1
        return 'url(#'+gname+')'

    def effect(self):

        #inkex.utils.debug("yo")

        h = 10
        offset = [0.0,1.0]

        # check the number of selected objects
        idx = self.options.ids
        if len(idx) != 2:
            inkex.utils.debug('Select two circles!')
            return
        c0, c1 = self.svg.selected[idx[0]], self.svg.selected[idx[1]]
        st0 = self.get_style_dict(c0)
        st1 = self.get_style_dict(c1)

        # check their types and get the radii
        r0 = self.get_radius(c0, st0)
        r1 = self.get_radius(c1, st1)
        if r0 is None or r1 is None:
            inkex.utils.debug('Select two circles!')
            return

        x0 = float(c0.attrib['cx'])
        y0 = float(c0.attrib['cy'])
        x1 = float(c1.attrib['cx'])
        y1 = float(c1.attrib['cy'])

        grad = self.make_gradient(offset, st0['stroke'], st1['stroke'])
        self.make_liaison(r0, r1, x0, x1, y0, y1, h, grad)

        return

bb = BubbleBond()
bb.run()


        #svg = self.document.getroot()
        #parent = self.svg.get_current_layer()
        #self.addPath(svg, style,
        #             'm 439.7786,473.74954 20.24066,0 -0.0387,-267.40595 -20.28271,0 z',
        #             'ccccc',label=label)
