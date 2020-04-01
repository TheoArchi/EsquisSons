"""EsquisSons Listener is used to declare the listening point.
Define its position, orientation and size :)
-
AAU / Theo Marchal / BETA VERSION / AVRIL2020"""

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class MyComponent(component):
    
    def RunScript(self, Listener_Location, Direction, Height):
        
        __author__ = "theomarchal"
        self.Params.Input[0].Description = "Location of the listener foots (as a point - Default is set to 0,0,0)"
        self.Params.Input[1].Description = "Direction of the listener (in degrees from 0 to 360)"
        self.Params.Input[2].Description = "How tall is the listener (default = 1.80)"
        self.Params.Output[0].Description = "Listener Geometry, size and direction"
        self.Params.Output[1].Description = "Listener Object (plug it into EsquisSons)"
        self.Name = "Listener Point"
        self.NickName = "Listener"
        self.Message = "EsquisSons V3"
        self.Category = "EsquisSons"
        self.SubCategory = "1/ Scene"
                
                
        import rhinoscriptsyntax as rs
                
        LL = Listener_Location
        LD = Direction
        LH = Height
                
        if LL is None:
            LL = rs.AddPoint(0,0,0)
        if LD is None:
            LD = 0
        if LH is None:
            LH = 1.8
                
        LV = rs.VectorRotate([0,(LH),0],LD,[0,0,1])
        matrix = rs.XformTranslation((0,0,LH))
        LHp = rs.PointTransform(LL,matrix)
        LV2 = rs.VectorScale((rs.VectorRotate(LV,90,[0,0,1])),0.5)
        LV3 = rs.VectorScale((rs.VectorRotate(LV,-90,[0,0,1])),0.5)
        T1 = rs.PointTransform(LL,(rs.XformTranslation(LV)))
        Tl = rs.PointTransform(LL,(rs.XformTranslation(LV2)))
        Tr = rs.PointTransform(LL,(rs.XformTranslation(LV3)))
        ps=[T1,Tl,Tr]
        Geo = [rs.AddSphere(LHp,(LH/10)),rs.AddLine(LL,LHp),rs.AddSrfPt(ps)]
        Tl = rs.PointTransform(Tl,matrix)
        Tr = rs.PointTransform(Tr,matrix)
        LP = [LHp,Tl,Tr,LH]
        Listener = [LP]
        return (Geo, Listener)
