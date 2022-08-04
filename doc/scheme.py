#!/usr/bin/env python3

import math


def same_size(x, y0, y1, r0, h=40):
    # the circles
    print(f'  <circle cx="{x}" cy="{y0}" r="{r0}" stroke="black" stroke-width="1" fill="white" />')
    print(f'  <circle cx="{x}" cy="{y1}" r="{r0}" stroke="black" stroke-width="1" fill="white" />')

    # the line connecting the centers
    print(f'  <line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" style="stroke:rgb(255,0,0);stroke-width:1" />')
    l = abs(y1-y0)

    # the radius of the tangent circles
    R = (0.25*l**2+0.25*h**2-r0**2) / (2*r0-h)

    # the tangent circles
    dx = 0.5*h+R
    dy = (y1-y0)*0.5
    print(f'  <circle cx="{x+dx}" cy="{y0+dy}" r="{R}" stroke="black" stroke-width="1" fill="white" />')
    print(f'  <circle cx="{x-dx}" cy="{y0+dy}" r="{R}" stroke="black" stroke-width="1" fill="white" />')

    # the points where the tangent circles touch the main circles
    xx = dx*r0 / math.hypot(dx, dy)
    yy = dy*r0 / math.hypot(dx, dy)
    print(f'  <circle cx="{x+xx}" cy="{y0+yy}" r="{1}" stroke="#00FFFF" stroke-width="1" fill="white" />')
    print(f'  <circle cx="{x-xx}" cy="{y0+yy}" r="{1}" stroke="#00FFFF" stroke-width="1" fill="white" />')
    print(f'  <circle cx="{x+xx}" cy="{y1-yy}" r="{1}" stroke="#00FFFF" stroke-width="1" fill="white" />')
    print(f'  <circle cx="{x-xx}" cy="{y1-yy}" r="{1}" stroke="#00FFFF" stroke-width="1" fill="white" />')
    print()


