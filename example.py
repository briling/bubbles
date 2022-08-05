#!/usr/bin/env python3

import bubbles

xcanv = 500
ycanv = 500

bubble_world = bubbles.Bubble_World()

bubble_world.def_bubble(0, fill=0xFFAAFF, r=25, stroke=0x990000, stroke_w=10)
bubble_world.def_bubble(1, fill=0xAAFFFF, r=25, stroke=0x000099, stroke_w=10)
bubble_world.def_bubble(2, fill=0xFFAAFF, r=25, stroke=0x990099, stroke_w=5)
bubble_world.print_head(xcanv, ycanv)
bubble_world.print_def(font_weight='bold')

b0 = (0 , 50, 100)
b1 = (2 , 50, 200)
bubble_world.put_liaison(b0, b1, auto=False)
bubble_world.put_bubble(b0)
bubble_world.put_bubble(b1)
bubble_world.put_text(*b0[1:], ['123', 'abc', ',./'])
bubble_world.put_text(*b1[1:], ['123', 'abc', ',./'], fs=8)

b0 = ( 0   , 250  , 250  )
b1 = ( 2   , 150, 250)
bubble_world.put_liaison(b1, b0, alpha=-1.3, auto=False)
bubble_world.put_bubble(b0)
bubble_world.put_bubble(b1)
bubble_world.put_text(*b0[1:], ['123'])
bubble_world.put_text(*b1[1:], ['123'], fs=6)

b0 = (0   , 400 , 250 )
b1 = (2   , 400  , 150  )
bubble_world.put_liaison(b0, b1, auto=False)
bubble_world.put_bubble(b0)
bubble_world.put_bubble(b1)

b0 = (2   , 300 , 200 )
b1 = (0   , 200  , 150  )
bubble_world.put_liaison(b0, b1, alpha=-0.8, auto=False)
bubble_world.put_bubble(b0)
bubble_world.put_bubble(b1)




b0 = (0 , 50, 300)
b1 = (1 , 50, 400)
bubble_world.put_liaison(b0, b1)
bubble_world.put_bubble(b0)
bubble_world.put_bubble(b1)

b0 = ( 0   , 250  , 450  )
b1 = ( 1   , 150, 450)
bubble_world.put_liaison(b1, b0, auto=False, alpha=0.1)
bubble_world.put_bubble(b0)
bubble_world.put_bubble(b1)

b0 = (0   , 400 , 450 )
b1 = (1   , 400  , 350  )
bubble_world.put_liaison(b0, b1, h=4)
bubble_world.put_bubble(b0)
bubble_world.put_bubble(b1)

b0 = (1   , 300 , 400 )
b1 = (0   , 200  , 350  )
bubble_world.put_liaison(b0, b1, h=32)
bubble_world.put_bubble(b0)
bubble_world.put_bubble(b1)

bubble_world.print_tail()
