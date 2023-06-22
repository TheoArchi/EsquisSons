"""EsquisSons Built Environment allows to transform geometries into envirronment for the sonic sketch.
You can connect multiple brep to one component. Avoid flat surfaces.
-
AAU / Theo Marchal / BETA VERSION / AVRIL2020"""

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import Grasshopper.Kernel as gh


class BuiltEnvironment(component):

    def RunScript(self, environment_geo, _opacity, _abs_coef):

        # block init
        __author__ = "theomarchal"
        self.Params.Input[
            0].Description = "Built Environment : Use brep ; You can connect multiple brep, Avoid flat surfaces and meshes ;)"
        self.Params.Input[
            1].Description = "*Optional* Geometry acoustic opacity [Between 1 and 10]  (if none or 0, default = 4)"
        self.Params.Input[
            2].Description = "*Optional* Absorption coefficient of the geometry [Float number between 0.01 and 0.99] (if none = 0.4)"
        self.Params.Output[0].Description = "Environment representation"
        self.Params.Output[1].Description = "Environment object (plug it into EsquisSons MainEngine)"
        self.Name = "Built Environment"
        self.NickName = "Environment"
        self.Message = "EsquisSons V3"
        self.Category = "EsquisSons"
        self.SubCategory = "1/ Scene"

        # environment_geo check
        if environment_geo is None:
            self.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, 'You must link a geometry to environment_geo')
        if rs.IsMesh(environment_geo):
            self.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Error,
                                   "You cannot use meshes here... sorry about that, we'll figure it out !")

        # _opacity and _abs_coef default values
        if _opacity <= 0 or _opacity is None:
            _opacity = 4
        if _abs_coef <= 0 or _abs_coef is None:
            _abs_coef = 0.4

        # creation of an environment (as a list of list)
        geometry = [environment_geo, _opacity, _abs_coef]
        environment = [geometry]

        print
        environment

        environment_preview = environment_geo

        return (environment_preview, environment)