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

    def print_def(self, grad_offset=30.0, font_family='LMsans', font_weight='normal'):
      print('  <defs>');
      self.print_def_bubble()
      print()
      self.print_def_gradient(offset=grad_offset)
      print()
      self.print_def_font(family=font_family,weight=font_weight)
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
              print('    <linearGradient id="myGradient%d.%d" x1="0" x2="0" y1="0" y2="1">\
        <stop offset="%d%%" stop-color="#%06x" />\
        <stop offset="%d%%" stop-color="#%06x" />\
        </linearGradient>'%(i, j, offset, bubi['stroke'], 100-offset, bubj['stroke']))

    def print_def_font(self, family='LMsans', weight='normal'):
      if family=='Helvetica':
        print(f'''    <style>
            .mytext {'{'}
              font-style:normal; font-variant:normal; font-weight:{weight}; font-stretch:normal;
              line-height:125%;
              font-family:"Adobe Helvetica"; -inkscape-font-specification:"Adobe Helvetica, Normal";
              font-variant-ligatures:normal; font-variant-caps:normal; font-variant-numeric:normal; font-feature-settings:normal;
              text-align:start; letter-spacing:0px; word-spacing:0px; writing-mode:lr-tb; text-anchor:middle;
              fill-opacity:1; stroke:#FFFFFF;
              stroke-width:0; stroke-linecap:butt; stroke-linejoin:miter; stroke-opacity:1;
              stroke-miterlimit:4; stroke-dasharray:none
            {'}'}
          </style>''' )
      if family=='LMsans':
        print(f'''    <style>
        .mytext {'{'}
          line-height:125%;
          font-style:normal;font-variant:normal;font-weight:{weight};font-stretch:normal;
          font-family:"Latin Modern Sans";-inkscape-font-specification:"Latin Modern Sans";
          text-align:center;text-anchor:middle;
          fill-opacity:1; stroke:#FFFFFF;
          stroke-width:0; stroke-linecap:butt; stroke-linejoin:miter; stroke-opacity:1;
          stroke-miterlimit:4; stroke-dasharray:none
        {'}'}
          </style>''' )


    def put_bubble(self, t, x, y):
      print(f'  <use x="{x}" y="{y}" xlink:href="#bubble{str(t)}" />');


    def put_liaison(self, t0, x0, y0, t1, x1, y1_, alpha=None, h=None, auto=False):

        r0 = self.bubble[t0]['r']+self.bubble[t0]['stroke_w']/2
        r1 = self.bubble[t1]['r']+self.bubble[t1]['stroke_w']/2

        if r0 < r1:
           self.put_liaison(t1, x1, y1_, t0, x0, y0, alpha, h, auto)
           return

        angle = math.pi/2 - math.atan2(y1_-y0,x1-x0)
        l = math.sqrt( (x0-x1)**2 + (y0-y1_)**2)
        x = x0
        y1 = y0+l

        if h is None:
            h = 0.666*r1
        if abs(r0-r1)>1e-4:
            self.put_liaison_diffr(x,y0,y1,t0,t1,alpha,h,angle, auto)
        else:
            self.put_liaison_equal(x,y0,y1,t0,t1,h, angle)

    def put_liaison_equal(self, x,y0,y1,t0,t1,h,angle):

      r0 = self.bubble[t0]['r']+self.bubble[t0]['stroke_w']/2

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


    def put_liaison_diffr(self, x,y0,y1,t0,t1,alpha,h,angle, auto=False):
      #def cross2lines(x_1, y_1, x_2, y_2, x_3, y_3, x_4, y_4):
      #    x = ((x_1*y_2-y_1* x_2)*(x_3-x_4)-(x_1-x_2)*(x_3 *y_4-y_3* x_4)) / ((x_1-x_2)*(y_3-y_4)-(y_1-y_2)*(x_3-x_4))
      #    y = ((x_1*y_2-y_1* x_2)*(y_3-y_4)-(y_1-y_2)*(x_3 *y_4-y_3* x_4)) / ((x_1-x_2)*(y_3-y_4)-(y_1-y_2)*(x_3-x_4))
      #    return x,y
      def PX(x, y0, y1, l, EO1, C, D, X11, X12, cosa, sina):
          px = x                            - cosa*l*C / ( EO1 * math.sqrt(D) )
          py = (X11*y0-X12*y1)/math.sqrt(D) - sina*l*C / ( EO1 * math.sqrt(D) )
          return px, py

      def get_coord(alpha):
        sina = math.sin((90-alpha)/180*math.pi) # угол между секущей и прямой соединяющей центры
        cosa = math.cos((90-alpha)/180*math.pi)
        # пересечение секущих с окружностями
        B = 2 * EO1 * sina
        C = EO1**2-r1**2
        D = B*B-4*C
        X11 = (-B +math.sqrt(D))*0.5
        X12 = (-B -math.sqrt(D))*0.5
        X21 = X11 * r0/r1
        # px, py = cross2lines(x,y0,Cx+X21*cosa,Cy+X21*sina, x, y1, Cx+X12*cosa,  Cy+X12*sina) # центр касательной окружности
        # print('X', px, '\t', py)
        px, py = PX(x, y0, y1, l, EO1, C, D, X11, X12, cosa, sina)
        # print('X', px, '\t', py)
        R = math.sqrt((px-(Cx+X21*cosa))**2 + (py-(Cy+X21*sina))**2) # радиус касательной окружности
        h = 2*(x-px-R)
        return sina, cosa, X12, X21, R, h


      r0 = self.bubble[t0]['r']+self.bubble[t0]['stroke_w']/2
      r1 = self.bubble[t1]['r']+self.bubble[t1]['stroke_w']/2
      l = abs(y1-y0)
      EO1 = r1*l / (r0-r1)
      EO0 = EO1+l
      Cx = x
      Cy = y1+EO1
      cosb = r1/EO1

      alpha_max = math.asin(cosb)/math.pi*180
      if alpha is None:
          alpha = 0.5*alpha_max

      if auto==False:
          sina, cosa, X12, X21, R, hh = get_coord(alpha)
      else:
          from scipy import optimize
          alpha = optimize.fsolve(lambda x: get_coord(x)[-1]-h, alpha) #, method=None, jac=None, hess=None, hessp=None, bounds=None, constraints=(), tol=None, callback=None, options=None)
          sina, cosa, X12, X21, R, hh = get_coord(alpha)


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
      l = (len(text)-1.5)/2
      print(f'    <tspan x="{x}" dy="{-l}em">', text[0], '</tspan>')
      for line in text[1:]:
        print(f'    <tspan x="{x}" dy="1em">', line, '</tspan>')
      print('  </text>')

