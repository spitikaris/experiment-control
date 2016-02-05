import os

class photoframe:
    corner = [1100,1140]
    offset = 0
    width = 0
    height = 0
    tileNo = 0
    tileWidth = 0
    tileHeight = 0

    def __init__(self, exp, tileNumber):
        self.width = int(exp.width_cm *10/0.198)
        self.height = int(exp.height_cm *10/0.238)
        self.tileNo = tileNumber

    def points_in_x(self):
        self.tileWidth = int(self.width/self.tileNo)
        thelist = range(self.corner[0]-int(self.tileWidth/2),self.corner[0]-self.width, -self.tileWidth)
        print thelist
        return thelist

    def points_in_y(self):
        self.tileHeight = int(self.height/self.tileNo)
        thelist = range(self.corner[1]-int(self.tileHeight/2),self.corner[1]-self.height, -self.tileHeight)
        print thelist
        return thelist


    def define_rect(self,exp):
        self.width = int(exp.width_cm *10/0.198)
        self.height = int(exp.height_cm *10/0.238)


def experimentGrapper():
    expName = raw_input("Enter name of experiment: ")
    myexp = experiment(expName)
    myexp.width_cm = input("Enter width of experiment: ")
    myexp.height_cm = input("Enter height of experiment: ")
    return myexp

def saveSetup(experiment):
    	s = open(experiment.name + '/setup.ini', 'w')
    	s.write('sidelength1='+str(experiment.width_cm))
    	s.write('sidelength2='+str(experiment.height_cm))
    	s.write('totalSteps='+str(experiment.totalSteps()))
    	s.write('amount_of_steps='+str(experiment.no_steps))
    	s.close()

class experiment:
    def __init__(self, name):
        self.name = name
        os.system("mkdir " + self.name)
    def photoPrefix(self):
        return self.name+"/"+self.name

    def totalSteps(self):
        return self.steplength * self.no_steps
    height_cm = 0
    width_cm = 0
    steplength = 0
    no_steps = 0
    stepsPerCm = 1000


    name = ""

class bcolors:
    HEADER = '\033[95m'
    SEND = '\033[94m'
    RECEIVE = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
