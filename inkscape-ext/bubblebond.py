#!/usr/bin/env python

from itertools import count
import inkex
from lxml import etree

try:
    import bubbles
except ImportError:
    # try and detect the bubbles.py file next to this one
    import sys, os
    sys.path.append(os.path.split(__file__)[0])
    import bubbles
    del sys.path[-1]
    del sys,os


class BubbleBond(inkex.Effect):

    def add_arguments(self, pars):
        pars.add_argument('--tab')
        pars.add_argument('--width',   type=int,           default=25,    dest='width')
        pars.add_argument('--offset1', type=int,           default=0,     dest='offset1')
        pars.add_argument('--offset2', type=int,           default=100,   dest='offset2')
        pars.add_argument('--back',    type=inkex.Boolean, default=False, dest='back')

    def effect(self):

        width   = 1e-2*self.options.width
        offsets = (1e-2*self.options.offset1, 1e-2*self.options.offset2)
        back    = self.options.back

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

        if 'stroke' in st0 and st0['stroke'] != 'none':
            col0 = st0['stroke']
        elif 'fill' in st0:
            col0 = st0['fill']
        else:
            col0 = 'none'
        if 'stroke' in st1 and st1['stroke'] != 'none':
            col1 = st1['stroke']
        elif 'fill' in st0:
            col1 = st1['fill']
        else:
            col1 = 'none'
        colors = (col0, col1)
        x0 = float(c0.attrib['cx'])
        y0 = float(c0.attrib['cy'])
        x1 = float(c1.attrib['cx'])
        y1 = float(c1.attrib['cy'])

        grad = self.make_gradient(colors, offsets)
        self.make_liaison(r0, r1, x0, x1, y0, y1, h, grad)

        if back is True:
            # don't understand why it works so thanks to extensions/restack.py
            parent = self.svg.get_current_layer()
            parent.append(c0)
            parent.append(c1)

        return

    def add_gradient(self, gname, colors, offsets):
        # thanks to https://github.com/r-forge/svgmapping/tree/master/inkscape/extensions
        gradient = etree.SubElement(self.svg.defs, inkex.addNS('linearGradient', 'svg'))
        gradient.set('id', gname)
        for (offset, color) in zip(offsets, colors):
            stop = etree.Element(inkex.addNS('stop', 'svg'))
            stop.set('style', str(inkex.Style({'stop-color': color, 'stop-opacity': '1'})))
            stop.set('offset', str(offset))
            gradient.append(stop)
        gradient.set('x1', '0')
        gradient.set('y1', '0')
        gradient.set('x2', '0')
        gradient.set('y2', '1')
        self.svg.defs.append(gradient)

    def make_gradient(self, colors, offsets):
        if self.svg.defs is None:
            etree.SubElement(self.document.getroot(), inkex.addNS('defs', 'svg'))
        defs = [i.get_id() for i in self.svg.defs.findall('*')]
        for gi in count(0):
            gname = f'BubbleBondLinearGradient{gi}'
            if gname not in defs:
                self.add_gradient(gname, colors, offsets)
                return 'url(#'+gname+')'

    def make_liaison(self, r0, r1, x0, x1, y0, y1, h, gradient):
        BW         = bubbles.Bubble_World()
        angle, y11 = BW.liaison_angle(x0, x1, y0, y1)
        path       = BW.liaison_path(r0, r1, x0, y0, y11, None, h, True, 1e-4)
        liaison       = inkex.elements.PathElement()
        liaison.path  = path
        liaison.style = str(inkex.styles.Style({'stroke': 'none', 'stroke-width': '0', 'fill': gradient}))
        liaison.transform.add_rotate(-angle, x0, y0)
        self.svg.get_current_layer().append(liaison)
        return

    def get_radius(self, c0, st0):
        if c0.tag_name == 'circle':
            r0 = c0.radius
        elif c0.tag_name == 'ellipse':
            if abs(c0.radius[0]-c0.radius[1]) > 1e-4:
                return None
            r0 = c0.radius[0]
        else:
            return None
        if 'stroke' in st0 and st0['stroke'] != 'none':
            return r0 + float(st0['stroke-width'])/2
        else:
            return r0

    def get_style_dict(self, c0):
        st0_str = c0.attrib['style']
        st0_obj = inkex.styles.Style.parse_str(st0_str)
        if hasattr(st0_obj, 'items'):
            st0_dict = { k:v for k,v in st0_obj.items() }
        else:
            # fallback that only works on old versions of inkscape (before which one?)
            st0_dict = { k:v for k,v in st0_obj }
        return st0_dict


bb = BubbleBond()
bb.run()