def diff_size(x, y0, y1, r0, r1, alphafrac=0.75):

    def linecross(x_1, y_1, x_2, y_2, x_3, y_3, x_4, y_4):
        # crossing point of the lines [(x_1,y_1),(x_2,y_2)] and [(x_3,y_3),(x_4,y_4)]
        x = ((x_1*y_2-y_1*x_2)*(x_3-x_4)-(x_1-x_2)*(x_3*y_4-y_3*x_4)) / ((x_1-x_2)*(y_3-y_4)-(y_1-y_2)*(x_3-x_4))
        y = ((x_1*y_2-y_1*x_2)*(y_3-y_4)-(y_1-y_2)*(x_3*y_4-y_3*x_4)) / ((x_1-x_2)*(y_3-y_4)-(y_1-y_2)*(x_3-x_4))
        return x, y

    # the circles
    print(f'  <circle cx="{x}" cy="{y0}" r="{r0}" stroke="black" stroke-width="1" fill="white" />')
    print(f'  <circle cx="{x}" cy="{y1}" r="{r1}" stroke="black" stroke-width="1" fill="white" />')

    # the line connecting the centers
    print(f'  <line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" style="stroke:rgb(255,0,0);stroke-width:1" />')
    l = abs(y1-y0)

    # the homothetic center
    EO1 = r1*l / (r0-r1)
    EO0 = EO1+l
    Cx = x
    Cy = y1+EO1
    print(f'  <circle cx="{Cx}" cy="{Cy}" r="{1}" stroke="red" stroke-width="1" fill="white" />')

    # the points where the tangent rays touch the circles
    cosmaxb = r1/EO1
    sinmaxb = math.sqrt(1-cosmaxb**2)
    tx1 = math.sqrt(EO1**2-r1**2) * cosmaxb
    ty1 = math.sqrt(EO1**2-r1**2) * sinmaxb
    print(f'  <circle cx="{Cx+tx1}" cy="{Cy-ty1}" r="{1}" stroke="red" stroke-width="1" fill="white" />')
    print(f'  <circle cx="{Cx-tx1}" cy="{Cy-ty1}" r="{1}" stroke="red" stroke-width="1" fill="white" />')
    tx0 = math.sqrt(EO0**2-r0**2) * cosmaxb
    ty0 = math.sqrt(EO0**2-r0**2) * sinmaxb
    print(f'  <circle cx="{x+tx0}" cy="{Cy-ty0}" r="{1}" stroke="red" stroke-width="1" fill="white" />')
    print(f'  <circle cx="{x-tx0}" cy="{Cy-ty0}" r="{1}" stroke="red" stroke-width="1" fill="white" />')

    # the angle between the tangent ray and the line connecting the centers
    max_alpha = math.asin(cosmaxb)

    # the tangent rays
    print(f'  <line x1="{Cx}" y1="{Cy}" x2="{Cx+300*cosmaxb}" y2="{Cy-300*sinmaxb}" style="stroke:grey;stroke-width:1;stroke-opacity:0.3" />')
    print(f'  <line x1="{Cx}" y1="{Cy}" x2="{Cx-300*cosmaxb}" y2="{Cy-300*sinmaxb}" style="stroke:grey;stroke-width:1;stroke-opacity:0.5" />')

    # the angle between the secant ray and the line connecting the centers
    alpha = alphafrac * max_alpha
    sinb = math.cos(alpha)
    cosb = math.sin(alpha)

    # the secant rays
    print(f'  <line x1="{Cx}" y1="{Cy}" x2="{Cx+300*cosb}" y2="{Cy-300*sinb}" style="stroke:grey;stroke-width:1" />')
    print(f'  <line x1="{Cx}" y1="{Cy}" x2="{Cx-300*cosb}" y2="{Cy-300*sinb}" style="stroke:grey;stroke-width:1" />')

    # crossing points of the rays and the circles
    B = 2 * EO1 * sinb
    C = EO1**2-r1**2
    D = B*B-4*C
    X11 = (-B+math.sqrt(D))*0.5
    X12 = (-B-math.sqrt(D))*0.5
    print(f'  <circle cx="{Cx+X11*cosb}" cy="{Cy+X11*sinb}" r="{1}" stroke="red" stroke-width="1" fill="white" />')
    print(f'  <circle cx="{Cx-X11*cosb}" cy="{Cy+X11*sinb}" r="{1}" stroke="red" stroke-width="1" fill="white" />')
    print(f'  <circle cx="{Cx+X12*cosb}" cy="{Cy+X12*sinb}" r="{1}" stroke="cyan" stroke-width="1" fill="white" />')
    print(f'  <circle cx="{Cx-X12*cosb}" cy="{Cy+X12*sinb}" r="{1}" stroke="red" stroke-width="1" fill="white" />')
    X21 = X11 * r0/r1
    X22 = X12 * r0/r1
    print(f'  <circle cx="{Cx+X21*cosb}" cy="{Cy+X21*sinb}" r="{1}" stroke="cyan" stroke-width="1" fill="white" />')
    print(f'  <circle cx="{Cx-X21*cosb}" cy="{Cy+X21*sinb}" r="{1}" stroke="red" stroke-width="1" fill="white" />')
    print(f'  <circle cx="{Cx+X22*cosb}" cy="{Cy+X22*sinb}" r="{1}" stroke="red" stroke-width="1" fill="white" />')
    print(f'  <circle cx="{Cx-X22*cosb}" cy="{Cy+X22*sinb}" r="{1}" stroke="red" stroke-width="1" fill="white" />')
    # we know that the tangent circle touches the main circles in the cyan points

    # the tangent circle
    px, py = linecross(x, y0, Cx+X21*cosb, Cy+X21*sinb, x, y1, Cx+X12*cosb, Cy+X12*sinb)  # center
    R = math.hypot(px-(Cx+X21*cosb), py-(Cy+X21*sinb))                                    # radius
    print(f'  <circle cx="{px}" cy="{py}" r="{R}" stroke="grey" opacity="0.5" stroke-width="1" fill="white" />')

    # the exact liaison
    print(f'''  <g id="liason0" fill="red" opacity="0.1" > <path d="
    M {Cx+X12*cosb} {Cy+X12*sinb}
    A {R},  {R}  0 0 0 {Cx+X21*cosb} {Cy+X21*sinb}
    A {r0}, {r0} 0 0 0 {Cx-X21*cosb} {Cy+X21*sinb}
    A {R},  {R}  0 0 0 {Cx-X12*cosb} {Cy+X12*sinb}
    A {r1}, {r1} 0 0 0 {Cx+X12*cosb} {Cy+X12*sinb}
  "/></g>''')

    # a more simple liaison that doesn't clip
    print(f'''  <g id="liason1" fill="blue" opacity="0.1" > <path d="
    M {Cx+X12*cosb} {Cy+X12*sinb}
    A {R},  {R}  0 0 0 {Cx+X21*cosb} {Cy+X21*sinb}
    H {Cx-X21*cosb}
    A {R},  {R}  0 0 0 {Cx-X12*cosb} {Cy+X12*sinb}
    z
  "/></g>''')
    print()


def main():
    print('<svg xmlns="http://www.w3.org/2000/svg" '
          'xmlns:xlink="http://www.w3.org/1999/xlink" '
          'width="400" height="300">')

    x  = 100
    y0 = 80
    r0 = 40
    y1 = 180
    # the distance between the tangent circles (the liaison width parameter)
    h  = 40
    same_size(x, y0, y1, r0, h=h)

    x  = 320
    y0 = 80
    r0 = 40
    y1 = 180
    r1 = 20
    # the ratio of the angle between the secant ray and the line connecting the centers
    # to the angle between the tangent ray and the line connecting the centers
    # (affects the liaison width)
    af = 0.75
    diff_size(x, y0, y1, r0, r1, alphafrac=af)

    print("</svg>\n")


if __name__ == '__main__':
    main()

