
"""Visualize Reflexion close to listener.
Use Visualize Output of "EsquisSons Main engine" :)
<WORKS ONLY WITH UNTRIMMED BREP OR SURFACES / You may encounter some bugs in semi-closed volumes>
-
AAU / Theo Marchal / BETA VERSION / MARS2020"""

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class MyComponent(component):
    
    def RunScript(self, Vi, NmbrOfRay, NmbrOfRef, Tolerance):
        
        __author__ = "theomarchal"
        self.Params.Input[0].Description = "Visualize (from esquissons main engine)"
        self.Params.Input[1].Description = "Definition/number of ray (1-100)<default=10>"
        self.Params.Input[2].Description = "Level of reflexion/number of bounces(1-10)<default=2>"
        self.Params.Input[3].Description = "Ray Distance to listener tolerance (0.1-1.0)<default=0.5>"
        self.Params.Output[0].Description = "Reflexion Rays"
        self.Name = "Visualize Reflections"
        self.NickName = "Visualize Rays" 
        self.Message = "EsquisSons V3"
        self.Category = "EsquisSons"
        self.SubCategory = "2/ Visualization"
        Def = NmbrOfRay
        Level = NmbrOfRef
        Dist = Tolerance
        import rhinoscriptsyntax as rs
        import Grasshopper.Kernel as gh
        
        rem = gh.GH_RuntimeMessageLevel.Remark
        ero = gh.GH_RuntimeMessageLevel.Error
        war = gh.GH_RuntimeMessageLevel.Warning
        
        
        if Def == None :
            Def = 10
        if Level == None :
            Level =2
        if Dist == None :
            Dist = 0.5
        try:
            Ge =Vi[0]
        except:
            self.AddRuntimeMessage(ero, 'A "Vi" ouptut from main engine must be connected !')
            raise Exception('noInput')
        Lis =Vi[1]
        Src =Vi[2]
        udiv = Def
        vdiv = Def
        Pt_L = Lis [0][0]
        Pt_R = Lis [0][2]
        srf = []
        FirstRay = []
        SecondRay = []
        First_RefPoint = []
        drawray =[]
        for i in Ge :
            srf.append(i[0])
        for i in Src :
            sph =(rs.AddSphere(i[1],i[2]))
            Src_pt =(i[1])
            u = rs.SurfaceDomain(sph,0)
            v = rs.SurfaceDomain(sph,1)
            pts = []
            for i in range(0, udiv+1, 1):
                for j in range(0, vdiv+1, 1):
                    pt = (i/udiv,j/vdiv,0)
                    sphP = rs.SurfaceParameter(sph,pt)
                    newpt = rs.EvaluateSurface(sph,sphP[0],sphP[1])
                    pts.append(rs.AddPoint(newpt))
            Dir = []
            for p in pts:
                Dir.append(rs.VectorCreate(p,Src_pt))
            Reflexion = []
            for d in Dir :
                Reflexion.append(rs.ShootRay(srf,Src_pt,d,reflections=Level))
            SourceRay = []
            for v in Reflexion :
                Cl_Pt = []
                Ray_v = []
                try :
                    Ray_v.append(rs.AddPolyline(v))
                except :
                    pass
                for u in Ray_v :
                    pt_on = rs.CurveClosestPoint (u,Pt_L)
                    cl = rs.EvaluateCurve(u,pt_on)
                    Dicl = (rs.Distance(Pt_L,cl))
                    if Dicl <= ((Lis [0])[3])*Dist:
                        try:
                            drawray.append(u)
                        except:
                            pass
        if len(drawray) == 0 :
            self.AddRuntimeMessage(war, 'No ray, please be sure Geometries are connected to main engine and placed to create reflexions')
            self.AddRuntimeMessage(war, 'Change parameters to generate more rays')
            Rays = None
        else : 
            Rays = drawray
        return Rays
