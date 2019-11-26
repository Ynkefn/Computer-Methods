import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from PipeDrawingClass import gl2D, gl2DText, gl2DCircle

class Node:
    def __init__(self):         # Node Class holds all node values
        self.name = None
        self.x = None
        self.y = None
        self.z = None

class PipeLink:
    def __init__(self):         # Pipe Class holds all pipe values
        self.name = None
        self.begNodeName = None
        self.endNodeName = None
        self.nodeBeg = None
        self.nodeEnd = None
        self.length = None
        self.diameter = None

class Source:
    def __init__(self):         # Source Class holds all source values
        self.inletNodeID = None
        self.outletNodeID = None

class Reference:                # Reference Class holds all reference values
    def __init__(self):
        self.nodeID = None
        self.pressure = None

class Devices:                  # Devices Class holds all device values
    def __init__(self):
        self.deviceID = None
        self.begNodeID = None
        self.endNodeID = None

class PumpData:
    def __init__(self):         # PumpData Class holds all pump_data values
        self.pumpID = None
        self.description = None
        self.shutoff_head = None
        self.cCoeff = []
        self.dCoeff = []

class DeviceData:               # DeviceData Class holds all device_data
    def __init__(self):
        self.deviceID = None
        self.description = None
        self.cCoeff = []

class Pipe:
    def __init__(self, ):       # Pipe class holds all usable values
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
        self.node = []                  # These lists is where the data from the classes above will be stored
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

            if keyword == 'title': self.title = cells[1].strip()        # Standard keyword single value stuff
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
                hold = []       # Declare empty list for holding values
                for cell in cells[1:]:       # Loop through all cells and remove spaces and parenthesis
                    value = cell.replace("(", "").replace(")", "").strip()
                    hold.append(value)       # Add every value to hold
                for i, j in enumerate(hold):    # Loop through hold using enumerate. i is the count (from enumerate)
                    if i % 4 is 0:              # j is the actual index
                        thisnode = Node()       # Check for every 4th value by using modulo.
                        thisnode.z = float(hold[i-1])   # thisnode = Node() creates an instance for Node
                        thisnode.y = float(hold[i-2])   # Fill every data value in Node with their respective value
                        thisnode.x = float(hold[i-3])
                        thisnode.name = hold[i-4]
                        self.node.append(thisnode)      # Append all values to the list into the Main Pipe Class

            if keyword == 'pipes':
                hold = []
                for cell in cells[1:]:                  # Exact same as above
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
                thissource = Source()               # More basic keyword readings
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
                        thisref = Reference()       # Same as above
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
                        thisdevice = Devices()      # Same same
                        thisdevice.deviceID = hold[i-3]
                        thisdevice.begNodeID = hold[i-2]
                        thisdevice.endNodeID = hold[i-1]
                        self.devices.append(thisdevice)

            if keyword == 'pump_data':
                thispData = PumpData()
                thispData.pumpID = cells[1].strip()     # This one is a little different. Basically the same concepts
                thispData.description = cells[2].strip()    # as above but I went through each cell and declared the
                thispData.shutoff_head = float(cells[3].strip())    # single values first. Then went on to the
                for i in cells[4:7]:                                # coefficients. Made lists for them and appended the
                    thispData.cCoeff.append(float(i))               # the values to them.
                for i in cells[8:11]:
                    thispData.dCoeff.append(float(i))
                self.pump_data.append(thispData)                    # Appended all data to main list in Pipe Class

            if keyword == 'device_data':
                thisdData = DeviceData()
                thisdData.deviceID = cells[1].strip()
                thisdData.description = cells[2].strip()
                for i in cells[3:6]:
                    thisdData.cCoeff.append(float(i))
                self.device_data.append(thisdData)

        self.UpdateConnections()

    def UpdateConnections(self):
        xmin = 99999
        xmax = -99999
        ymin = 99999
        ymax = -99999

        for pipe in self.pipes:             # Determine drawing size based off of max and min x and y values
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
        x1, y1, x2, y2 = None, None, None, None     # This draws source lines
        for source in self.source:                  # Initialize x and y values and loop through source and node
            for node in self.node:
                if source.inletNodeID == node.name:     # Check is inlet and outlet node for source equal node names
                    x1 = node.x                         # If they do, set x and y values to node values
                    y1 = node.y
                if source.outletNodeID == node.name:
                    x2 = node.x
                    y2 = node.y
                glColor3f(0, 0, 1)                      # Draw source line
                glLineWidth(2)
                glBegin(GL_LINE_STRIP)
                if x1 or y1 is not None:
                    glVertex2f(x1, y1)
                if x2 or y2 is not None:
                    glVertex2f(x2, y2)
                glEnd()

            glColor3f(0, 0, 0)
            name = source.inletNodeID + source.outletNodeID
            gl2DText(name, x1 + (x2-x1)/2, y1 + (y2-y1)/2)

        for device in self.devices:
            x1, x2, y1, y2 = None, None, None, None
            for node in self.node:
                if device.begNodeID == node.name:       # Same as above but for devices
                    x1 = int(node.x)
                    y1 = int(node.y)
                if device.endNodeID == node.name:
                    x2 = int(node.x)
                    y2 = int(node.y)
                glColor3f(0, 0, 0)
                glLineWidth(2)
                glBegin(GL_LINE_STRIP)
                if x1 and y1 is not None:
                    glVertex2f(x1, y1)
                if x2 and y2 is not None:
                    glVertex2f(x2, y2)
                glEnd()

        for pipe in self.pipes:
            x1 = pipe.nodeBeg.x             # Loop through all pipes and draw all pipes
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
            red = False                         # Draw all nodes. Including reference nodes.
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
