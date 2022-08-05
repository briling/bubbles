#!/usr/bin/env python3

import bubbles

xcanv = 1000
ycanv = 600

rouge = 0xFF0000
groseille = 0xB51F1F
canard = 0x007480
leman = 0x00A79F

bubble_world = bubbles.Bubble_World(xcanv, ycanv)

bubble_world.def_bubble(0, fill=0xFFFFFF, r=70, stroke=rouge,     stroke_w=15)
bubble_world.def_bubble(1, fill=0xFFFFFF, r=70, stroke=groseille, stroke_w=15)
bubble_world.def_bubble(2, fill=0xFFFFFF, r=70, stroke=canard,    stroke_w=15)
bubble_world.def_bubble(3, fill=0xFFFFFF, r=40, stroke=canard,    stroke_w=10)
bubble_world.def_bubble(4, fill=0xFFFFFF, r=70, stroke=leman,     stroke_w=15)
bubble_world.def_bubble(5, fill=0xFFFFFF, r=30, stroke=leman,     stroke_w=12)
bubble_world.def_bubble(6, fill=0xFFFFFF, r=40, stroke=canard,     stroke_w=10)
bubble_world.def_bubble(666, fill=0xFFFFFF, r=40, stroke=leman,     stroke_w=10)


x0 = 250
y0 = 250

x1 = x0-130
y1 = y0-130

x11 = x0+130
y11 = y0+130

x3 = x11 + 200
y3 = y11
y32 = y3 + 100
y33 = y3 - 100
x32 = x3 - 120
x33 = x3 - 120

y42 = y3 + 50
y43 = y3 - 50
x42 = x3 + 150
x43 = x3 + 150

y52 = y42 + 50
y53 = y42 - 50
x52 = x42 + 100
x53 = x42 + 100



bubble_world.add_bubble((0, x0, y0))
bubble_world.add_bubble((1, x1, y1))
bubble_world.add_bubble((2, x11, y11))
bubble_world.add_bubble((1, x11, y1))
bubble_world.add_bubble((1, x1, y11))

bubble_world.add_bubble((4, x3, y3))
bubble_world.add_bubble((3, x32, y32))
bubble_world.add_bubble((3, x33, y33))

bubble_world.add_bubble((5, x42, y42))
bubble_world.add_bubble((5, x43, y43))

bubble_world.add_bubble((6, x52, y52))
bubble_world.add_bubble((6, x53, y53))


bubble_world.add_liaison((0,x0,y0),(1,x1,y1))
bubble_world.add_liaison((0,x0,y0),(1,x1,y1))
bubble_world.add_liaison((0,x0,y0),(1,x11,y1))
bubble_world.add_liaison((0,x0,y0),(1,x1,y11))
bubble_world.add_liaison((0,x0,y0),(2,x11,y11))

bubble_world.add_liaison((2,x11,y11),(4,x3,y3))
bubble_world.add_liaison((2,x11,y11),(3,x32,y32),h=62)
bubble_world.add_liaison((2,x11,y11),(3,x33,y33),h=62)

bubble_world.add_liaison((4,x3,y3),(5,x42,y42), h=13.5)
bubble_world.add_liaison((4,x3,y3),(5,x43,y43), h=13.5)

bubble_world.add_liaison((5,x42,y42),(6,x52,y52), h=10.5)
bubble_world.add_liaison((5,x42,y42),(6,x53,y53), h=10.5)


bubble_world.add_text(x0, y0,  ['QML', 'representations'], fs=14, fc=0x000000)
bubble_world.add_text(x1, y1,  ['model', 'potentials'], fs=22, fc=0x000000)
bubble_world.add_text(x1, y11, ['internal', 'coordinates'], fs=22, fc=0x000000)
bubble_world.add_text(x11,y1,  ['density', 'of neighbors'], fs=22, fc=0x000000)
bubble_world.add_text(x11,y11, ['electronic', 'structure'], fs=22, fc=0x000000)
bubble_world.add_text(x3, y3,  ['SPAHM'], fs=25, fc=0x000000)

bubble_world.dump()

