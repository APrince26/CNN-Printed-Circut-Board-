# in the spirit of lef/def and verilog
# https://coriolis.lip6.fr/doc/lefdef/lefdefref/lefdefref.pdf

import shapely


class DB:
    def __init__(self, name):
        self.name = name
        self.macros = list()
        self.devices = list()
        self.connections = list()
        self.die = None

    def set_top_macro(self, macro):
        self.die = macro

    def add_macro(self, macro):
        self.macros.append(macro)

    def add_device(self, device):
        self.devices.append(device)

    def add_connection(self, connection):
        self.connections.append(connection)


class Net:
    def __init__(self, name, macro):
        self.name = name
        macro.nets.append(self)


class Pin:
    def __init__(self, name, rect):
        self.name = name
        self.rect = rect


class Macro:
    def __init__(self, name, children, rect, pins):
        self.children = list()
        self.name = name
        self.rect = rect
        self.pins = pins
        self.nets = None
        self.nets = list()

    def add_child(self, child):
        self.children.add(child)

    def get_pin_by_name(self, name):
        for p in self.pins:
            if p.name == name:
                return p
        return None


class Component:
    def __init__(self, name, macro, loc, parent):
        self.name = name
        self.macro = macro
        self.loc = loc
        self.parent = parent
        parent.children.append(self)
        self.parent_net_map = {}


    def set_net(self, template_pin, net):
        self.parent_net_map.update({net: template_pin})




class Connection:
    def __init__(self, c0, c1, p0, p1):
        self.c0 = c0
        self.c1 = c1
        self.p0 = p0
        self.p1 = p1
        r0 = p0.rect.move_by(c0.loc.x, c0.loc.y)
        r1 = p1.rect.move_by(c1.loc.x, c1.loc.y)
        xy0 = r0.center()
        xy1 = r1.center()
        self.line = shapely.LineString([(xy0.x, xy0.y), (xy1.x, xy1.y)])
