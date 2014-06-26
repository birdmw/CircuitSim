import math
import matplotlib.pyplot as plt

class node:
    def __init__(self, voltage):
        self.V = voltage
        self.inbox = 0

    def update(self):
        self.V = self.V + self.inbox
        self.inbox = 0

class inductor:
    def __init__(self, L, node1, node2):

        self.node1 = node1
        self.node2 = node2
        
        self.L = L
        
        self.prevTime = globalTime
        self.dt = globalTime - self.prevTime

        self.Iprev = 0
        self.I = 0
        self.dI = self.I - self.Iprev

        self.Vprev = node2.V - node1.V
        self.V = node2.V - node1.V
        self.dV = self.V - self.Vprev

    def update(self):
        if (self.prevTime < globalTime):

            self.dt = globalTime - self.prevTime
            self.prevTime = globalTime
            self.Vprev = self.V
            self.Iprev = self.I
            
            self.V = self.node2.V - self.node1.V
            self.dV = self.V - self.Vprev

            self.I = self.Iprev + self.V / self.dt / self.L #* (1.602176565*10**-19)
            self.dI = self.I - self.Iprev

            self.node1.inbox += self.I
            self.node2.inbox -= self.I

class capacitor:
    def __init__(self, C, node1, node2):

        self.node1 = node1
        self.node2 = node2
        
        self.C = C
        
        self.prevTime = globalTime
        self.dt = globalTime - self.prevTime

        self.Vprev = node2.V - node1.V
        self.V = node2.V - node1.V
        self.dV = self.V - self.Vprev

        self.Iprev = 0
        self.I = 0
        self.dI = self.I - self.Iprev

    def update(self):
        if (self.prevTime < globalTime):
            
            self.dt = globalTime - self.prevTime

            self.prevTime = globalTime
            self.Iprev = self.I
            self.Vprev = self.V

            self.V = self.node2.V - self.node1.V
            self.dV = self.V - self.Vprev
                        
            self.I = self.C * self.dV / self.dt #* (1.602176565*10**-19)
           # print self.dV
            self.dI = self.I - self.Iprev

            self.node1.inbox -= self.I
            self.node2.inbox += self.I

class resistor:
    def __init__(self, R, node1, node2):

        self.node1 = node1
        self.node2 = node2
        
        self.R = R
        
        self.prevTime = globalTime
        self.dt = globalTime - self.prevTime

        self.Vprev = node2.V - node1.V
        self.V = node2.V - node1.V
        self.dV = self.V - self.Vprev

        self.Iprev = 0
        self.I = 0
        self.dI = self.I - self.Iprev

    def update(self):
        if (self.prevTime < globalTime):

            self.dt = globalTime - self.prevTime
            self.prevTime = globalTime
            self.Iprev = self.I
            self.Vprev = self.V

            self.V = self.node2.V - self.node1.V
            self.dV = self.V - self.Vprev
                        
            self.I = self.V / self.R #* (1.602176565*10**-19)
            self.dI = self.I - self.Iprev

            self.node1.inbox += self.I
            self.node2.inbox -= self.I
        

globalTime = 0
timeStep = 10**(-7) #-3 mS, -6 uS, -9 nS, -12 pS, -15 fS, -18 aS
stopTime = 30000*timeStep


nodes = list()
for i in range(4):
    nodes.append( node(0))

inductor1 = inductor(.0000001, nodes[2], nodes[3])
capacitor1 = capacitor(0.00000005,nodes[0],nodes[1])
resistor1 = resistor(10000,nodes[1],nodes[2])

sF = 8000 # Hz

InputNode = list()
OutputNode = list()


while globalTime < stopTime:
    globalTime = globalTime + timeStep
    
    for n in nodes:
        n.update()

    capacitor1.update()
    resistor1.update()
    
    if (globalTime < stopTime/2):
        nodes[0].V=5*math.sin(2*math.pi*sF*globalTime)

    if (globalTime > stopTime/2):
        nodes[0].V=-5

    if (globalTime > stopTime*3/4):
        nodes[0].V=-2
        
    nodes[2].V=0


    InputNode.append(nodes[0].V)
    OutputNode.append(nodes[1].V)

print max(OutputNode[:len(OutputNode)/2])

plt.plot(OutputNode)
plt.plot(InputNode)
plt.ylabel('Voltage')
plt.show()
