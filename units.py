# define a class called "length" whose constructor takes a value in one of the following units: m, ft, miles, km, LY, pc, Mpc, AU, and has methods for each of the other units that return the value in that unit
class Length:
    def __init__(self, value, unit):
        if unit == 'm':
            self.m = value
        elif unit == 'ft':
            self.m = value*0.3048
        elif unit == 'miles':
            self.m = value*1609.34
        elif unit == 'km':
            self.m = value*1000
        elif unit == 'LY':
            self.m = value*9.461*10**15
        elif unit == 'pc':
            self.m = value*3.086*10**16
        elif unit == 'Mpc':
            self.m = value*3.086*10**19
        elif unit == 'AU':
            self.m = value*1.496*10**11
        else:
            raise Exception("Invalid unit")

    def m(self):
        return self.m

    def ft(self):
        return self.m/0.3048

    def miles(self):
        return self.m/1609.34

    def km(self):
        return self.m/1000

    def LY(self):
        return self.m/9.461*10**15

    def pc(self):
        return self.m/3.086*10**16

    def Mpc(self):
        return self.m/3.086*10**19

    def AU(self):
        return self.m/1.496*10**11

# define a class called "mass" whose constructor takes a value in one of the following units: kg, g, solar masses, and has methods for each of the other units that return the value in that unit

class Mass:
    def __init__(self, value, unit):
        if unit == 'kg':
            self.kg = value
        elif unit == 'g':
            self.kg = value/1000
        elif unit == 'solar masses':
            self.kg = value*1.989*10**30
        else:
            raise Exception("Invalid unit")

    def kg(self):
        return self.kg

    def g(self):
        return self.kg*1000

    def solarMasses(self):
        return self.kg/(1.989*10**30)

# define a class called "luminosity" whose constructor takes a value in one of the following units: W, solar luminosities, and has methods for each of the other units
