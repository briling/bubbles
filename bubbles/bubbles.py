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
        self._usedump  = False

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

      if self._usedump:
          idx = []
          for a,k in self._bubbles:
              idx.append(a[0])
      else:
          idx = list(self.bubble.keys())

      for i in sorted(set(idx)):
        bub = self.bubble[i]
        cf = self._colors[bub['fill']]
        cs = self._colors[bub['stroke']]
        print(f"  <symbol id='bubble{str(i)}'> "\
              f"<circle cx='0' cy='0' r='{bub['r']}' "\
              f"fill='#{cf:06x}' stroke='#{cs:06x}' stroke-width='{bub['stroke_w']}'/> "\
              '</symbol>')

    def print_def_gradient(self, offset=30.0):

        if self._usedump:
          idx = []
          for [a,k] in self._liaisons:
            col0 = self.bubble[a[0]]['stroke']
            col1 = self.bubble[a[3]]['stroke']
            idx.append( (col0,col1) )
        else:
          idx = []
          for i in self.bubble.keys():
            for j in self.bubble.keys():
              col0 = self.bubble[i]['stroke']
              col1 = self.bubble[j]['stroke']
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


    def put_liaison(self, t0, x0, y0, t1, x1, y1, h=None, auto=True, alpha=None):

        r0 = self.bubble[t0]['r']+self.bubble[t0]['stroke_w']/2
        r1 = self.bubble[t1]['r']+self.bubble[t1]['stroke_w']/2
        col0 = self.bubble[t0]['stroke']
        col1 = self.bubble[t1]['stroke']

        # virtually align the liaison with the y-axis
        angle = math.pi/2 - math.atan2(y1-y0,x1-x0)
        l   = math.hypot( x0-x1 , y0-y1)
        y11 = y0+l

        if h is None:
            h = 0.666*r1
        if abs(r0-r1)>1e-4:
            R, dx0, dy0, dx1, dy1, dx2 = self.put_liaison_diffr(r0, r1, x0, y0, y11, alpha=alpha, h=h, auto=auto)
        else:
            R, dx0, dy0, dx1, dy1, dx2 = self.put_liaison_equal(r0, x0, y0, y11, h)

        print(f'  <g transform="rotate({-angle/math.pi*180},{x0},{y0})"> <path d=" ' \
              f'M {dx0} {dy0} '\
              f'a {R}, {R}  0 0 0 {dx1} {+dy1} '\
              f'h {dx2} '\
              f'a {R}, {R}  0 0 0 {dx1} {-dy1} '\
              f'z" '\
              f'fill="url(\'#myGradient{col0}.{col1}\')" /> </g>')

    def put_liaison_equal(self, r0, x, y0, y1, h):

      '''
      There are 2 circles C0, C1 with radius r0 centered at the points (x,y0) and (x,y1).
      We search for two other circles C2, C2' of the same radius tangent to C0 and C1
      so that the shortest distance between C2 and C2' = h.
      R is the radius of C2 and C2' and other values are needed to find the tangent points
      required to draw the liaison using the arc svg shape.

      All the equations can be easily derived used the Pythagorean theorem.
      '''

      l = abs(y1-y0)
      R = (0.25*l**2 + 0.25*h**2 - r0**2) / (2.0*r0 - h)

      dx = 0.5*h + R
      dy = 0.5*l
      dr = math.hypot(dx, dy)

      xx = dx*r0 / dr
      yy = dy*r0 / dr
      return R, x+xx, y0+yy, 0,  2.0*(dy-yy), -2.0*xx


    def put_liaison_diffr(self, r0, r1, x, y0, y1, alpha, h, auto=True):

      '''
      There are 2 circles C0, C1 with radii r0!=r1 centered at the points (x,y0) and (x,y1).
      We search for two other circles C2, C2' of the same radius tangent to C0 and C1
      so that the shortest distance between C2 and C2' = h.
      R is the radius of C2 and C2' and other values are needed to find the tangent points
      required to draw the liaison using the arc svg shape.

      In this case (r0!=r1) the derivation is less straightforward
      (see https://en.wikipedia.org/wiki/Tangent_lines_to_circles#Tangent_lines_to_two_circles
      and https://en.wikipedia.org/wiki/Homothetic_center#Tangent_circles_and_antihomologous_points).
      We can send two secant rays from the homothetic center (specifying the angle between the rays)
      and thus find the tangent points and then R.
      However I could not find a closed expression connecting these values to h
      so the right angle is found through 1D optimization.
      '''

      def PX(x, y0, y1, l, EO1, C, D, X11, X12, cosa, sina):
          # obtained from a simplification of the general expression for the crossing of two lines
          px = x                            - cosa*l*C / ( EO1 * math.sqrt(D) )
          py = (X11*y0-X12*y1)/math.sqrt(D) - sina*l*C / ( EO1 * math.sqrt(D) )
          return px, py

      def get_coord(alpha):
        # angle between the secant and the line connecting the centers
        sina = math.sin((90-alpha)/180*math.pi)
        cosa = math.cos((90-alpha)/180*math.pi)
        # crossing point of the secants with the circle
        B = 2 * EO1 * sina
        C = EO1**2-r1**2
        D = B*B-4*C
        X11 = (-B +math.sqrt(D))*0.5
        X12 = (-B -math.sqrt(D))*0.5
        X21 = X11 * r0/r1
        px, py = PX(x, y0, y1, l, EO1, C, D, X11, X12, cosa, sina) # center of the tangent circle
        R = math.sqrt((px-(Cx+X21*cosa))**2 + (py-(Cy+X21*sina))**2) # radius of the tangent circle
        h = 2*(x-px-R)  # distance between the two tangent circles
        return sina, cosa, X12, X21, R, h


      # find the homothetic center
      l = abs(y1-y0)
      EO1 = r1*l / (r0-r1)
      EO0 = EO1+l
      Cx = x
      Cy = y1+EO1
      cosb = r1/EO1 # angle between tangent rays

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
        self._usedump = True
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

