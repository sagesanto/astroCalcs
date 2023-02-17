import math
from units import *
from sympy.solvers import solve
from sympy import *
import tkinter as tk
from tkinter import *

root = tk.Tk()

formulas = {}

def selectFormula(formula):
    userFormulaInterp(formula.get())

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
    tk.Button(master=entryFrame, text="Evaluate", command=lambda: evalFormula(entries,formula)).pack()

def evalFormula(entries,formula):
    global root
    #process entries. remove the ones that are empty
    values = {}
    for entry in entries.keys():
        if entries[entry].get() != "":
            values[entry] = entries[entry].get()

    val,solvingFor = formula.evaluate(values)
    #display the result on the root window

    result = tk.Label(text=solvingFor+": "+ str(val))
    result.pack()

def done():
    global root
    root.withdraw()
    userRadiusInterp()

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
    entryFrame.pack(side=tk.LEFT)
    header = tk.Label(text="Choose a formula from the dropdown, then confirm selection", master=entryFrame)
    header.pack()
    options = formulas.keys()
    value_inside = tk.StringVar(entryFrame)
    value_inside.set("Select a formula")
    dropDown = tk.OptionMenu(entryFrame, value_inside, *options)
    dropDown.pack()
    # entry = tk.Entry(width=20, bg="white", fg="black",master=entryFrame)
    # entry.pack()
    tk.Button(master=entryFrame, text="Select", command=lambda: selectFormula(value_inside)).pack()
    tk.Button(master=entryFrame, text="Quit", command=root.destroy).pack()
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
        for symb in split:
            if symb in constants.keys():
                expression = expression.replace(symb, str(constants[symb]))
        return expression
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

lum = formula("Stellar Luminosity","4 * pi * R ** 2 * stefanBoltzmann * T ** 4 - L", "Find one of radius, temperature, or temperature from the other two", ["R","T","L"])
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



