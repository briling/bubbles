import math

class Bubble_World:
    def __init__(self,
                 xcanv=None, ycanv=None,
                 grad_offset=30.0,
                 font_family='Latin Modern Sans', font_weight='normal'):
        self.pars = locals(); self.pars.pop('self')
        self.bubble = {}
        self._bubbles  = []
        self._liaisons = []
        self._texts    = []
        self._colors   = []
        self._colorsid = []

    def def_bubble(self, key, fill=0xFFFFFF, r=50, stroke=0x990000, stroke_w=10):

        def findcolor(c):
            if not c in self._colors:
                self._colors.append(c)
            return self._colors.index(c)

        self.bubble[key] = {'fill'    :findcolor(fill),
                            'r'       :r,
                            'stroke'  :findcolor(stroke),
                            'stroke_w':stroke_w,
                           }

    def print_head(self, xcanv, ycanv):
        print('<svg xmlns="http://www.w3.org/2000/svg" '\
              'xmlns:xlink="http://www.w3.org/1999/xlink" '\
              f'width="{xcanv}" height="{ycanv}">')
    def print_tail(self):
      print('</svg>');

    def print_def(self, grad_offset=30.0, font_family='Latin Modern Sans', font_weight='normal'):
      print('  <defs>');
      self.print_def_gradient(offset=grad_offset)
      print()
      self.print_def_font(family=font_family,weight=font_weight)
      print('  </defs>');
      print()
      self.print_def_bubble()
      print()

    def print_def_bubble(self):

      idx = []
      for a,k in self._bubbles:
          idx.append(a[0])

      for i in sorted(set(idx)):
        bub = self.bubble[i]
        cf = self._colors[bub['fill']]
        cs = self._colors[bub['stroke']]
        print(f"  <symbol id='bubble{str(i)}'> "\
              f"<circle cx='0' cy='0' r='{bub['r']}' "\
              f"fill='#{cf:06x}' stroke='#{cs:06x}' stroke-width='{bub['stroke_w']}'/> "\
              '</symbol>')

    def print_def_gradient(self, offset=30.0):

        idx = []
        for [a,k] in self._liaisons:
          col0 = self.bubble[a[0]]['stroke']
          col1 = self.bubble[a[3]]['stroke']
          idx.append( (col0,col1) )

        for i,j in sorted(set(idx)):
            coli = self._colors[i]
            colj = self._colors[j]
            print(f'    <linearGradient id="myGradient{i}.{j}" x1="0" x2="0" y1="0" y2="1">'\
                  f'<stop offset="{offset}%"     stop-color="#{coli:06x}"/> '\
                  f'<stop offset="{100-offset}%" stop-color="#{colj:06x}"/> '\
                  f'</linearGradient>')

    def print_def_font(self, family='Latin Modern Sans', weight='normal'):
        # font examples: 'Latin Modern Sans', 'Adobe Helvetica', 'monospace'
        print(f'''    <style>
        .mytext {'{'}
          font-style:normal; font-variant:normal; font-weight:{weight}; font-stretch:normal;
          line-height:125%;
          font-family:"{family}"; -inkscape-font-specification:"{family}";
          font-variant-ligatures:normal; font-variant-caps:normal; font-variant-numeric:normal; font-feature-settings:normal;
          text-align:start; letter-spacing:0px; word-spacing:0px; writing-mode:lr-tb; text-anchor:middle;
          fill-opacity:1; stroke:#FFFFFF;
          stroke-width:0; stroke-linecap:butt; stroke-linejoin:miter; stroke-opacity:1;
          stroke-miterlimit:4; stroke-dasharray:none
        {'}'}
        </style>''' )


    def put_bubble(self, t, x, y):
      print(f'  <use x="{x}" y="{y}" xlink:href="#bubble{str(t)}" />');


    def put_liaison(self, t0, x0, y0, t1, x1, y1_, h=None, auto=True, alpha=None):

        r0 = self.bubble[t0]['r']+self.bubble[t0]['stroke_w']/2
        r1 = self.bubble[t1]['r']+self.bubble[t1]['stroke_w']/2

        angle = math.pi/2 - math.atan2(y1_-y0,x1-x0)
        l = math.sqrt( (x0-x1)**2 + (y0-y1_)**2)
        x = x0
        y1 = y0+l

        if h is None:
            h = 0.666*r1
        if abs(r0-r1)>1e-4:
            R, dx0, dy0, dx1, dy1, dx2 = self.put_liaison_diffr(x,y0,y1,t0,t1,alpha,h,auto)
        else:
            R, dx0, dy0, dx1, dy1, dx2 = self.put_liaison_equal(x,y0,y1,t0,t1,h)

        col0 = self.bubble[t0]['stroke']
        col1 = self.bubble[t1]['stroke']
        print(f'  <g transform="rotate({-angle/math.pi*180},{x},{y0})"> <path d=" ' \
              f'M {dx0} {dy0} '\
              f'a {R}, {R}  0 0 0 {dx1} {+dy1} '\
              f'h {dx2} '\
              f'a {R}, {R}  0 0 0 {dx1} {-dy1} '\
              f'z" '\
              f'fill="url(\'#myGradient{col0}.{col1}\')" /> </g>')

    def put_liaison_equal(self, x,y0,y1,t0,t1,h):

      r0 = self.bubble[t0]['r']+self.bubble[t0]['stroke_w']/2

      l = abs(y1-y0)
      R = (0.25*l**2+0.25*h**2-r0**2) / (2*r0-h)

      dx = 0.5*h+R
      dy = (y1-y0)*0.5
      dr = math.sqrt(dx**2 + dy**2)

      xx = dx*r0 / dr
      yy = dy*r0 / dr
      return R, x+xx, y0+yy, 0,  2*(dy-yy), -2*xx

    def put_liaison_diffr(self, x,y0,y1,t0,t1,alpha,h,auto=True):
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

      return R, Cx+X12*cosa, Cy+X12*sina, (X21-X12)*cosa, (X21-X12)*sina, -2*X21*cosa



    def put_text(self, x,y, text, fs=12, fc=0x000000):
      print(f'  <text x="{x}" y="{y}" class="mytext" font-size="{fs}px" fill="#{fc:06x}">')
      l = (len(text)-1.5)/2
      for i,line in enumerate(text):
          print(f'    <tspan x="{x}" dy="{-l if i is 0 else 1}em"> {line} </tspan>')
      print('  </text>')

    def add_liaison(self, *args, **kwargs):
      self._liaisons.append((args, kwargs))

    def add_bubble(self, *args, **kwargs):
      self._bubbles.append((args, kwargs))

    def add_text(self, *args, **kwargs):
      self._texts.append((args, kwargs))

    def put_all_liaisons(self):
      for [a,k] in self._liaisons:
          self.put_liaison(*a, **k)

    def put_all_bubbles(self):
      for [a,k] in self._bubbles:
          self.put_bubble(*a, **k)

    def put_all_texts(self):
      for [a,k] in self._texts:
          self.put_text(*a, **k)

    def dump(self):
        self.print_head(*self.get_canvsize())
        self.print_def(grad_offset=self.pars['grad_offset'], font_family=self.pars['font_family'], font_weight=self.pars['font_weight'])
        self.put_all_liaisons()
        print()
        self.put_all_bubbles()
        print()
        self.put_all_texts()
        print()
        self.print_tail()

    def get_canvsize(self):
        xcanv=self.pars['xcanv']
        ycanv=self.pars['ycanv']
        if xcanv is None or ycanv is None:
            xmax = ymax = 0
            rmean = 0
            for t,x,y in self._bubbles:
                r = self.bubble[t]['r']+self.bubble[t]['stroke_w']/2
                xmax = max(xmax, x+r)
                ymax = max(ymax, y+r)
                rmean += r
            rmean /= len(self._bubbles)
            if xcanv is None: xcanv = xmax+rmean/2
            if ycanv is None: ycanv = ymax+rmean/2
        return xcanv, ycanv

