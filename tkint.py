# This examples runs only in python 3.+ versions since Tkinter was changed
from svg.path import Path, Line, Arc, CubicBezier, QuadraticBezier, parse_path
from tkinter import Tk, Canvas, Frame, BOTH

""" demo of using a great python module svg.path by 
    Lennart Regebro see site: https://pypi.org/project/svg.path/
    to draw svg in Tkinter
"""

from svg.path import Path, Line, Arc, CubicBezier, QuadraticBezier, parse_path

svgpath = """m 76,232.24998 c 81.57846,-49.53502 158.19366,-20.30271 
216,27 61.26714,59.36905 79.86223,123.38417 9,156
-80.84947,31.72743 -125.19991,-53.11474 -118,-91 v 0 """

path = parse_path(svgpath)

# svg.path point method returns a complex number p, p.real and p.imag can pull the x, and y
# # on 0.0 to 1.0 along path, represent percent of distance along path
n = 100  # number of line segments to draw

# pts = []
# for i in range(0,n+1):
#     f = i/n  # will go from 0.0 to 1.0
#     complex_point = path.point(f)  # point(x) is method on svg.path to return point x * 100  percent along path
#     pts.append((complex_point.real, complex_point.imag))

pts = [ (p.real,p.imag) for p in (path.point(i/n) for i in range(0, n+1))]  # list comprehension version or loop above

class SVGcurve(Frame):

    def __init__(self, pts):
        super().__init__()
        self.pts = pts
        self.initUI()

    def initUI(self):
        self.master.title("svg")
        self.pack(fill=BOTH, expand=1)

        canvas = Canvas(self)
        x0, y0 = self.pts[0]
        for x1, y1 in self.pts[1:]:
            canvas.create_line(x0, y0, x1, y1)
            x0, y0 = x1, y1

        canvas.pack(fill=BOTH, expand=1)


root = Tk()
ex = SVGcurve(pts)  # convert i_pts to (x,y) tuple list
root.geometry("400x600+300+300")
root.mainloop()