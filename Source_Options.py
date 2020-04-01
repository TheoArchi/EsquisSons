"""EsquisSons Source Options allows you to more precisely define a source (shuffle, volume, mute etc.)
-
AAU / Theo Marchal / BETA VERSION / AVRIL2020"""

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class MyComponent(component):
    
    def RunScript(self, Source_On, RandomizeSource, Manual_Volume_1_100):
        
        __author__ = "theomarchal"
        self.Params.Input[0].Description = "Mute the source if set to False (use boolean here)"
        self.Params.Input[1].Description = "Set chance of playing the source (1/x chance where x is the input)(Int input, if none the source is continuously looped)"
        self.Params.Input[2].Description = "Manual Volume from 1 to 100 (disengage the mainengine calculation for volume if connected - not active if volume is set to 0)"
        self.Params.Output[0].Description = "Source options (connect to Source component)"
        self.Name = "Source options"
        self.NickName = "Source_Opt" 
        self.Message = "EsquisSons V3"
        self.Category = "EsquisSons"
        self.SubCategory = "2/ Option"
        
        
        import rhinoscriptsyntax as rs
        import math
        Son = Source_On
        Mvol = Manual_Volume_1_100
        rdm = RandomizeSource
        
        if Mvol is None :
            Mvol = 0
        if Mvol>100:
            Mvol=100
        if Mvol<0:
            Mvol=0
        if Mvol != 0:
            Mvol = ((10*math.log10(1+Mvol)))
            Mvol = 3.49*Mvol
        if Son is None :
            Son = True
        if Son is False :
            Mvol = 1
        
        if rdm is None :
            rdm = 0
        if rdm == 1 :
            rdm = 0
        
        OptionSource = ['None',Son,Mvol,rdm]
        OptSource = [OptionSource]
        return OptSource
