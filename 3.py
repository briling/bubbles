#!/usr/bin/env python3

import math




class Bubble_World:
    def __init__(self):
        self.bubble = {}
    def def_bubble(self, key, fill=0xFFFFFF, r=50, stroke=0x990000, stroke_w=10):
        self.bubble[key] = {'fill'    :fill,
                            'r'       :r,
                            'stroke'  :stroke,
                            'stroke_w':stroke_w}

    def print_head(self, xcanv, ycanv):
      print('<svg xmlns="http://www.w3.org/2000/svg" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'width="%d" height="%d">' % (xcanv, ycanv))
    def print_tail(self):
      print("</svg>");

    def print_def(self, grad_offset=30.0):
      print('  <defs>');
      self.print_def_bubble()
      print()
      self.print_def_gradient(grad_offset)
      print()
      self.print_def_font()
      print('  </defs>');
      print()

    def print_def_bubble(self):
      for key in self.bubble.keys():
        bub = self.bubble[key]
        print('    <g id="bubble'+str(key)+'"> '
              '<circle cx="0" cy="0" r="%lf" '
              'fill="#%06x" stroke="#%06x" stroke-width="%lf"/>'
              '</g>' % (bub['r'], bub['fill'], bub['stroke'], bub['stroke_w']))

    def print_def_gradient(self, offset=30.0):
      for i in self.bubble.keys():
          for j in self.bubble.keys():
              bubi = self.bubble[i]
              bubj = self.bubble[j]
              print('    <linearGradient id="myGradient%d.%d" gradientTransform="rotate(90)">\
        <stop offset="%d%%" stop-color="#%06x" />\
        <stop offset="%d%%" stop-color="#%06x" />\
        </linearGradient>'%(i, j, offset, bubi['stroke'], 100-offset, bubj['stroke']))

    def print_def_font(self):
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


    def put_bubble(self, t, x, y):
      print(f'  <use x="{x}" y="{y}" xlink:href="#bubble{str(t)}" />');


    def put_liaison(self, t0, x0, y0, t1, x1, y1_, alpha=None, h=None):

        r0 = self.bubble[t0]['r']+self.bubble[t0]['stroke_w']/2
        r1 = self.bubble[t1]['r']+self.bubble[t1]['stroke_w']/2

        if r0 < r1:
           self.put_liaison(t1, x1, y1_, t0, x0, y0, alpha, h)
           return

        angle = math.pi/2 - math.atan2(y1_-y0,x1-x0)
        l = math.sqrt( (x0-x1)**2 + (y0-y1_)**2)
        x = x0
        y1 = y0+l

        if abs(r0-r1)>1e-4:
            self.put_liaison_diffr(x,y0,y1,t0,t1,alpha,angle)
        else:
            self.put_liaison_equal(x,y0,y1,t0,t1,h, angle)

    def put_liaison_equal(self, x,y0,y1,t0,t1,h,angle):

      r0 = self.bubble[t0]['r']+self.bubble[t0]['stroke_w']/2
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


    def put_liaison_diffr(self, x,y0,y1,t0,t1,alpha,angle):
      def cross2lines(x_1, y_1, x_2, y_2, x_3, y_3, x_4, y_4):
          x = ((x_1*y_2-y_1* x_2)*(x_3-x_4)-(x_1-x_2)*(x_3 *y_4-y_3* x_4)) / ((x_1-x_2)*(y_3-y_4)-(y_1-y_2)*(x_3-x_4))
          y = ((x_1*y_2-y_1* x_2)*(y_3-y_4)-(y_1-y_2)*(x_3 *y_4-y_3* x_4)) / ((x_1-x_2)*(y_3-y_4)-(y_1-y_2)*(x_3-x_4))
          return x,y
      r0 = self.bubble[t0]['r']+self.bubble[t0]['stroke_w']/2
      r1 = self.bubble[t1]['r']+self.bubble[t1]['stroke_w']/2
      l = abs(y1-y0)
      # круги разного размера
      # малый круг снизу
      EO1 = r1*l / (r0-r1)
      EO0 = EO1+l
      Cx = x
      Cy = y1+EO1
      cosb = r1/EO1
      if alpha is None:
          alpha = 0.666*math.acos(cosb)
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
          <g transform="rotate({-angle/math.pi*180},{x},{y0})">\n\
            <path d=" \n\
            M {Cx+X12*cosa} {Cy+X12*sina} \n\
            A {R},  {R}  0 0 0 {Cx+X21*cosa} {Cy+X21*sina}  \n\
            h {-2*X21*cosa} \n\
            A {R},  {R}  0 0 0 {Cx-X12*cosa} {Cy+X12*sina}  \n\
            z" \n\
            fill="url(\'#myGradient{t0}.{t1}\')" \n\
            />\n\
          </g>')

    def put_text(self, x,y, text, fs=12, fc=0x000000):
      print(f'  <text x="{x}" y="{y}" class="mytext" font-size="{fs}px" fill="#{fc:06x}">')
      l = (len(text)-1)/2
      print(f'    <tspan x="{x}" dy="-{l}em">', text[0], '</tspan>')
      for line in text[1:]:
        print(f'    <tspan x="{x}" dy="1em">', line, '</tspan>')
      print('  </text>')




################################################################

xcanv = 500
ycanv = 500

bubble_world = Bubble_World()

bubble_world.def_bubble(0, fill=0xFFAAFF, r=25, stroke=0x990000, stroke_w=10)
bubble_world.def_bubble(1, fill=0xAAFFFF, r=25, stroke=0x000099, stroke_w=10)
bubble_world.def_bubble(2, fill=0xFFAAFF, r=25, stroke=0x990099, stroke_w=5)


bubble_world.print_head(xcanv, ycanv)
bubble_world.print_def()




b0 = (0 , 50, 100)
b1 = (2 , 50, 200)
bubble_world.put_liaison(*b0, *b1)
bubble_world.put_bubble(*b0)
bubble_world.put_bubble(*b1)

b0 = ( 0   , 250  , 250  )
b1 = ( 2   , 150, 250)
bubble_world.put_liaison(*b1, *b0)
bubble_world.put_bubble(*b0)
bubble_world.put_bubble(*b1)

b0 = (0   , 400 , 250 )
b1 = (2   , 400  , 150  )
bubble_world.put_liaison(*b0, *b1)
bubble_world.put_bubble(*b0)
bubble_world.put_bubble(*b1)

b0 = (2   , 300 , 200 )
b1 = (0   , 200  , 150  )
bubble_world.put_liaison(*b0, *b1)
bubble_world.put_bubble(*b0)
bubble_world.put_bubble(*b1)




b0 = (0 , 50, 300)
b1 = (1 , 50, 400)
bubble_world.put_liaison(*b0, *b1)
bubble_world.put_bubble(*b0)
bubble_world.put_bubble(*b1)

b0 = ( 0   , 250  , 450  )
b1 = ( 1   , 150, 450)
bubble_world.put_liaison(*b1, *b0)
bubble_world.put_bubble(*b0)
bubble_world.put_bubble(*b1)

b0 = (0   , 400 , 450 )
b1 = (1   , 400  , 350  )
bubble_world.put_liaison(*b0, *b1)
bubble_world.put_bubble(*b0)
bubble_world.put_bubble(*b1)

b0 = (1   , 300 , 400 )
b1 = (0   , 200  , 350  )
bubble_world.put_liaison(*b0, *b1)
bubble_world.put_bubble(*b0)
bubble_world.put_bubble(*b1)












bubble_world.print_tail()
