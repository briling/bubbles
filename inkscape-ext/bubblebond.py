#!/usr/bin/env python

import math
import inkex
from inkex.elements import Group, PathElement
from lxml import etree
import bubbles

class BubbleBond(inkex.Effect):

    def add_arguments(self, pars):
        pars.add_argument('--tab')
        pars.add_argument('--width',   type=int,           default=25,    dest='width'  )
        pars.add_argument('--offset1', type=int,           default=0,     dest='offset1')
        pars.add_argument('--offset2', type=int,           default=100,   dest='offset2')
        pars.add_argument('--back',    type=inkex.Boolean, default=False, dest='back'   )

    # thanks to https://github.com/r-forge/svgmapping/tree/master/inkscape/extensions

    def check_gradient(self, name):
        try:
            self.document.xpath('//svg:linearGradient[@id="%s"]' % name, namespaces=inkex.NSS)[0]
        except:
            return False
        return True

    def add_gradient(self, colors, offsets, name):
        defs = self.svg.getElement('/svg:svg//svg:defs')
        if defs is None:
            defs = etree.SubElement(self.document.getroot(),inkex.addNS('defs','svg'))
        gradient = etree.SubElement(defs,inkex.addNS('linearGradient','svg'))
        gradient.set('id', name)
        for (offset, color) in zip(offsets, colors):
            stop = etree.Element(inkex.addNS('stop','svg'))
            stop.set('style', str(inkex.Style(color)))
            stop.set('offset', f'{offset}')
            gradient.append(stop)
        gradient.set('x1', '0')
        gradient.set('y1', '0')
        gradient.set('x2', '0')
        gradient.set('y2', '1')
        defs.append(gradient)

    def make_liaison(self, r0, r1, x0, x1, y0, y1, h, gradient):
        BW = bubbles.Bubble_World()
        angle, y11 = BW.liaison_angle(x0, x1, y0, y1)
        path       = BW.liaison_path(r0, r1, x0, y0, y11, None, h, True, 1e-4)
        liaison = PathElement()
        liaison.path  = path
        liaison.style = str(inkex.styles.Style({'stroke':'none', 'stroke-width':'0', 'fill':gradient}))
        liaison.transform.add_rotate(-angle, x0, y0)
        self.svg.get_current_layer().append(liaison)
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
        c0 = { 'stop-color' : str0 , 'stop-opacity' : '1' }
        c1 = { 'stop-color' : str1 , 'stop-opacity' : '1' }
        gi = 0
        while True:
            gname = f'BubbleBondLinearGradient{gi}'
            if not self.check_gradient(gname):
                self.add_gradient((c0, c1), offset, gname)
                break
            gi+=1
        return 'url(#'+gname+')'

    def effect(self):

        width  = 1e-2*self.options.width
        offset = [1e-2*self.options.offset1, 1e-2*self.options.offset2]
        back   = self.options.back

        # check the number of selected objects
        idx = self.options.ids
        if len(idx) != 2:
            raise inkex.AbortExtension("Select exactly 2 circles.")
        c0, c1 = self.svg.selected[idx[0]], self.svg.selected[idx[1]]
        st0 = self.get_style_dict(c0)
        st1 = self.get_style_dict(c1)

        # check their types and get the radii
        r0 = self.get_radius(c0, st0)
        r1 = self.get_radius(c1, st1)
        if r0 is None or r1 is None:
            raise inkex.AbortExtension("These are not circles.")
        h = width * 2.0*min(r0, r1)

        x0 = float(c0.attrib['cx'])
        y0 = float(c0.attrib['cy'])
        x1 = float(c1.attrib['cx'])
        y1 = float(c1.attrib['cy'])

        grad = self.make_gradient(offset, st0['stroke'], st1['stroke'])
        self.make_liaison(r0, r1, x0, x1, y0, y1, h, grad)

        if back is True:
            # don't understand why it works so thanks to extensions/restack.py
            parent = self.svg.get_current_layer()
            parent.append(c0)
            parent.append(c1)

        return

bb = BubbleBond()
bb.run()
