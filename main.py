import math
from units import *
from sympy.solvers import solve
from sympy import *
import tkinter as tk
from tkinter import *

root = tk.Tk()
root.geometry("+300+300")

formulas = {}
log = []
def selectFormula(formula):
    print(formula)
    if formula.get()!="Select a formula":
      userFormulaInterp(formula.get())


def showInfo(formula):
    global root, formulas
    if formula.get()!="Select a formula":
        infoWindow = tk.Toplevel(root)
        infoWindow.title("Formula Info")
        infoFrame = tk.Frame(master=infoWindow, relief=tk.FLAT, borderwidth=10)
        infoFrame.pack(side=tk.LEFT)
        formula = formulas[formula.get()]
        header = tk.Label(text=formula.name, master=infoFrame)
        header.pack()
        expression = tk.Label(text=formula.expression, master=infoFrame)
        expression.pack()
        desc = tk.Label(text=formula.description, master=infoFrame)
        desc.pack()
        variables = tk.Label(text="Variables: "+concatListToString(formula.variables), master=infoFrame)
        variables.pack()
        tk.Button(master=infoFrame, text="Back", command=infoWindow.destroy).pack()


def userFormulaInterp(formula):
    global root, formulas
    evalWindow = tk.Toplevel(root)
    evalWindow.title("Evaluate Formula")
    entryFrame = tk.Frame(master=evalWindow, relief=tk.FLAT, borderwidth=10)
    entryFrame.pack(side=tk.LEFT)
    header = tk.Label(text="Enter values for all but one of the variables", master=entryFrame)
    header.pack()
    formula = formulas[formula]
    entries = {} #these are user entered values
    for variable in formula.variables:
        label = tk.Label(text=variable, master=entryFrame)
        entry = tk.Entry(width=20, bg="white", fg="black", master=entryFrame)
        entries[variable] = entry
        label.pack()
        entry.pack()
    tk.Button(master=entryFrame, text="Evaluate", command=lambda: evalFormula(entries,formula,evalWindow)).pack()
    tk.Button(master=entryFrame, text="Back", command=evalWindow.destroy).pack()


def evalFormula(entries,formula,evalWindow):
    global root
    #process entries. remove the ones that are empty
    values = {}
    for entry in entries.keys():
        if entries[entry].get() != "":
            values[entry] = entries[entry].get()
    resultFrame = tk.Frame(master=evalWindow, relief=tk.FLAT, borderwidth=10,width=100)
    resultFrame.pack(side=tk.RIGHT)
    val,solvingFor = formula.evaluate(values)
    #display the result on the root window
    log.append(solvingFor+": "+ str(val))
    result = tk.Label(text=solvingFor+": "+ str(val), master=resultFrame)
    result.pack(side=tk.BOTTOM)


#this is not in use, just an example from a previous project
def handleEnter(event):
    global numRanges, entry
    numRanges += 1
    global root, listFrame
    gridFrame = tk.Frame(master=listFrame, relief=tk.RAISED, borderwidth=1)
    pair = entry.get()
    ranges.append(pair)
    entry.delete(0,tk.END)
    gridFrame.grid(row=numRanges, column=0)
    label = tk.Button(master=gridFrame, text=pair, command=lambda: remove(gridFrame, pair))
    label.pack()

def formulaSelection(formulas):
    global root, value_inside
    root.title("Evaluate Formula")
    entryFrame = tk.Frame(master=root,relief=tk.FLAT,borderwidth=10)
    entryFrame.pack(side=tk.RIGHT,fill=BOTH,expand=True)
    buttonFrame = tk.Frame(master=root, relief=tk.FLAT, borderwidth=10)
    buttonFrame.pack(fill=BOTH)
    header = tk.Label(text="Choose a formula from the dropdown, then confirm selection or press info to see formula details", master=entryFrame)
    header.pack(fill=BOTH)
    options = formulas.keys()
    value_inside = tk.StringVar(entryFrame)
    value_inside.set("Select a formula")
    dropDown = tk.OptionMenu(entryFrame,value_inside, *options)
    dropDown.config(width=20,height=2)
    dropDown.pack(side=tk.LEFT)

    tk.Button(master=root, width=10, height=2, text="Select", command=lambda: selectFormula(value_inside)).pack(in_=buttonFrame)
    tk.Button(master=root, width=10, height=2, text="Info", command=lambda: showInfo(value_inside)).pack(in_=entryFrame,side=tk.LEFT)
    tk.Button(master=root, width=10, height=2, text="Quit", command=root.destroy).pack(in_=buttonFrame)

    listFrame = tk.Frame(master=root,relief=tk.RIDGE,borderwidth =1)
    listFrame.pack(side=tk.RIGHT)
    root.bind('<Return>', handleEnter)
    root.mainloop()

