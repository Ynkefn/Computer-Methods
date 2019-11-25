import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from PipeDrawingClass import gl2D, gl2DText, gl2DCircle

class Node:
    def __init__(self):
        self.name = None
        self.x = None
        self.y = None
        self.z = None

class PipeLink:
    def __init__(self):
        self.name = None
        self.begNodeName = None
        self.endNodeName = None
        self.nodeBeg = None
        self.nodeEnd = None
        self.length = None
        self.diameter = None

class Source:
    def __init__(self):
        self.inletNodeID = None
        self.outletNodeID = None

class Reference:
    def __init__(self):
        self.nodeID = None
        self.pressure = None

class Devices:
    def __init__(self):
        self.deviceID = None
        self.begNodeID = None
        self.endNodeID = None

class PumpData:
    def __init__(self):
        self.pumpID = None
        self.description = None
        self.shutoff_head = None
        ######################## STOPPED HERE #######################
        # Need variables for coefficients still

class DeviceData:
    def __init__(self):
        ## NEED ALL VARIABLES STILL ##
        self.test = None

class Pipe:
    def __init__(self, ):
        self.title = None
        self.fund_dis_unit = None
        self.fund_force_unit = None
        self.fund_time_unit = None
        self.flow_unit = None
        self.flow_unit_conv = None
        self.press_unit = None
        self.press_unit_conv = None
        self.head_unit = None
        self.head_unit_conv = None
        self.gravity = None
        self.roughness = None
        self.density = None
        self.viscosity = None
        self.node = []
        self.pipes = []
        self.ref_nodes = []
        self.devices = []
        self.source = []
        self.pump_data = []
        self.device_data = []
        self.DrawingSize = None

    def ReadPipeData(self, data):
        for line in data:
            cells = line.strip().split(',')
            keyword = cells[0].lower()

            if keyword == 'title': self.title = cells[1].strip()
            if keyword == 'distance_unit': self.fund_dis_unit = cells[1].strip()
            if keyword == 'force_unit': self.fund_force_unit = cells[1].strip()
            if keyword == 'time_unit': self.fund_time_unit = cells[1].strip()
            if keyword == 'gravity': self.gravity = float(cells[1].strip())
            if keyword == 'roughness': self.roughness = float(cells[1].strip())
            if keyword == 'density': self.density = float(cells[1].strip())
            if keyword == 'viscosity': self.viscosity = float(cells[1].strip())

            if keyword == 'flow_unit':
                self.flow_unit = cells[1].strip()
                self.flow_unit_conv = float(cells[2].strip())

            if keyword == 'pressure_unit':
                self.press_unit = cells[1].strip()
                self.press_unit_conv = float(cells[2].strip())

            if keyword == 'head_unit':
                self.head_unit = cells[1].strip()
                self.head_unit_conv = float(cells[2].strip())

            if keyword == 'nodes':
                hold = []
                for cell in cells[1:]:
                    value = cell.replace("(", "").replace(")", "").strip()
                    hold.append(value)
                for i, j in enumerate(hold):
                    if i % 4 is 0:
                        thisnode = Node()
                        thisnode.z = float(hold[i-1])
                        thisnode.y = float(hold[i-2])
                        thisnode.x = float(hold[i-3])
                        thisnode.name = hold[i-4]
                        self.node.append(thisnode)

            if keyword == 'pipes':
                hold = []
                for cell in cells[1:]:
                    value = cell.replace("(", "").replace(")", "").strip()
                    hold.append(value)
                for i, j in enumerate(hold):
                    if i % 4 is 0:
                        thispipe = PipeLink()
                        thispipe.begNodeName = hold[i-4]
                        thispipe.endNodeName = hold[i-3]
                        thispipe.length = float(hold[i-2])
                        thispipe.diameter = float(hold[i-1])
                        self.pipes.append(thispipe)

            if keyword == 'source':
                thissource = Source()
                thissource.inletNodeID = cells[1].strip()
                thissource.outletNodeID = cells[2].strip()
                self.source.append(thissource)

            if keyword == 'ref_nodes':
                hold = []
                for cell in cells[1:]:
                    value = cell.replace("(", "").replace(")", "").strip()
                    hold.append(value)
                for i, j in enumerate(hold):
                    if i % 2 is 0:
                        thisref = Reference()
                        thisref.nodeID = hold[i-2]
                        thisref.pressure = hold[i-1]
                        self.ref_nodes.append(thisref)

            if keyword == 'devices':
                hold = []
                for cell in cells[1:]:
                    value = cell.replace("(", "").replace(")", "").strip()
                    hold.append(value)
                for i, j in enumerate(hold):
                    if i % 3 is 0:
                        thisdevice = Devices()
                        thisdevice.deviceID = hold[i-3]
                        thisdevice.begNodeID = hold[i-2]
                        thisdevice.endNodeID = hold[i-1]
                        self.devices.append(thisdevice)

        self.UpdateConnections()

    def UpdateConnections(self):
        xmin = 99999
        xmax = -99999
        ymin = 99999
        ymax = -99999

        for pipe in self.pipes:
            for node in self.node:
                if node.name == pipe.begNodeName:
                    pipe.nodeBeg = node
                if node.name == pipe.endNodeName:
                    pipe.nodeEnd = node
                if node.x <= xmin:
                    xmin = node.x
                if node.x >= xmax:
                    xmax = node.x
                if node.y <= ymin:
                    ymin = node.y
                if node.y >= ymax:
                    ymax = node.y

        self.DrawingSize = [xmin, xmax, ymin, ymax*1.25]

    def DrawPipePicture(self):
        x = 0
        y = 0

        for pipe in self.pipes:
            x1 = pipe.nodeBeg.x
            y1 = pipe.nodeBeg.y
            x2 = pipe.nodeEnd.x
            y2 = pipe.nodeEnd.y

            glColor3f(0, .75, 0)
            glLineWidth(2)
            glBegin(GL_LINE_STRIP)
            glVertex2f(x1, y1)
            glVertex2f(x2, y2)
            glEnd()

            glColor3f(0, 0, 0)
            name = pipe.begNodeName + pipe.endNodeName
            gl2DText(name, x1 + (x2-x1)/2, y1 + (y2-y1)/2)

        for node in self.node:
            red = False
            radius = (self.DrawingSize[1]-self.DrawingSize[0]) / 60
            for ref in self.ref_nodes:
                if ref.nodeID == node.name:
                    red = True

            if red is True:
                glColor(.75, 0, 0)
                gl2DCircle(node.x, node.y, radius, fill=True)
            else:
                glColor3f(0, .75, 0)
                gl2DCircle(node.x, node.y, radius, fill=True)

            glColor3f(0, 0, 0)
            gl2DText(node.name, node.x, node.y)
