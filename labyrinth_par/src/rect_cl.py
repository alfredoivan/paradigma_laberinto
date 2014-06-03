# -*- coding: utf-8 -*-

#Rectangle class: to handle areas and point contains easily and cleanly.
class Rectangle:
    
    def __init__(self, xinicial = 1, xfinal = 1, yinicial=1, yfinal=1):
        self.__xinicial = xinicial
        self.__xfinal = xfinal
        self.__yinicial = yinicial
        self.__yfinal = yfinal
    ##Setters to float
    ##Getters
    #def get_length(self):
    #    return self.__length
    #def get_width(self):
    #    return self.__width
    ##Get perimeter and area
    def contains(self,xobj=1, yobj=1):
        #contains a given point
        if (xobj > self.__xinicial and xobj < self.__xfinal):
            if (yobj > self.__yinicial and yobj < self.__yfinal):
                return True
        return False
    #def area(self):
    #    return self.__length * self.__width