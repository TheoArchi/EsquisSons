
"""EsquisSons Built Environment allows to transform geometries into envirronment for the sonic sketch.
You can connect multiple brep to one component, Avoid flat surfaces. 
-
AAU / Theo Marchal / BETA VERSION / AVRIL2020"""

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class MyComponent(component):
    
    def RunScript(self, Geo, _Opacity, _AbsCoef):
        
        
        __author__ = "theomarchal"
        self.Params.Input[0].Description = "Built Environment : Use brep ; You can connect multiple brep, Avoid flat surfaces and meshes ;)"
        self.Params.Input[1].Description = "*optional* Geometry acoustic opacity [Btw 1 and 10]  (if none or 0 default = 4)"
        self.Params.Input[2].Description =  "*optional* Absorption Coefficient of the geometry [Float number btw 0.01 and 0.99] (if none = 0.4)"
        self.Params.Output[0].Description = "Built environment representation"
        self.Params.Output[1].Description = "Built environment as a geometry object"
        self.Name = "Built Environment"
        self.NickName = "Environment"
        self.Message = "EsquisSons V3"
        self.Category = "EsquisSons"
        self.SubCategory = "1/ Scene"
        
        import Grasshopper.Kernel as gh
        import rhinoscriptsyntax as rs
        
        rem = gh.GH_RuntimeMessageLevel.Remark
        ero = gh.GH_RuntimeMessageLevel.Error
        war = gh.GH_RuntimeMessageLevel.Warning
        
        if Geo is None :
            self.AddRuntimeMessage(war, 'You must provide a geometry')
        
        if rs.IsMesh(Geo):
            self.AddRuntimeMessage(ero, "You cannot use meshes here... sorry about that we'll figure it out !")
        Preview = Geo
        if _Opacity <= 0 :
            _Opacity = 4
        if _AbsCoef <= 0 :
            _AbsCoef = 0.4
        Geo_Obj = [Geo,_Opacity,_AbsCoef]
        Geometry=[Geo_Obj]
        print Geometry
        return (Preview, Geometry)