## Constants
constants = {
"L0" : 3*10^28, # base luminosity, W
"G" : 6.67*10**-9, # gravitational constant
"k" : 1.381*10**-23, # Boltzmann's constant
"h" : 6.626*10**-34, # Planck's constant
"stefanBoltzmann" : 5.67*10**-8,
"hubble" : 67.66, #hubble's constant, (km/s)/Mpc
"c" : 3*10**8, #m/s
"pi" : math.pi,
"earthMass" : 5.972*10**24, #kg
"earthRadius" : 6371000, #m
"sunMass" : Mass(1, "solar masses"), #kg
"sunRadius" : 6.957*10**8, #m
"AU" : Length(1.496*10**11,"m") #m
}

## ------

#mass, luminosity, radius, apparent mag, absolute mag, distance, temperature

def concatListToString(list):
    str = ""
    for item in list:
        str += item + " "
    return str[:-1]

def oddOneOut(values, pattern):
    for arg in pattern:
        if arg not in values.keys():
            return arg
    return None

class formula:
    def __init__(self, name, expression, description, variables):
        self.expression = self.formatExpression(expression)
        self.variables = variables
        self.name = name
        self.description = description
        self.symbols = symbols(concatListToString(variables))
    def formatExpression(self,expression):
        global constants
        split = expression.split(" ")
        value = ""
        for symb in split:
            if symb in constants.keys():
                value = expression.replace(symb, str(constants[symb]))
        return value
    def evaluate(self, values): #values is a dictionary of variables to values, containing one less entry than there are variables
        print("Evaluating",self.expression,"with",values)
        solvingFor = oddOneOut(values, self.variables)
        expr = solve(self.expression, solvingFor)[0]
        for arg in values.keys():
            expr = expr.subs(arg, values[arg])
        return expr.evalf(), solvingFor

#get absolute mag from apparent magnitude and distance in pc
def absMag(apparent,distance): #distance in parsecs
    return apparent - 5 * math.log(distance,10)+5

#get the luminosity ratio of two stars from their abs mags
def lumRatioAbsMag(M1,M2):
    return 10**((M1-M2)/-2.5)

def lumFromAbsMag(M):
    global L0
    return L0*10**(-M/2.5)

def absMagFromLum(L):
    global L0
    return -2.5*math.log((L/L0),10)

def gravForce(m1,m2,r):
    global G
    return G*m1*m2/(r**2)

def lumRadTemp(values): #values is a dict of {R:val,T:val,L:val} but with one missing value
    global stefanBoltzmann, pi
    expr = solve(4 * pi * R ** 2 * stefanBoltzmann * T ** 4 - L, L)[0]
    for arg in values.keys():
        expr = expr.subs(arg,values[arg])
    return expr

lum = formula("Stellar Luminosity","4 * pi * R ** 2 * stefanBoltzmann * T ** 4 - L", "Find one of radius, temperature, or luminosity from the other two", ["R","T","L"])
absoluteMag = formula("Absolute Magnitude","m - 5 * log(d,10)+5-M", "Find the absolute magnitude of a star given its apparent magnitude and distance", ["m","d","M"])

# print("eval",lum.evaluate({"R":6.957*10**8,"T":5778}))

formulas = {lum.name:lum,absoluteMag.name:absoluteMag}

formulaSelection(formulas)


# print("Temp:",lumRadTemp({T:5778,R:6.957*10**8}))

# print(absMag(0.01,1.35))
# print(lumFromAbsMag(absMag(0.01,1.35)))
# print(absMagFromLum(lumFromAbsMag(absMag(0.01,1.35))))
# print(absMag(0.61,161))
# print(lumRatioAbsMag(-5.42,4.83))



