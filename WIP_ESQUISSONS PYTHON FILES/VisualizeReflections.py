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
import Grasshopper.Kernel as gh


class VisualizeReflections(component):

    def RunScript(self, visualization, _nb_rays, _nb_reflections, _tolerance_dist):

        # block init
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

        # set default values
        if _nb_rays == None:
            _nb_rays = 10
        if _nb_reflections == None:
            _nb_reflections = 2
        if _tolerance_dist == None:
            _tolerance_dist = 0.5

        # check visualization and get environment, listener and sources back from visualization
        try:
            environment = visualization[0]
            listener = visualization[1]
            sources = visualization[2]
        except:
            self.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Error,
                                   'A "visualization" ouptut from main engine must be connected !')
            raise Exception('noInput')

        # get listener_head and environment_geo back
        # - listener_head : point representing the head of the listener
        # - environment_geo : rhinoceros breps forming a listening environment
        listener_head = listener[0][0]
        environment_geo = []
        for geometry in environment:
            environment_geo.append(geometry[0])

        # calculation of rays for every sound_source
        # - rays : list of the reflection rays
        rays = []

        for sound_source in sources:
            # creation of a sphere from source location and size
            # - sphere_srf : sphere representing the sound_source
            source_location = (sound_source[1])
            sphere_srf = (rs.AddSphere(source_location, sound_source[2]))

            for i in range(0, _nb_rays + 1, 1):
                for j in range(0, _nb_rays + 1, 1):

                    # divide sphere into a point_list
                    # - pt : point created from _nb_rays, to later divide the sphere_srf
                    # - sphere_parameter : parameter of the sphere_srf locating a point created from pt on the sphere_srf
                    # - new_pt : point obtained from the previous sphere_parameter
                    # - pt_ray : point used to form rays (point on the sphere_srf used to divide it into _nb_rays*nb_rays parts)
                    pt = (i / _nb_rays, j / _nb_rays, 0)
                    sphere_parameter = rs.SurfaceParameter(sphere_srf, pt)
                    new_pt = rs.EvaluateSurface(sphere_srf, sphere_parameter[0], sphere_parameter[1])
                    pt_ray = rs.AddPoint(new_pt)

                    # creation of a vector used to guide the rays
                    # - ray_vect : vector going from new_pt to source_location (radius of the source sphere)
                    ray_vect = rs.VectorCreate(pt_ray, source_location)

                    # calculation of the points where reflection occurs on environment_geo for ray_vect
                    # the number of reflection calculated is _nb_reflections
                    # - reflection_points : list of the reflection points calculated
                    reflection_points = rs.ShootRay(environment_geo, source_location, ray_vect,
                                                    reflections=_nb_reflections)

                    # creation of a polyline representing the reflection ray (calculated from reflection_points)
                    # - reflection_rays : polyline of reflection rays
                    try:
                        reflection_rays = rs.AddPolyline(reflection_points)
                    except:
                        pass

                    # take into consideration tolerance_dist for each ray of reflection_rays
                    # - closest_pt_listener_par : parameter locating the closest point from listener_head on the ray
                    # - closest_pt_listener : point obtained from closest_pt_listener_par
                    # - dist_rays_listener : distance between each ray and listener
                    closest_pt_listener_par = rs.CurveClosestPoint(reflection_rays, listener_head)
                    closest_pt_listener = rs.EvaluateCurve(reflection_rays, closest_pt_listener_par)
                    dist_rays_listener = (rs.Distance(listener_head, closest_pt_listener))

                    # if the distance between ray and listener is lower than listener_height*_tolerance_dist
                    # the ray is added to rays
                    # - rays : list of every ray respecting the _tolerance_dist criteria
                    if dist_rays_listener <= ((listener[0])[3]) * _tolerance_dist:
                        try:
                            rays.append(reflection_rays)
                        except:
                            pass

        # check rays and display warning if there is no ray
        if len(rays) == 0:
            self.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning,
                                   'No ray, please be sure environment is connected to main engine and placed to create reflexions')
            self.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, 'Change parameters to generate more rays')

        return rays