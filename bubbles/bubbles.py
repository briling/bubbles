import math


class Bubble_World:
    def __init__(self,
                 xcanv=None, ycanv=None,
                 grad_offset=30.0,
                 font_family='Latin Modern Sans', font_weight='normal'):
        self.pars = locals(); self.pars.pop('self')
        self.bubble = {}  # bubble definitions
        self._bubbles  = []  # bubble placements (id, x, y)
        self._liaisons = []
        self._texts    = []
        self._colors   = []  # color definition

    def _format_head(self,xcanv, ycanv):
        print('<svg xmlns="http://www.w3.org/2000/svg" '
              'xmlns:xlink="http://www.w3.org/1999/xlink" '
              f'width="{xcanv}" height="{ycanv}">')

    def _format_tail(self):
        print('</svg>')

    
    def _format_defs(self, dump=False, grad_offset=30.0, font_family='Latin Modern Sans', font_weight='normal'):
        ret  = '  <defs>\n'
        ret += self._format_def_bubbles(dump=dump)
        ret += '\n'
        ret += self._format_def_gradients(dump=dump, offset=grad_offset)
        ret += '\n'
        ret += self._format_def_fonts(family=font_family, weight=font_weight)
        ret += '  </defs>\n\n'
        return ret

    def _format_def_bubbles(self, dump=False):

        ret = ""
        if dump is True:
            idx = set([a[0][0] for a,k in self._bubbles])
        else:
            idx = list(self.bubble.keys())

        for i in idx:
            bub = self.bubble[i]
            cf = self._colors[bub['fill']]
            cs = self._colors[bub['stroke']]
            ret += f"    <circle id='bubble{str(i)}' cx='0' cy='0' r='{bub['r']}' "
            ret += f"fill='#{cf:06x}' stroke='#{cs:06x}' stroke-width='{bub['stroke_w']}'/>\n"

        return ret

    def _format_def_gradients(self, offset=30.0, dump=False):

        ret = ""
        if dump is True:
            idx = [(self.bubble[a[0][0]]['stroke'], self.bubble[a[1][0]]['stroke']) for [a,k] in self._liaisons]
        else:
            idx = [(self.bubble[i      ]['stroke'], self.bubble[j      ]['stroke']) for i in self.bubble.keys() for j in self.bubble.keys()]

        for i,j in set(idx):
            coli = self._colors[i]
            colj = self._colors[j]
            ret += f'    <linearGradient id="myGradient{i}.{j}" x1="0" x2="0" y1="0" y2="1">'
            ret += f'<stop offset="{offset}%"     stop-color="#{coli:06x}"/> '
            ret += f'<stop offset="{100-offset}%" stop-color="#{colj:06x}"/> '
            ret += f'</linearGradient>\n'
            
        return ret

    def _format_def_font(self, family='Latin Modern Sans', weight='normal'):
        # font examples: 'Latin Modern Sans', 'Adobe Helvetica', 'monospace'
        return f'''    <style>
        .mytext {{
          font-style:normal; font-variant:normal; font-weight:{weight}; font-stretch:normal;
          line-height:125%;
          font-family:"{family}"; -inkscape-font-specification:"{family}";
          font-variant-ligatures:normal; font-variant-caps:normal; font-variant-numeric:normal; font-feature-settings:normal;
          text-align:start; letter-spacing:0px; word-spacing:0px; writing-mode:lr-tb; text-anchor:middle;
          fill-opacity:1; stroke:#FFFFFF;
          stroke-width:0; stroke-linecap:butt; stroke-linejoin:miter; stroke-opacity:1;
          stroke-miterlimit:4; stroke-dasharray:none
        }}
    </style>'''

    def _format_bubble(self, a):
        t, x, y = a
        return f'  <use x="{x}" y="{y}" xlink:href="#bubble{str(t)}" />\n'

    def _format_liaison(self, a0, a1, h=None, auto=True, alpha=None, tol=1e-4):
        t0, x0, y0 = a0
        t1, x1, y1 = a1
        r0 = self.bubble[t0]['r']+self.bubble[t0]['stroke_w']/2
        r1 = self.bubble[t1]['r']+self.bubble[t1]['stroke_w']/2
        col0 = self.bubble[t0]['stroke']
        col1 = self.bubble[t1]['stroke']

        # virtually align the liaison with the y-axis
        angle, y11 = self.liaison_angle(x0, x1, y0, y1)
        path = self.liaison_path(r0, r1, x0, y0, y11, alpha, h, auto, tol)

        return f'  <g transform="rotate({-angle},{x0},{y0})"> <path d=" '+\
               path+\
               f'" fill="url(\'#myGradient{col0}.{col1}\')" /> </g>\n'

    def _format_text(self, x,y, text, fs=12, fc=0x000000):
        print(f'  <text x="{x}" y="{y}" class="mytext" font-size="{fs}px" fill="#{fc:06x}">')
        l = (len(text)-1.5)/2
        for i,line in enumerate(text):
            print(f'    <tspan x="{x}" dy="{-l if i==0 else 1}em"> {line} </tspan>')
        print('  </text>')
    
    def _format_all_liaisons(self):
        ret = ''
        for [a,k] in self._liaisons:
            ret += self._format_liaison(*a, **k)
        return ret

    def _format_all_bubbles(self):
        ret = ''
        for [a,k] in self._bubbles:
            ret += self._format_bubble(*a, **k)
        return ret

    def _format_all_texts(self):
        ret = ''
        for [a,k] in self._texts:
            ret += self._format_text(*a, **k)
        return ret

    def def_bubble(self, key, fill=0xFFFFFF, r=50, stroke=0x990000, stroke_w=10):

        def findcolor(c):
            if c not in self._colors:
                self._colors.append(c)
            return self._colors.index(c)

        self.bubble[key] = {'fill'     : findcolor(fill),
                            'r'        : r,
                            'stroke'   : findcolor(stroke),
                            'stroke_w' : stroke_w,
                            }

    def add_liaison(self, *args, **kwargs):
        self._liaisons.append((args, kwargs))

    def add_bubble(self, *args, **kwargs):
        self._bubbles.append((args, kwargs))

    def add_text(self, *args, **kwargs):
        self._texts.append((args, kwargs))


    def dump(self):
        ret  = self._format_head(*self.get_canvsize())
        ret += self._format_defs(dump=True, grad_offset=self.pars['grad_offset'], font_family=self.pars['font_family'], font_weight=self.pars['font_weight'])
        ret += self._format_all_liaisons()
        ret += '\n'
        ret += self._format_all_bubbles()
        ret += '\n'
        ret += self._format_all_texts()
        ret += '\n'
        ret += self._format_tail()
        return ret

    def get_canvsize(self):
        xcanv = self.pars['xcanv']
        ycanv = self.pars['ycanv']
        if xcanv is None or ycanv is None:
            xmax = ymax = 0
            rmean = 0
            for [a,k] in self._bubbles:
                t,x,y = a[0]
                r = self.bubble[t]['r']+self.bubble[t]['stroke_w']/2
                xmax = max(xmax, x+r)
                ymax = max(ymax, y+r)
                rmean += r
            rmean /= len(self._bubbles)
            if xcanv is None: xcanv = xmax+rmean/2
            if ycanv is None: ycanv = ymax+rmean/2
        return xcanv, ycanv


