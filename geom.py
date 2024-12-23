import copy
import shapely

class XY:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2


class Rect:
    def __init__(self, ll, ur):
        self.ll = ll
        self.ur = ur

    def move_by(self, x, y):
        r = copy.deepcopy(self)
        r.ll.x = self.ll.x + x
        r.ll.y = self.ll.y + y
        r.ur.x = self.ur.x + x
        r.ur.y = self.ur.y + y
        return r

    def width(self):
        return abs(self.ur.x - self.ll.x)

    def height(self):
        return abs(self.ur.y - self.ll.y)

    def center(self):
        return XY(self.ll.x + self.width() / 2, self.ll.y + self.height() / 2)

    def left(self):
        return self.ll.x

    def bottom(self):
        return self.ll.y

    def right(self):
        return self.ur.x

    def top(self):
        return self.ur.y

    def to_shapely_box (self):
        return shapely.box(self.left(), self.bottom(), self.right(), self.top())


def det_crosses(lines):
    total = max(len(lines), 1)
    already_has_cross = set()

    crosses = 0;
    for idx in range(total - 1):
        line1 = lines[idx]
        for jdx in range(idx + 1, total):
            line2 = lines[jdx]
            if line2 in already_has_cross:
                continue
            intersect = line1.intersects(line2)
            if intersect:
                crosses += 1
                already_has_cross.add(line2)

    total = max(total, 1)
    return total, crosses
