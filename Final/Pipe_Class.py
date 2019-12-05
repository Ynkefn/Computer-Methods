import numpy as np
from scipy.optimize import fsolve

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from PipeDrawingClass import gl2D, gl2DText, gl2DCircle


class Node:
    def __init__(self):         # Node Class holds all node values
        self.name = []
        self.x = None
        self.y = None
        self.z = None
        self.plainPressure = None   #pressure of plain nodes
        self.rname = []           # putting ref node name in the same class as plain nodes
        self.rpressure = None       #pressure of ref nodes (known)

class PipeLink:
    def __init__(self):         # Pipe Class holds all pipe values
        self.name = None
        self.begNodeName = []
        self.endNodeName = []
        self.nodeBeg = None
        self.nodeEnd = None
        self.length = None
        self.diameter = None
        self.flow = None

class Source:
    def __init__(self):         # Source Class holds all source values
        self.inletNodeID = None
        self.outletNodeID = None
        self.sourceflow = []

class Reference:                # Reference Class holds all reference values
    def __init__(self):
        self.nodeID = None
        self.pressure = None

class Devices:                  # Devices Class holds all device values
    def __init__(self):
        self.deviceID = None
        self.begNodeID = None
        self.endNodeID = None

    def flowcalc(self, rho, mu, eps, g):
        """devices need to be able to calculate their own flow
           (unless we delete the calls to flowcalc below)"""

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
        self.count = 0
        self.length = 0
        self.diameter = 0
        self.flowsum = []
        self.flows = []

    #def nodeByID(self, ID):

    #def DeviceByID(self, ID):

    #def pumpByID(self, ID):

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
                        #thisnode.names = hold[i - 4]
                        self.node.append(thisnode)      # Append all values to the list into the Main Pipe Class

            if keyword == 'pipes':
                hold = []
                thispipe = PipeLink()
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
                        thisref = Node()       # Same as above
                        thisref.nodeID = hold[i-2]
                        thisref.pressure = hold[i-1]
                        self.ref_nodes.append(thisref)

                        ref = Reference()  # Same as above
                        ref.nodeID = hold[i - 2]
                        ref.pressure = hold[i - 1]
                        self.ref_nodes.append(ref)

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


    def AnalyzeFlowSystem(self, guesses = None, Q = None, deltaP = None, Pump = None):
        rho = self.density
        mu = self.viscosity
        eps = self.roughness
        g = self.gravity
        nodes = Node()
        thispipe = PipeLink()
        source = Source()
        errors = []

        def solver_eq(self,Q=None,guesses=None,deltap=None,pump=None):
            x = len(thispipe.diameter)
            if Q is not None:   #
                if x == 1:      #check for single pipe
                    L = thispipe.length[0]
                    D = thispipe.diameter[0]
                    dp = pipe_deltaP(Q, rho, mu, eps, g, L, D)
                    self.dp = []
                    self.dp.append(dp)
                    head = dp / (rho * g)
                    self.head = []  # reset values, only have append as an option for later, it may end up being used
                    self.head.append(head)
                    power = Q * dp
                    self.power = []
                    self.power.append(power)

        def equations(vals):
            for i in range(len(nodes.name)):
                nodes.plainPressure.append(vals[i])
                self.flowsum.append(0)

            for i in range(len(thispipe.begNodeName)):  #solve for dp in each pipe
                L = thispipe.length[i]
                D = thispipe.diameter[i]
                n1 = thispipe.begNodeName[i]
                n2 = thispipe.endNodeName[i]
                count = 0

                for j in nodes.rname:   #looking for ref nodes
                    if n1==j: p1=0      #and assigning their pressure

                for j in nodes.name:    #looking at normal nodes
                    if n1==j:           #if true we have one
                        p1=nodes.plainPressure[count]   #assign p1 for that pipe's pressure
                    count+=1

                for j in nodes.rname:
                    if n2==j: p2=0      #assign p2 if we have a ref node

                count = 0       #reset count for p2 assigning
                for j in nodes.name:
                    if n2==j:
                        p2=nodes.plainPressure[count]   #assign p2 if condtns met
                    count+=1

                dp = p2 - p1

                Q = pipe_flow(dp, rho, mu, eps, g, L, D)

                for j in range(len(nodes.name)):    #flow into node 1
                    a = nodes.name[j]
                    if a==n1: self.flowsum[j]+=Q

                for j in range(len(nodes.name)):    #flow into node 2
                    a = nodes.name[j]
                    if a==n2: self.flowsum[j]-=Q

                self.flows.append(Q)

                #devices
                #for d in range(len(deviceBegNode

                qguess = vals[-1]
                source.sourceflow = qguess
                for j in range(len(nodes.name)):
                    a = nodes.name[j]
                    if a == source.inletNodeID:         #if source inlet
                        self.flowsum[j] += qguess       #add our guess
                    if a == source.outletNodeID:        #if source outlet
                        self.flowsum[j] -= qguess       #subtract out guess

                for j in range(len(nodes.name)):
                    errors.append(self.flowsum[j])  #fill our error array

                if Q is not None:
                    errors.append(Q-qguess)     #improve our errors if Q is known

                return errors

        if guesses is None:
            nnodes = len(nodes.name)
            guesses = np.linspace(1, 10, nnodes)
            guesses = np.append(guesses, 3.85)

            #scales = np.ones_like(guesses)  # pressure guesses
            #scales[len(scales) - 1] = self.flow_unit_conv / self.press_unit_conv
        answer = fsolve(equations, guesses)
        errors = equations(answer)
        answer = fsolve(equations, answer)

        #while np.linalg.norm(errors) / len(errors) > 10e-13:
        #    answer = fsolve(equations, answer, diag=scales)
        #    errors = equations(answer)
        #self.errors = np.linalg.norm(errors) / len(errors)

        print(answer)
        return answer


            #for i in range(len(self.ref_nodes)):
             #   #put pressure guesses in ref nodes and start flowsum at 0
              #  self.ref_nodes[i].pressure = vals[i]    #set node pressures
               # self.ref_nodes[i].flowsum = 0           #set node flow to 0

            #for pipe in self.pipes:
                #use node pressures tp calculate pipeflows & update flowsums
    ### DELA HAS A FLOWCALC FUNCITON IN BOTH HIS PIPES AND DEVICES;
    ### IF WE WANNA USE THIS METHOD WE'LL HAVE TO ADD THEM TOO
             #   pipe.flowcalc(rho, mu, eps, g)  #calc flow using node pressures
              #  pipe.nodeEnd -= pipe.flow       #its possible this and the below line
               # pipe.nodeBeg += pipe.flow       #should be flipped

            #for dev in self.devices:
             #   dev.flowcalc(rho, mu, eps, g)   #calc flow using node pressures
              #  dev.node1.flowsum -= dev.flow   #flows out of node
               # dev.node2.flowsum += dev.flow   #flows into node

            #qguess = vals[len(vals)-1]      #supply flow is final unknown
            #self.sourceflow = qguess        #store it in sourceflow
            #self.source.inletNodeID.flowsum -= qguess  #subtracttt flow to source inlet node
            #errors = []     #error vector
            #for i in range(len(self.ref_nodes)):
            #    #append node flow errors (hopefully 0)
            #    errors.append(self.plain_nodes[i].flowsum)

            #if Q is not None:       #constant flow source checked
            #    errors.append(Q - qguess)
            #if deltaP is not None:  #constant pressure checked
            #    dp = self.source_node_flow_out.pressure - self.source_node_flow_in.pressure
            #    errors.append(dp - deltaP)
            #if Pump is not None:    #pump source checked
            #    myc = PumpData.self.cCoeff     #get coeffs

            #    pumpPressure = myc[0] + myc[1]*qguess + myc[2]*qguess**2 + myc[3]*qguess**3
            #    dp = self.source_node_flow_out.pressure - self.source_node_flow_in.pressure
            #    errors.append(dp - pumpPressure)
            #    pass
            #return errors

        nnodes = len(self.ref_nodes)

        #if guesses is None:
        #    guesses = np.linspace(1, 10, nnodes)*self.press_unit_conv
        #    guesses = np.append(guesses, self.flow_unit_conv)

        #scales = np.ones_like(guesses)      #pressure guesses
        #scales[len(scales)-1] = self.flow_unit_conv / self.press_unit_conv

        #answer = fsolve(solver_equations, guesses, diag=scales)
        #errors = solver_equations(answer)
        #while np.linalg.norm(errors) / len(errors) > 10e-13:
        #    answer = fsolve(solver_equations, answer, diag=scales)
        #    errors = solver_equations(answer)
        #self.errors = np.linalg.norm(errors) / len(errors)
        #return answer

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

    def Length(self):
        """This doesn't work for some reason but I'm trying to get this to display the lengths when the checkmark is clicked"""
        #pipe = PipeLink()
        #x1, y1, x2, y2 = None, None, None, None  # This draws source lines
        #for p in self.pipes:
            #x1 = p.nodeBeg.x  # Loop through all pipes and draw all pipes
            #y1 = p.nodeBeg.y
            #x2 = p.nodeEnd.x
            #y2 = p.nodeEnd.y
            #len = pipe.length
            #gl2DText(len, 1, 2)

#friction factor and stuff from Dela
def churchill(eps, D, Re):
    if Re < 0.01: return 0.1
    th1 = (-2.457*np.log((7/Re)**0.9 + 0.27*eps/D))**16
    th2 = (37530/Re)**16
    f = 8 * ((8/Re)**12 + (th1 + th2)**-1.5)**(1/12)
    return f

def pipe_deltaP(Q, rho, mu, eps, g, L, D):
    V = 4 * Q / np.pi / (D**2)
    Re = rho * abs(V) * D / mu
    f = churchill(eps, D, Re)
    dp = f * L * abs(V) * V * rho / (2*D)
    return dp

def pipe_flow(dp, rho, mu, eps, g, L, D):
    def rootfunc(Q):
        error = pipe_deltaP(Q, rho, mu, eps, g, L, D) - dp
        return error
    qguess = 1
    Q = fsolve(rootfunc, qguess)
    return float(Q)

def device_flow(dp, c0, c1, c2, c3):
    def rootfunc(Q):
        pressure = c0 + c1*Q + c2*Q**2 + c3*Q**3
        error = pressure - dp
        return error
    qguess = 1
    Q = fsolve(rootfunc, qguess)
    return float(Q)