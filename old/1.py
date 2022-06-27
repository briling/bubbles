#!/usr/bin/env python3

import math

def print_head():
  print('<svg xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        'width="%d" height="%d">' % (xcanv, ycanv))

def print_tail():
  print("</svg>\n");

def print_def_bubble(bubble):
  for i,bub in enumerate(bubble):
    print('    <g id="bubble%d"> '
          '<circle cx="0" cy="0" r="%lf" '
          'fill="#%06x" stroke="#%06x" stroke-width="%lf"/>'
          '</g>' % (i, bub['w'], bub['fill'], bub['stroke'], bub['stroke_w']))

def print_def_gradient(bubble, offset=30.0):
  for i,bubi in enumerate(bubble):
    for j,bubj in enumerate(bubble):
      pass
      print('    <linearGradient id="myGradient%d.%d" gradientTransform="rotate(90)">\
<stop offset="%d%%" stop-color="#%06x" />\
<stop offset="%d%%" stop-color="#%06x" />\
</linearGradient>'%(i, j, offset, bubi['stroke'], 100-offset, bubj['stroke']))

def print_def_liason(h=99.132464, rx=89.024213, ry=80.282081, dx=24.076051, dy=54.905692):
  print(f'\
    <g id="liason0" transform="translate(0,0)">\n\
      <path d="m {-h/2},{-dy} \n\
      a {rx}, {ry} 0  0  1  {dx},  {dy} {rx}, {ry} 0  0  1 -{dx},  {dy} h {h}\n\
      a {rx}, {ry} 0  0  1 -{dx}, -{dy} {rx}, {ry} 0  0  1  {dx}, -{dy} z" />\n\
    </g>')

def print_def_font():
  print('''    <style>\n\
      .mytext {\n\
        font-style:normal; font-variant:normal; font-weight:bold; font-stretch:normal;\n\
        line-height:125%;\n\
        font-family:"Adobe Helvetica"; -inkscape-font-specification:"Adobe Helvetica, Normal";\n\
        font-variant-ligatures:normal; font-variant-caps:normal; font-variant-numeric:normal; font-feature-settings:normal;\n\
        text-align:start; letter-spacing:0px; word-spacing:0px; writing-mode:lr-tb; text-anchor:middle;\n\
        fill-opacity:1; stroke:#FFFFFF;\n\
        stroke-width:0; stroke-linecap:butt; stroke-linejoin:miter; stroke-opacity:1;\n\
        stroke-miterlimit:4; stroke-dasharray:none\n\
      }\n\
    </style>\n\n''' )

def put_liason(t0,x0,y0,t1,x1,y1):

  r0 = bubble[t0]['w']+bubble[t0]['stroke_w']*0.5
  r1 = bubble[t1]['w']+bubble[t1]['stroke_w']*0.5
  r0_ = bubble[t0]['w']+bubble[t0]['stroke_w']
  r1_ = bubble[t1]['w']+bubble[t1]['stroke_w']
  dx = x1-x0
  dy = y1-y0
  x = (x0+x1)*0.5
  y = (y0+y1)*0.5
  l = math.hypot(dx,dy)
  angle = -math.acos(dy/l) * math.copysign( 180.0/math.pi, dx )
  x0_ = x0-r0_*math.sin(angle*math.pi/180.0)
  y0_ = y0+r0_*math.cos(angle*math.pi/180.0)
  x1_ = x1+r1_*math.sin(angle*math.pi/180.0)
  y1_ = y1-r1_*math.cos(angle*math.pi/180.0)
  x = (x0_+x1_)*0.5
  y = (y0_+y1_)*0.5
  hscale = pow((min(r0, r1)/80.0), 0.6)
  vscale = pow(((l-r0-r1)/(235.0-160)), 0.65)
  print('  <use x="0" y="0" xlink:href="#liason0" \
fill="url(\'#myGradient%d.%d\')" \
transform="translate(%f,%f) rotate(%f) scale(%f,%f) "  />'%((t0,t1, x,y, angle, hscale, vscale )))
  #print(f'<circle cx="{x}" cy="{y}" r="2" stroke="black" stroke-width="3" fill="red" />')
  #print(f'<circle cx="{x0_}" cy="{y0_}" r="2" stroke="black" stroke-width="3" fill="red" />')
  #print(f'<circle cx="{x1_}" cy="{y1_}" r="2" stroke="black" stroke-width="3" fill="red" />')

def put_bubble(t0, x0, y0):
  print('  <use x="%lf" y="%lf" xlink:href="#bubble%d" />'%( x0, y0, t0));

def put_text(x,y, text, fs=12, fc=0x000000):
  print(f'  <text x="{x}" y="{y}" class="mytext" font-size="{fs}px" fill="#{fc:06x}">')
  l = (len(text)-1)/2
  print(f'    <tspan x="{x}" dy="-{l}em">', text[0], '</tspan>')
  for line in text[1:]:
    print(f'    <tspan x="{x}" dy="1em">', line, '</tspan>')
  print('  </text>')

def print_def():
  print('  <defs>');
  print_def_bubble(bubble)
  print()
  print_def_gradient(bubble)
  print()
  print_def_liason()
  print()
  print_def_font()
  print('  </defs>');
  print()

################################################################

xcanv = 500
ycanv = 500

bubble = []
bubble.append({'fill':0xFFAAFF,
               'w':   70,
               'stroke':0x990000,
               'stroke_w':20})
bubble.append({'fill':0xAAFFFF,
               'w':   70,
               'stroke':0x000099,
               'stroke_w':20})
bubble.append({'fill':0xFFAAFF,
               'w':   20,
               'stroke':0x990099,
               'stroke_w':5})

print_head()
print_def()

x0 = 250
y0 = 300
t0 = 0
t1 = 1
x1 = 150
y1 = 80
t2 = 2
x2 = 350
y2 = 20
x3 = 370
y3 = 400
put_bubble(t0, x0, y0)
put_bubble(t1, x1, y1)
put_liason(t0,x0,y0,t1,x1,y1)

put_liason(t0,x0,y0,t2,x3,y3)

put_text(x1,y1, ['My very very', 'very very very', 'very long text'], fs=14, fc=0xff00ff)


put_bubble(t2, x3, y3)

print_tail()
