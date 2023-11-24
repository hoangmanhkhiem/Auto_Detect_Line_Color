from math import ceil
import math
from svgpathtools import svg2paths2
import numpy as np
import webcolors
import re
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

color = []
Points = []
DATA = []


class TwoPointsWithDistance:
    def __init__(self, point1, point2,distancee):
        self.point1 = point1
        self.point2 = point2
        self.distance = distancee


class Info:
    def __init__(self, point1, point2,name):
        self.point1 = point1
        self.point2 = point2
        self.name = name
        self.nd = str(name) + " " + str(point1) + " " + str(point2) + "\n"


def read_svg(path):
    paths, attrs, svg_attr = svg2paths2(path)
    svg_size = (float(svg_attr['width'].replace('px', '')),
                float(svg_attr['height'].replace('px', '')))
    viewbox = [float(f) for f in svg_attr['viewBox'].split(' ')]

    polys = []
    for path in paths:
        poly = []
        for subpaths in path.continuous_subpaths():
            points = []
            for seg in subpaths:
                if seg.length() == math.inf * (-1) or seg.length() == math.inf:
                    break
                interp_num = ceil(seg.length() / 8)
                points.append(seg.point(np.arange(interp_num) / interp_num))
            points = np.concatenate(points)
            points = np.append(points, points[0])
            poly.append(points)
        polys.append([[(p.real, p.imag) for p in pl] for pl in poly])
    return (polys, attrs, svg_size, viewbox)


def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def max_distance_between_points(poly):
    max_distance = 0
    max_distance_points = None
    for i in range(len(poly) - 1):
        for j in range(i + 1, len(poly)):
            dist = distance(poly[i], poly[j])
            if dist > max_distance:
                max_distance = dist
                max_distance_points = (poly[i], poly[j])
    point1, point2 = max_distance_points
    Points.append(TwoPointsWithDistance(point1,point2,max_distance))


def searching_code(color):
    listtt = []
    data = []
    for color_code in color:
        # Convert hex to RGB
        rgb = webcolors.hex_to_rgb(color_code)
        data.append(str(rgb))
    for line in data:
        match = re.search(r'red=(\d+), green=(\d+), blue=(\d+)', line)
        if match:
            red = int(match.group(1))
            green = int(match.group(2))
            blue = int(match.group(3))
            listtt.append(int(red)-int(green)-int(blue))
    value = max(listtt)
    indx = listtt.index(value)
    return indx


def draw_multipolygon(mpoly, fill):
    red = color[searching_code(color)]
    if fill == red:
        # print(fill)
        for i, poly in enumerate(mpoly):
            max_distance_between_points(poly)


def main():
    path_root = "D:\\svg\\"
    for i in range(6):
        print("Da chay xong tep thu {}".format(i+1))
        fileName = "neg_" + str(i) + ".svg"
        path = path_root + fileName
        if path is None:
            raise Exception("Could not file")
        if read_svg(path) is not None:
            polys, attrs, svg_size, viewbox = read_svg(path)
    
            for poly, attr in zip(polys, attrs):
                if 'style' in attr.keys():
                    attr.update({attrs.split(':')[0]: attrs.split(':')[1] for attrs in attr['style'].split(';')})
                if 'stroke' not in attr.keys():
                    attr['stroke'] = attr['fill']
                if 'fill' in attr.keys():
                    if attr['fill'] not in color:
                        color.append(attr['fill'])
            for poly, attr in zip(polys, attrs):
                if 'fill' in attr.keys():
                    draw_multipolygon(poly, fill=attr['fill'])
            maxx_diss = 0
            _x = 0
            _y = 0
            for pr in Points:
                if maxx_diss < pr.distance:
                    maxx_diss = pr.distance
                    _x = pr.point1
                    _y = pr.point2
            name = "neg_" + str(i) + ".jpg"
            DATA.append(Info(_x,_y,name))
            color.clear()
            Points.clear()
        else:
            DATA.append(Info(None,None,None))
    with open("output.txt","w") as f:
        for x in DATA:
            a = str(x.nd)
            characters_to_remove = "(),"
            new_string = a
            for char in characters_to_remove:
                new_string = new_string.replace(char, "")
            f.writelines(new_string)


if __name__ == '__main__':
    main()
