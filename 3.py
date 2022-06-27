#!/usr/bin/env python3

import math

def cross2lines(x_1, y_1, x_2, y_2, x_3, y_3, x_4, y_4):
  x = ((x_1*y_2-y_1* x_2)*(x_3-x_4)-(x_1-x_2)*(x_3 *y_4-y_3* x_4)) / ((x_1-x_2)*(y_3-y_4)-(y_1-y_2)*(x_3-x_4))
  y = ((x_1*y_2-y_1* x_2)*(y_3-y_4)-(y_1-y_2)*(x_3 *y_4-y_3* x_4)) / ((x_1-x_2)*(y_3-y_4)-(y_1-y_2)*(x_3-x_4))
  return x,y

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
  print_def_font()
  print('  </defs>');
  print()



def put_liaison_equal(x,y0,y1,t0,t1,h,angle,bubble):

  r0 = bubble[t0]['w']+bubble[t0]['stroke_w']/2
  if h is None:
      h = 0.666*r0

  l = abs(y1-y0)
  R = (0.25*l**2+0.25*h**2-r0**2) / (2*r0-h)

  dx = 0.5*h+R
  dy = (y1-y0)*0.5
  dr = math.sqrt(dx**2 + dy**2)

  xx = dx*r0 / dr
  yy = dy*r0 / dr

  print(f' <g transform="rotate({-angle/math.pi*180},{x},{y0})">\n\
    <path d=" \n\
    M {x+xx} {y0+yy} \n\
    A {R}, {R}  0 0 0 {x+xx} {y1-yy}  \n\
    h {-2*xx}\n\
    A {R}, {R}  0 0 0 {x-xx} {y0+yy}  \n\
    z"\n\
    fill="url(\'#myGradient{t0}.{t1}\')" \n\
    />\n\
  </g>')


def put_liaison_diffr(x,y0,y1,t0,t1,alpha,angle,bubble):
  r0 = bubble[t0]['w']+bubble[t0]['stroke_w']/2
  r1 = bubble[t1]['w']+bubble[t1]['stroke_w']/2
  l = abs(y1-y0)
  # круги разного размера
  # малый круг снизу
  EO1 = r1*l / (r0-r1)
  EO0 = EO1+l
  Cx = x
  Cy = y1+EO1
  cosb = r1/EO1
  if alpha is None:
      alpha = 0.95*math.acos(cosb)
  #print(math.asin(cosb)/math.pi*180) # угол между касательной и прямой соединяющей центры
  # больше него нельзя
  sina = math.sin((90-alpha)/180*math.pi) # угол между секущей и прямой соединяющей центры
  cosa = math.cos((90-alpha)/180*math.pi)
  # пересечение секущих с окружностями
  B = 2 * EO1 * sina
  C = EO1**2-r1**2
  D = B*B-4*C

  X11 = (-B +math.sqrt(D))*0.5
  X12 = (-B -math.sqrt(D))*0.5
  X21 = X11 * r0/r1
  px, py = cross2lines(x,y0,Cx+X21*cosa,Cy+X21*sina, x, y1, Cx+X12*cosa,  Cy+X12*sina) # центр касательной окружности
  R = math.sqrt((px-(Cx+X21*cosa))**2 + (py-(Cy+X21*sina))**2) # радиус касательной окружности
  print(f'\n\
      <g transform="rotate({-angle/math.pi*180},{x0},{y0})">\n\
        <path d=" \n\
        M {Cx+X12*cosa} {Cy+X12*sina} \n\
        A {R},  {R}  0 0 0 {Cx+X21*cosa} {Cy+X21*sina}  \n\
        h {-2*X21*cosa} \n\
        A {R},  {R}  0 0 0 {Cx-X12*cosa} {Cy+X12*sina}  \n\
        z" \n\
        fill="url(\'#myGradient{t0}.{t1}\')" \n\
        />\n\
      </g>')

def put_liaison(x0, y0, t0, x1, y1_, t1, bubble, alpha=None, h=None):

    r0 = bubble[t0]['w']+bubble[t0]['stroke_w']/2
    r1 = bubble[t1]['w']+bubble[t1]['stroke_w']/2

    if r0 < r1:
       put_liaison(x1, y1_, t1,x0, y0, t0,  bubble, alpha, h)
       return

    angle = math.pi/2 - math.atan2(y1_-y0,x1-x0)
    l = math.sqrt( (x0-x1)**2 + (y0-y1_)**2)
    x = x0
    y1 = y0+l

    if abs(r0-r1)>1e-4:
        put_liaison_diffr(x,y0,y1,t0,t1,alpha,angle,bubble)
    else:
        put_liaison_equal(x,y0,y1,t0,t1,h, angle,bubble)



class Bubble_World:
    def __init__(self):
        self.bubble = {}
    def def_bubble(self, key, fill=0xFFFFFF, r=50, stroke=0x990000, stroke_w=10):
        self.bubble[key] = {'fill'    :fill,
                            'w'       :r,
                            'stroke'  :stroke,
                            'stroke_w':stroke_w}





################################################################

xcanv = 500
ycanv = 500

bubble_world = Bubble_World()

bubble = []
bubble.append({'fill':0xFFAAFF,
               'w':   50,
               'stroke':0x990000,
               'stroke_w':20})
bubble.append({'fill':0xAAFFFF,
               'w':   70,
               'stroke':0x000099,
               'stroke_w':20})
bubble.append({'fill':0xFFAAFF,
               'w':   55,
               'stroke':0x990099,
               'stroke_w':10})

for i,b in enumerate(bubble):
    bubble_world.def_bubble(i,fill=b['fill'], r=b['w'], stroke=b['stroke'], stroke_w=b['stroke_w'])

print_head()









print_def()


t0 = 0
x0 = 50
y0 = 100

t1 = 2
x1 = 50
y1 = 300
put_liaison(x0, y0, t0, x1, y1, t1, bubble)
put_bubble(t0, x0, y0)
put_bubble(t1, x1, y1)


t0 = 0
x0 = 250
y0 = 250

t1 = 2
x1 = 100
y1 = 250
put_liaison(x0, y0, t0, x1, y1, t1, bubble)
put_bubble(t0, x0, y0)
put_bubble(t1, x1, y1)


t0 = 0
x0 = 400
y0 = 250

t1 = 2
x1 = 400
y1 = 100
put_liaison(x0, y0, t0, x1, y1, t1, bubble)
put_bubble(t0, x0, y0)
put_bubble(t1, x1, y1)


put_liaison(400, 400, t1,500, 100, t0, bubble)
put_bubble(t0, 500, 100)
put_bubble(t1, 400, 400)




print_tail()
