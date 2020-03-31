"""EsquisSons Source allows you to define a sound source.
Give its position, its size, and the sound file to play :)
-
AAU / Theo Marchal / BETA VERSION / AVRIL2020"""

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class MyComponent(component):
    
    def RunScript(self, Source_Location, Source_Path, Source_Size, _OptSource):
        __author__ = "theomarchal"
        self.Params.Input[0].Description = "Location of the source (as a point -Default is set to 0,0,0 /Disabled for curve shapes in source options)"
        self.Params.Input[1].Description = "Path to the sound file (as a text)"
        self.Params.Input[2].Description = "Source Size (Amplitude Sphere radius - Default is set to 1)"
        self.Params.Input[3].Description = "*Optional* Source Options (From 'Source Options' component)"
        self.Params.Output[0].Description = "Source representation"
        self.Params.Output[1].Description = "Source Object"
        self.Name = "Sound Source"
        self.NickName = "Source" 
        self.Category = "EsquisSons"
        self.SubCategory = "1/ Scene"
        
        
        import rhinoscriptsyntax as rs
        import Grasshopper.Kernel as gh
        
        rem = gh.GH_RuntimeMessageLevel.Remark
        ero = gh.GH_RuntimeMessageLevel.Error
        war = gh.GH_RuntimeMessageLevel.Warning
        
        SL = Source_Location
        SP = Source_Path
        SpS = Source_Size
        Opt = _OptSource
        
        if SL is None:
            SL = rs.AddPoint(0,0,0)
        if SP is None or len(SP)==0 :
            SP = "NoSound"
            self.AddRuntimeMessage(war, 'Source need a sound to be played (Source_path input)- you can use built-in sound (EsquiSsons) for a start')
        if Opt is None or len(Opt)==0 :
            if SpS is None:
                SpS = 1
            Geo = rs.AddSphere(SL,SpS)
            SD = [SP,SL,SpS,0,0]
            Source = [SD]
            self.Message = "EsquisSons V3"
        else :
            if Opt[0][3] == 0 : 
                self.Message = "EsquisSons V3"
            else : 
                self.Message = "Randomly play source"
            if SpS is None:
                SpS = 1
            Geo = rs.AddSphere(SL,SpS)
            SD = [SP,SL,SpS,Opt[0][2],Opt[0][3]]
            Source = [SD]
            '''else :
                Curve = Opt[0][0]
                CrvPts = rs.DivideCurveEquidistant(Curve,(SpS*2),create_points=False,return_points=True)
                SL = []
                Geo=[]
                for point in CrvPts : SL.append(point)
                for point in SL : Geo.append(rs.AddSphere(point,SpS))
                SD = []
                for i in SL :
                    sSD =[SP,i,SpS,Opt[0][2],Opt[0][3]]
                    SD.append(sSD)
                    Source = SD
            '''
        print SD
        return (Geo, Source)