class BondSolver:
    
    @staticmethod
    def liaison_path(r0, r1, x0, y0, y11, alpha, h, auto, tol):
        if h is None:
            h = 0.666*r1
        if abs(r0-r1) > 1e-4:
            curv1,curv2, (x1,y1), dx0, dx1 = BondSolver._compute_circles_diffr(r0, r1, x0, y0, y11, alpha=alpha, h=h, auto=auto, tol=tol)
        else:
            #curv1,curv2, (x1,y1), dx0, dx1 = BondSolver._compute_circles_equal(r0, x0, y0, y11, h)
            curv1,curv2, (x1,y1), dx0, dx1 = BondSolver._compute_bezier(r0, r1, x0, y0, y11, h, theta0=math.pi/6, theta1=math.pi/6, tol=tol)

        # move to C1, C1 -> C0 path, cross-C0 path, C0 -> C1 path, cross-C1 path, close.
        return f'M {x1} {y1} '\
               f'{curv1} '\
               f'a {r0*1.01}, {r0*1.01} 0 0 0 {-dx0} 0'\
               f'{curv2} '\
               f'a {r1*1.01}, {r1*1.01} 0 0 0 {+dx1} 0'\
               f'z'

    @staticmethod
    def liaison_angle(x0, x1, y0, y1):
        angle = math.degrees(math.pi*0.5 - math.atan2(y1-y0, x1-x0))
        y11 = y0 + math.hypot(x0-x1, y0-y1)
        return angle, y11

    @staticmethod
    def _compute_circles_equal(r0, x, y0, y1, h):

        '''
        There are 2 circles C0, C1 with radius r0 centered at the points (x,y0) and (x,y1).
        We search for two other circles C2, C2' of the same radius tangent to C0 and C1
        so that the shortest distance between C2 and C2' = h.
        R is the radius of C2 and C2' and other values are needed to find the tangent points
        required to draw the liaison using the arc svg shape.

        All the equations can be easily derived used the Pythagorean theorem.
        '''

        l = abs(y1-y0)
        assert 0.5*h <= r0 , f"bad h parameter, should be less or equal to {2*r0}"
        if 0.5*l < r0:
            assert 0.25*(l**2+h**2) >= r0**2, f"bad h parameter, should be greater or equal to {2*math.sqrt(r0**2-l**2/4)}"
        
        R = (0.25*l**2 + 0.25*h**2 - r0**2) / (2.0*r0 - h)

        dx = 0.5*h + R
        dy = 0.5*l
        dr = math.hypot(dx, dy)

        # position of a tangent point wrt C0's center
        xx = dx*r0 / dr
        yy = dy*r0 / dr

        # R, R, rotation, flag,flag, travel_x, travel_y
        curv1 = f'a {R}, {R}  0 0 0 0 {+2.0*(dy-yy)} '
        curv2 = f'a {R}, {R}  0 0 0 0 {-2.0*(dy-yy)} '
        return curv1,curv2 (x+xx, y0+yy), 2*xx, +2*xx
        

    @staticmethod
    def _compute_ellipses_equal(r0, x, y0, y1, h):

        '''
        There are 2 circles C0, C1 with radius r0 centered at the points (x,y0) and (x,y1).
        We search for two ellipses E2, E2' of the same radii, tangent to C0 and C1
        so that the shortest distance between E2 and E2' = h.
        R1 is the 'horizontal radius' of E2 and E2',
        R2 is their 'vertical radius', and a*R1 is the radius at the tangent points.
        other values are also needed to link the tangent points in the svg arc shape.
        '''

        l = abs(y1-y0)
        assert 0.5*h <= r0 , f"bad h parameter, should be less or equal to {2*r0}"
        assert abs(a)>=1, "bad a elongation parameter: should be bigger than 1 in amplitude"
        if 0.5*l < r0:
            assert 0.25*(l**2+h**2) >= r0**2, f"bad h parameter, should be greater or equal to {2*math.sqrt(r0**2-l**2/4)}"
        
        # from the Pythagorean theorem, we get:
        # (a**2 -1) * R1**2 + (2*r0*a -h)*R1 + (r0**2 - h**2/4 - l**2/4) = 0
        # which gives a determinant of
        R1det = (h**2 + l**2)*a**2 - 4*h*r0*a - l**2 + 4*r0**2 
        # which is a polynomial of a, that we want positive
        if R1det<0:
            part1 = 2*h*r0/(h**2 + l**2)
            part2 = l*math.sqrt(h**2 + l**2 - 4*r0**2)/(h**2 + l**2)
            raise AssertionError(f"bad a elongation parameter: should be between {max(1,part1-part2)} and {part1+part2}.")
        # there are often two roots to the main polynomial, but often only one positive one
        # since the roots are (-b±sqrt(det))/2a, we compare the amplitudes of b**2 and det
        # which, since h**2+l**2 >= 4*r0**2,
        # det_bigger = abs(a) >= 1
        # which also means that there is no solution for abs(a)<1, which is why we checked that at the start
        denom = 2*(a**2 -1)
        part1 = (2*a*r0 - h)/denom
        part2 = math.sqrt(R1det)/denom
        if denom <0:
            R1 = part1 - part2
        else:
            R1 = part1 + part2

        dx = 0.5*h + R1
        dy = 0.5*l
        dr = math.hypot(dx, dy)
        
        # and now we fetch R2=R1*a0, given that the ellipse is given by (y/a0**2 +x**2 = R1**2
        # =>  1/a**2 = (sin(theta)/(a0))**2 +cos(theta)**2
        #theta = math.arctan(dy/dx)
        tan_theta = dy/dx
        sin_theta = tan_theta/math.sqrt(tan_theta**2 +1)
        a0 = 1/math.sqrt(1/(a*sin_theta)**2 - 1/tan_theta**2)

        # position of a tangent point wrt C0's center
        xx = dx*r0 / dr
        yy = dy*r0 / dr

        # R, R, rotation, flag,flag, travel_x, travel_y
        curv1 = f'a {R1}, {R1*a0}  0 0 0 0 {+2.0*(dy-yy)}'
        curv2 = f'a {R1}, {R1*a0}  0 0 0 0 {-2.0*(dy-yy)}'
        return curv1,curv2, (x+xx, y0+yy), 2*xx, +2*xx
    
    
    @staticmethod
    def _compute_circles_diffr(r0, r1, x, y0, y1, alpha, h, auto=True, tol=1e-4):

        '''
        There are 2 circles C0, C1 with radii r0!=r1 centered at the points (x,y0) and (x,y1).
        We search for two other circles C2, C2' of the same radius tangent to C0 and C1
        so that the shortest distance between C2 and C2' = h.
        R is the radius of C2 and C2' and other values are needed to find the tangent points
        required to draw the liaison using the arc svg shape.

        In this case (r0!=r1) the derivation is less straightforward
        (see https://en.wikipedia.org/wiki/Homothetic_center#Tangent_circles_and_antihomologous_points).
        We can send two secant rays from the homothetic center
        (specifying the angle between the rays and the line connecting the centers)
        and thus find the tangent points and then R.
        However I could not find a closed expression connecting these values to h
        so the right angle is found with numerical golden-rule search.
        '''

        def PX(y0, y1, l, EO1, B, C, sD, cosb, sinb):
            # obtained from a simplification of the general expression for the crossing of two lines
            px = cosb*l*C / (EO1 * sD)
            py = sinb*l*C / (EO1 * sD) - 0.5 * (B*l/sD + (y0+y1))
            return px, py

        def get_coord(alpha):
            # the angle complementary to the angle between the secant and the line connecting the centers
            sinb = math.cos(alpha)
            cosb = math.sin(alpha)
            # crossing points of the secants with the circles
            B   = 2 * EO1 * sinb
            C   = EO1**2-r1**2
            sD  = math.sqrt(B*B-4*C)
            X11 = (-B+sD)*0.5
            X12 = (-B-sD)*0.5
            X21 = X11 * r0/r1
            px, py = PX(y0, y1, l, EO1, B, C, sD, cosb, sinb)  # center of the tangent circle (with x==Cx==0)
            R = math.hypot(px+(X21*cosb), py+(Cy+X21*sinb))    # radius of the tangent circle
            h = 2*(px-R)                                       # distance between the two tangent circles
            return sinb, cosb, X12, X21, R, h

        # the homothetic center
        l = abs(y1-y0)
        EO1 = r1*l / (r0-r1)
        Cx = x
        Cy = y1+EO1

        # angle between the tangent ray and the line connecting the centers
        sin_alpha_max = r1/EO1
        alpha_max = math.asin(sin_alpha_max)

        if alpha is None:
            alpha = 0.5*alpha_max
        else:
            alpha = math.radians(alpha)

        if auto is True:
            alpha = alpha_max * _gold(lambda x: (get_coord(x*alpha_max)[-1]-h)**2, tol, 0, (1-1e-5))

        sinb, cosb, X12, X21, R, hh = get_coord(alpha)

        # R, R, rotation, flag,flag, travel_x, travel_y
        curv1 = f'a {R}, {R}  0 0 0 {(X21-X12)*cosb} {+(X21-X12)*sinb}'
        curv2 = f'a {R}, {R}  0 0 0 {(X21-X12)*cosb} {-(X21-X12)*sinb}'
        return curv1,curv2, (Cx+X12*cosb, Cy+X12*sinb), 2*X21*cosb, 2*X12*cosb
        
        # curv1 = f'a {R}, {R}  0 0 0 {(X12-X21)*cosb} {+(X12-X21)*sinb}'
        # curv2 = f'a {R}, {R}  0 0 0 {(X12-X21)*cosb} {-(X12-X21)*sinb}'
        # return curv1,curv2, (Cx-X21*cosb, Cy-X21*sinb), +2*X21*cosb, -2*X12*cosb


    @staticmethod
    def _compute_bezier(r0, r1, x, y0, y1, h, theta0, theta1, tol=1E-4):
        '''
        There are 2 circles C0, C1 with radius r0 centered at the points (x,y0) and (x,y1).
        we search for two (well, four) cubic polynomials x=f(y) that start tangent to C0 at theta0
        away from the C0-C1 line, then goes to be parallel to the C0-C1 line, at distance h/2 from it.
        From there, switch to the second polynomial and end up tangent to C1 at theta1 away from the C0-C1 line.
        At the point where these polynomials join, both first and second derivative must be the same.
        '''

        assert 0<=theta0<=math.pi/2, 'bad theta0: must be in [0;pi/2]'
        assert 0<=theta1<=math.pi/2, 'bad theta1: must be in [0;pi/2]'
        l = abs(y1-y0)
        # points and derivatives at the circles
        xx0 = r0*math.sin(theta0)
        yy0 = r0*math.cos(theta0)
        dd0 = -yy0/xx0  # dd0b = dd0*(yy2-yy0)
        xx1 = r1*math.sin(theta1)
        yy1 = r1*math.cos(theta1)
        dd1 = yy1/xx1  # dd1b = dd1*(yy2-yy1)
        xx2 = h/2
        assert xx2 <= min(xx0,xx1), 'h parameter too big: must be smaller than the diameter of the smallest circle'
        # check that the tangents do cross "below" the x=h/2 line
        assert xx1/dd1 + xx0/dd0 <= (yy1-yy0),  'theta parameters too high: tangents cross too high'

        # cubic interpolations: 
        # t0 = (y-yy0)/(yy2-yy0); t1=(y-yy1)/(yy2-yy1)
        # x[0] = (2*xx0 -2*xx2 +dd0b)*t0**3 + (-3*xx0 +3*xx2 -2*dd0b)*t0**2 + dd0b*t0 + xx0
        # x[1] = (2*xx1 -2*xx2 +dd1b)*t1**3 + (-3*xx1 +3*xx2 -2*dd1b)*t1**2 + dd1b*t1 + xx1
        # dx[0]/dt0 = (6*xx0 -6*xx2 +6*dd0b)*t0**2 + (-6*xx0 +6*xx2 -4*dd0b)*t0 + dd0b
        # d2x[0]/dt02 = (12*xx0 -12*xx2 +12*dd0b)*t0 + (-6*xx0 +6*xx2 -4*dd0b)
        # d2x[0]/dy2 = ( (12*xx0 -12*xx2 +12*dd0b)*t0 + (-6*xx0 +6*xx2 -4*dd0b) )/(yy2-yy0)**2
        # we also want the second derivative to be positive for all the segment:
        # dd0*(yy2-yy0) +1.5*(xx0-xx2) >= 0   =>  yy2 >= 1.5*(xx2-xx0)/dd0 + yy0
        
        
        # d2x[0]/dy2(t0=1) =  (6*xx0 -6*xx2 +8*dd0*(yy2-yy0))/(yy2-yy0)**2
        ### d2x[0]/dy2(t0=1) is strictly monotonous with yy2, if yy2>yy0
        ### same thing with d2x[0]/dy2(t0=1) when yy2<yy1:
        # we can numerically find the yy2 where they are equal
        if abs(r0/r1) <1E-4:
            yy2 = 0.5*(yy1+yy0)
        else:
            def f(yy2):
                return (
                    +(6*xx0 -6*xx2 +8*dd0*(yy2-yy0))/(yy2-yy0)**2
                    -(6*xx1 -6*xx2 +8*dd1*(yy2-yy1))/(yy2-yy1)**2
                )
            yy2 = _bisect_root(f, tol,yy0+1E-5,yy1-1E-5)

        # now, convert the cubic splines to Besier splines:
        # we just need to have the control points be at 1/3 and 2/3 of the y axis of each segment
        # first segment: ctrl0 relative to pt0
        # second segment: ctrl1 relative to pt2
        
        dyy2 = yy2-yy0
        dxx2 = xx2-xx0
        sublen0 = dyy2/3
        dyy1 = yy1-yy2
        dxx1 = xx1-xx2
        sublen1 = dyy1/3
        
        ctrl0a = sublen0, sublen0*dd0
        ctrl0b = 2*sublen0, dxx2
        # ctrl1 relative to pt2
        ctrl1a = sublen1, 0
        ctrl1b = 2*sublen1, dxx1+sublen1*dd1

        curv1 = f'c {ctrl0a[1]} {ctrl0a[0]}, {ctrl0b[1]} {ctrl0b[0]}, {dxx2} {dyy2} '\
                f'c {ctrl1a[1]} {ctrl1a[0]}, {ctrl1b[1]} {ctrl1b[0]}, {dxx1} {dyy1}'
        # and now the curve on the other side
        curv2 = f'c {ctrl1b[1]-dxx1} {ctrl1b[0]-dyy1}, {ctrl1a[1]-dxx1} {ctrl1a[0]-dyy1}, {-dxx1} {-dyy1} '\
                f'c {ctrl0b[1]-dxx2} {ctrl0b[0]-dyy2}, {ctrl0a[1]-dxx2} {ctrl0a[0]-dyy2}, {-dxx2} {-dyy2}' 
        
        return curv1,curv2, (x+xx0, y0+yy0), 2*xx0, 2*xx1

def _gold(f, eps, bra, ket):
    """Golden ratio optimisation: find a local minimum for f between bra and key, with tolerence eps"""
    phi = (math.sqrt(5.0)-1.0)*0.5
    d   = ket-bra
    x1  = ket-d*phi
    x2  = bra+d*phi
    y1  = f(x1)
    y2  = f(x2)
    for k in range(666):
        c = (bra+ket)*0.5
        if 0: print(f"{k:5d} a={bra:20.15f} b={ket:20.15f} c={c:20.15f} d={d:20.15f} y1={y1:+e} y2={y2:+e}")
        if d < eps: return c
        if y1 > y2:
            bra = x1
            x1  = x2
            d = ket-bra
            x2  = bra+d*phi
            y1  = y2
            y2  = f(x2)
        else:
            ket = x2
            x2  = x1
            d = ket-bra
            x1  = ket-d*phi
            y2  = y1
            y1  = f(x1)      
    return c

def _bisect_root(f, eps, bra, ket):
    if bra > ket:
        (bra,ket) = (ket,bra)
    a,b = f(bra),f(ket)
    decreaser = a > b
    assert a*b < 0
    
    while ket-bra > eps:
        x = 0.5*(bra+ket)
        y = f(x)
        if (y>0) ^ decreaser:
            ket = x
        else:
            bra = x
    return x