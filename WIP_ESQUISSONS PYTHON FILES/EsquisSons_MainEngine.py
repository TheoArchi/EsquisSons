"""EsquisSons Main Engine will calculate the auralisation.
Use Listener, Sources and Geometry objects to connect them here :)
-
AAU / Theo Marchal / BETA VERSION / MARS2020
With the Contribution of Manon COUTIER & Domitille GRANDJEAN"""

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import math
import OSC
import Grasshopper.Kernel as gh


class EsquissonsMainEngine(component):

    def RunScript(self, listener, sources, environment, _reverb_on, _lock, _indoor):

        # bloc init
        __author__ = "theomarchal"
        self.Params.Input[0].Description = "Listener Object (Use Esquissons_Listener component)"
        self.Params.Input[1].Description = "Sources Objects (Use Esquissons_Source component)"
        self.Params.Input[2].Description = "Built environment (Use Esquissons_Built Environment component)"
        self.Params.Input[
            3].Description = "Set Reverb_On to True to activate Reverberation (Boolean input)(default is off)"
        self.Params.Input[
            4].Description = "To Lock sources (and sound), set to True, then turn it back to False (Boolean input)(default is unlock)"
        self.Params.Input[
            5].Description = "*Optionnal* Set to 'True' if your scene is indoors, otherwise leave the field empty (Boolean input)(default is outdoor)"
        self.Params.Output[0].Description = "Visualize output (plug it in visualize components to see rays)"
        self.Params.Output[1].Description = "Reverberation time (in second / for each source)"
        self.Params.Output[2].Description = "Reverberation Info (Time and mix / for each source)"

        self.Name = "EsquisSons Main engine"
        self.NickName = "EsquisSons"
        self.Message = "EsquisSons V3.01"
        self.Category = "EsquisSons"
        self.SubCategory = "0/ EsquisSons"

        # check if there is a listener
        # - listener_head : point which represent the head of the listener
        # - listener_height : height of the listener
        try:
            listener_head = ((listener[0])[0])
            listener_height = ((listener[0])[3])
        except:
            self.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Error,
                                   'You must connect a listener component (EsquisSons) !')
            raise Exception('nolistener')

        # check if there are sources
        if len(sources) <= 0:
            self.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning,
                                   'You must connect at least one Source component (EsquisSons)')

        # check if there is an environment
        if len(environment) <= 0:
            self.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning,
                                   'You must connect at least one Geometry component (EsquisSons)')

        # init the reverberation factor regarding if the scene is indoor or not
        if _indoor is True:
            indoor_factor = 1.0
        else:
            indoor_factor = 1.5

        # This function calculates the proportion of sound to be sent to the left and to the right
        # We draw a line between triangle_left and triangle_right and the source, and we make the difference between the two distances
        # It gives a panoramic value on a potentiometer (which goes from 0 to 127)
        def panoramic(listener, source_location):
            triangle_left = ((listener[0])[1])
            triangle_right = ((listener[0])[2])
            listener_height = ((listener[0])[3])
            panoramic_value = (((rs.Distance(triangle_left, source_location)) - (
                rs.Distance(triangle_right, source_location)) + listener_height) * (127 / (2 * listener_height)))
            return panoramic_value;

        # This function calculates the impact of the distance on the sound
        # - distance_weighted : scale factor in relation to the height of the listener
        # - sound_attenuation : sound intensity in decibel of sound attenuation with distance
        # - high_cut_frequency : high frequency filter with distance (cut-off frequency)
        def impact_distance(height, distance):
            distance_weighted = (distance * 1.8) / (height)
            sound_attenuation = (10 * math.log10(distance_weighted))
            high_cut_frequency = (1 / distance_weighted) * 15000
            return [-(sound_attenuation), high_cut_frequency];

        # This function calculates the intersections between the sources and geometries on the source/listener path triangle_left and triangle_right
        # It is done on the left and on the right to differentiate the two ears.
        # - sphere_div : number of divisions of the source's sphere
        def intersection_source_env(sound_source, sphere_div, listener, environment):

            # - sphere_srf : identifier of the sphere of center source_location and radius source_size*2,5
            # - pt_list : list of points used to form lines
            # - pt = point
            # - sphere_parameter : parameterized surface of the sphere
            # - new_pt : new point obtained from the evaluated surface of the parameterized sphere
            sphere_srf = rs.AddSphere((sound_source[1]), ((sound_source[2]) * 2.5))
            pt_list = []
            for i in range(0, sphere_div + 1, 1):
                for j in range(0, sphere_div + 1, 1):
                    pt = (i / sphere_div, j / sphere_div, 0)
                    sphere_parameter = rs.SurfaceParameter(sphere_srf, pt)
                    new_pt = rs.EvaluateSurface(sphere_srf, sphere_parameter[0], sphere_parameter[1])
                    pt_list.append(rs.AddPoint(new_pt))

            # - lines_left : list of lines between the points of pts and triangle_left of listener
            # - lines_right : list of lines between the points of pts and triangle_right of listener
            lines_left = []
            lines_right = []
            for p in pt_list:
                lines_left.append(rs.AddLine((listener[0])[1], p))
                lines_right.append(rs.AddLine((listener[0])[2], p))

            # - intersection_left : list of intersection points/curves between geo_obj from environment and lines_left
            # - intersection_right : list of intersection points/curves between geo_obj from environment and lines_right
            intersection_left = []
            intersection_right = []

            for i in lines_left:
                for u in environment:
                    if type(rs.CurveBrepIntersect(i, (u[0]))) == tuple:
                        intersection_left.append((rs.CurveBrepIntersect(i, (u[0]))) + (u[1],))
                    else:
                        intersection_left.append((rs.CurveBrepIntersect(i, (u[0]))))

            for i in lines_right:
                for u in environment:
                    if type(rs.CurveBrepIntersect(i, (u[0]))) == tuple:
                        intersection_right.append((rs.CurveBrepIntersect(i, (u[0]))) + (u[1],))
                    else:
                        intersection_right.append((rs.CurveBrepIntersect(i, (u[0]))))

            # - inter_point_left :
            # - inter_point_right :
            # - nb_unblocked_lines_left : lines on the left which aren't blocked
            # - nb_unblocked_lines_right : lines on the right which aren't blocked
            inter_point_left = 0
            inter_point_right = 0

            for i in intersection_left:
                if type(i) is tuple:
                    inter_point_left += (1 * (i[-1]))
            nb_unblocked_lines_left = len(intersection_left) - inter_point_left

            for i in intersection_right:
                if type(i) is tuple:
                    inter_point_right += (1 * (i[-1]))
            nb_unblocked_lines_right = len(intersection_right) - inter_point_right

            # be sure that the variables nb_unblocked_lines_left and nb_unblocked_lines_right aren't negative//null to be able to do the following calculation
            if nb_unblocked_lines_left <= 0:
                nb_unblocked_lines_left = 0.1

            if nb_unblocked_lines_right <= 0:
                nb_unblocked_lines_right = 0.1

            # - sound_attenuation_env_left : variable which quantify the attenuation of the sound on the left
            # - sound_attenuation_env_right : variable which quantify the attenuation of the sound on the right
            sound_attenuation_env_left = ((math.log10(
                nb_unblocked_lines_left * 100 / len(intersection_left))) * 35.3) - 70.6
            sound_attenuation_env_right = ((math.log10(
                nb_unblocked_lines_right * 100 / len(intersection_right))) * 35.3) - 70.6

            return [sound_attenuation_env_left, sound_attenuation_env_right];

        # the function allows to adapt the source volume for the software
        # - source_vol : new volume wich can be used by the software
        def volume_source(sound_source):
            if sound_source[3] == 0 or sound_source[3] > 70:
                source_vol = 0
            else:
                source_vol = (sound_source[3] - 70)
            return source_vol

        # the function calculates the rays of reverberation
        # - sphere_div : number of divisions of the source's sphere
        def reverberation(environment, listener, sound_source, sphere_div):

            # - listener_head : point which represent the head of the listener
            # - sphere_srf : identifier of the sphere of center Source_Location and radius Source_Size
            # - source_location : point of the location of the source
            listener_head = listener[0][0]
            sphere_srf = (rs.AddSphere(sound_source[1], sound_source[2]))
            source_location = (sound_source[1])

            # - geometries : list of environment_geo from environment
            geometries = []
            for i in environment:
                geometries.append(i[0])

            # - first_reflection_point  : list of components 2 of the lines from reflection_points (these are points), (first point outside the sphere on which there is a reflection)
            # - first_ref_rays : first line of reflected sound
            # - second_ref_rays : second line of reflected sound
            first_reflection_point = []
            first_ref_rays = []
            second_ref_rays = []

            # - pt : point
            # - sphere_parameter : parameterized surface of the sphere
            # - new_pt : new point obtained from the evaluated surface of the parameterized sphere
            # - pt_ray : point used to form rays
            # - ray_vect : vector created from new_pt and source_location (radius of the source sphere)
            # - reflection_points : points got from the line modeled from the surface array geometries, the starting point of the ray (source_location),
            #                       the direction vector of the ray (ray_vector) and the maximum number of times the ray will be reflected (here 4)
            #                       (points on which the sound line bounces (on the geometries))
            for i in range(0, sphere_div + 1, 1):
                for j in range(0, sphere_div + 1, 1):
                    pt = (i / sphere_div, j / sphere_div, 0)
                    sphere_parameter = rs.SurfaceParameter(sphere_srf, pt)
                    new_pt = rs.EvaluateSurface(sphere_srf, sphere_parameter[0], sphere_parameter[1])
                    pt_ray = rs.AddPoint(new_pt)
                    ray_vect = rs.VectorCreate(pt_ray, source_location)
                    reflection_points = rs.ShootRay(geometries, source_location, ray_vect, reflections=4)

                    # - reflection_rays : polyline list created from elements from reflection_points
                    # - closest_pt_listener_par : point of the polyline of reflection_rays that is closest to listener_head
                    #                             (parameter of the curve that gives the location of the point in the reflection line that is closest to the listener)
                    # - closest_pt_listener : point resulting from the evaluation of the polyline of reflection_rays with respect to the parameter closest_pt_listener_par
                    #                         (the closest point to listener)
                    # - dist_rays_listener : distance between listener_head and closest_pt_listener
                    try:
                        first_reflection_point.append(reflection_points[1])
                        reflection_rays = rs.AddPolyline(reflection_points)
                        closest_pt_listener_par = rs.CurveClosestPoint(reflection_rays, listener_head)
                        closest_pt_listener = rs.EvaluateCurve(reflection_rays, closest_pt_listener_par)
                        dist_rays_listener = (rs.Distance(listener_head, closest_pt_listener))

                        # We are only interested in lines that do not pass too far from the listener's head
                        # - first_ref_point_par : parameter of the first reflection point
                        # - second_ref_point_par : parameter of the second reflection point
                        # - end_ref_point_par : point of the reflection_rays-curve closest to the end point of the reflection_rays-curve
                        #                       (parameter of the last reflection point)
                        if dist_rays_listener <= ((listener[0])[3]):
                            first_ref_point_par = rs.CurveClosestPoint(reflection_rays, reflection_points[1])
                            second_ref_point_par = rs.CurveClosestPoint(reflection_rays, reflection_points[2])
                            end_ref_point_par = rs.CurveClosestPoint(reflection_rays,
                                                                     (rs.CurveEndPoint(reflection_rays)))

                            if closest_pt_listener_par > second_ref_point_par:
                                second_ref_rays.append(
                                    closest_pt_listener_par / end_ref_point_par * (rs.CurveLength(reflection_rays)))

                            elif closest_pt_listener_par > first_ref_point_par:
                                first_ref_rays.append(
                                    closest_pt_listener_par / end_ref_point_par * (rs.CurveLength(reflection_rays)))

                    except:
                        pass

            # - first_ref_srf : list of surfaces on which the first reverberation takes place
            first_ref_srf = []
            for geo in geometries:
                i = 0
                while i < len(first_reflection_point) and rs.Distance(
                        (rs.BrepClosestPoint(geo, first_reflection_point[i])[0]), first_reflection_point[i]) >= 0.1:
                    i += 1
                if i != len(first_reflection_point):
                    first_ref_srf.append(geo)

            # - first_ref_abscoef : list of absorption coefficient of first reverberation surfaces
            first_ref_abscoef = []
            for x in environment:
                if x[0] in first_ref_srf:
                    first_ref_abscoef.append(x[2])

            # - first_ref_srf_abscoef : tuple list (reverberation area, absoption coefficient)
            first_ref_srf_abscoef = [(first_ref_srf[i], first_ref_abscoef[i]) for i in range(0, len(first_ref_srf))]

            # - ref_box : box shape created from the first_reflection_point list -> volume of the reflection scene
            # - ref_box_area : area of the box ref_box rounded to 2 decimal places
            # - ref_box_volume : value of the ref_box volume rounded to the first decimal place
            ref_box = rs.AddBox(rs.BoundingBox(first_reflection_point))
            ref_box_area = round((rs.SurfaceArea(ref_box)[0]), 2)
            ref_box_volume = round(((rs.SurfaceVolume(ref_box))[0]), 1)

            # - first_ref_positive_srf : for positive first_ref_srf_abscoef volumes, list of first_ref_srf_abscoef geometries
            # - first_ref_positive_abscoef : for positive first_ref_srf_abscoef volumes, list of first_ref_srf_abscoef absorption coefficient
            #                                (the aborption coefficient i is related to the geometry of index i in the list first_ref_positive_srf)
            # - first_ref_negative_area : for negative first_ref_srf_abscoef volumes, list of first_ref_srf_abscoef area of the surfaces
            #                            (areas of the surfaces for which we have reflections)
            # - first_ref_negative_abscoef : for negative first_ref_srf_abscoef volumes, list of first_ref_srf_abscoef absorption coefficient
            first_ref_positive_srf = []
            first_ref_positive_abscoef = []
            first_ref_negative_area = []
            first_ref_negative_abscoef = []
            for i in first_ref_srf_abscoef:
                if rs.SurfaceVolume(i[0]) > 0:
                    first_ref_positive_srf.append(i[0])
                    first_ref_positive_abscoef.append(i[1])
                else:
                    first_ref_negative_area.append((rs.SurfaceArea(i[0]))[0])
                    first_ref_negative_abscoef.append(i[1])

            # - srf_exploded : object identifiers created by decomposing the first_ref_positive_srf surface into smaller objects, the goal is to explode the volume into lots of small surfaces
            srf_exploded = rs.ExplodePolysurfaces(first_ref_positive_srf)

            # - srf_center_pt : centroid list of srf_exploded surfaces
            srf_center_pt = []
            for i in srf_exploded:
                p = 0
                while p < len(first_reflection_point) and rs.Distance(
                        (rs.BrepClosestPoint(i, first_reflection_point[p])[0]), first_reflection_point[p]) >= 0.01:
                    p += 1
                if p != len(first_reflection_point):
                    first_ref_negative_area.append(rs.SurfaceArea(i)[0])
                    srf_center_pt.append(rs.SurfaceAreaCentroid(i)[0])

            # We recover the absorption coefficients corresponding to the new surfaces that we have added in first_ref_negative_area
            for j in range(len(first_ref_positive_srf)):
                for i in srf_center_pt:
                    if rs.Distance((rs.BrepClosestPoint(first_ref_positive_srf[j], i)[0]), i) < 0.01:
                        first_ref_negative_abscoef.append(first_ref_positive_abscoef[j])

                        # - equivalent_abs_area : equivalent absorption area = multiplication of the absorption coefficient by the real volume (we have a value per surface)
            try:
                equivalent_abs_area = [first_ref_negative_area[i] * (first_ref_negative_abscoef[i]) for i in
                                       range(0, len(first_ref_negative_abscoef))]
            except:
                raise Exception(
                    'One source must be too deep inside a geometry, try to get it out or to move it a little bit !')

            # - equivalent_abs_area_sum : sum of all of the equivalent absorption area
            # - first_ref_negative_area_sum : sum of all of the area in first_ref_negative_area
            # - empty_area : all the area on which there is no reflection
            equivalent_abs_area_sum = len(equivalent_abs_area)
            first_ref_negative_area_sum = round(len(first_ref_negative_area), 2)
            empty_area = 2 * (round(ref_box_area - first_ref_negative_area_sum, 2))

            # check the value of empty_area
            if empty_area < 0:
                empty_area = 0

            # - rev_time : reverberation time
            rev_time = 1000 * (0.16 * ref_box_volume) / (equivalent_abs_area_sum + empty_area)

            # - first_reflection_sum : amount of first reflection for all of the rays
            # - first_reflection : amount of first reflection for one ray
            first_reflection_sum = 0
            for f in first_ref_rays:
                first_reflection = ((((listener[0])[3]) * 15) / f)
                first_reflection_sum += first_reflection

            # check the value of first_reflection_sum
            if first_reflection_sum > 125:
                first_reflection_sum = 125

            # - second_reflection_sum : amount of second reflection for all of the rays
            # - second_reflection : amount of second reflection for one ray
            second_reflection_sum = 0
            for s in second_ref_rays:
                second_reflection = ((((listener[0])[3]) * 20) / s)
                second_reflection_sum += second_reflection

            # check the value of second_reflection_sum
            if second_reflection_sum > 125:
                second_reflection_sum = 125

            # - reverb : output variable, list of reverberation time and first and second reflection proportions
            reverb = []
            reverb.append(round(first_reflection_sum))
            reverb.append(round(second_reflection_sum))
            reverb.append(round(rev_time, 2))

            return reverb

        def main():

            # - impact_distance_value : list containing the distance-related sound attenuation and the cutoff frequency
            # - list_sources_path : list of the paths of the sources
            impact_distance_value = []
            list_sources_path = []

            # - list_sources_panoramic : proportion of sound on the left and on the right
            # - list_sources_intersection_source_env : the intersection of the sound on the left and on the right
            list_sources_panoramic = []
            list_sources_intersection_source_env = []

            # - list_first_reflection_value : first reflection weighted by the factor (indoor/outdoor)
            # - list_second_reflection_value : second reflection weighted by the factor (indoor/outdoor)
            # - list_rev_time : list of the reverberation times
            # - rev_time_by_source : reverberation time by source
            # - rev_info_by_source : list of strings giving information on the reverberation of the sources
            list_first_reflection_value = []
            list_second_reflection_value = []
            list_rev_time = []
            rev_time_by_source = []
            rev_info_by_source = []

            # - manual_volume : Manual volume (if not entered, a default value is taken)
            # - randomize : value entered by the user that gives the probability that the sound will be played
            manual_volume = []
            randomize = []

            for iS in range(len(sources)):

                # - closest_pt_on_sphere : point of the source sphere that is closest to the listener
                # - dist_listener_source : distance between the source and the listener
                # - source_path_init // source_path_split // source_path_joined => successive modifications of the source path to obtain
                #                                                                  a writing having the correct form, it is then stored
                #                                                                  in list_sources_path
                closest_pt_on_sphere = (
                    rs.BrepClosestPoint((rs.AddSphere((sources[iS])[1], (sources[iS])[2])), listener_head))
                dist_listener_source = (rs.Distance(listener_head, (closest_pt_on_sphere[0])))
                impact_distance_value.append(impact_distance(listener_height, dist_listener_source))
                source_path_init = (sources[iS][0]).replace('\\', '/')
                source_path_split = (source_path_init).split()
                source_path_joined = ("\ ").join(source_path_split)
                list_sources_path.append(source_path_joined)

                if _lock == True:
                    list_sources_path[iS] = '/i/NoSource_LOCKED'
                    self.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Remark,
                                           'Your Sketch is locked, no sound until you unlock ;)')
                    self.Message = "EsquisSons is locked"

                list_sources_panoramic.append(panoramic(listener, (sources[iS])[1]))
                list_sources_intersection_source_env.append(
                    intersection_source_env((sources[iS]), 3, listener, environment))

                # if the reverberations are activated, the values necessary for the execution are calculated
                # - reverb : the output of the function reverberation for the source
                if _reverb_on == True:
                    reverb = reverberation(environment, listener, (sources[iS]), 50)
                    list_first_reflection_value.append((reverb)[0] * indoor_factor)
                    list_second_reflection_value.append((reverb)[1] * indoor_factor)
                    list_rev_time.append((reverb)[2])
                    rev_time_by_source.append(round((reverb)[2] / 1000, 1))
                    rev_info_by_source.append(str(round((reverb)[2] / 1000, 1)) + 'sec // mix : ' + str(
                        (reverb[0] + reverb[1]) * indoor_factor) + '%')

                # recovery of manual_volume and randomize
                manual_volume.append(volume_source(sources[iS]))
                randomize.append(sources[iS][4])

            # if the reverberations aren't activated, we display the proper message
            if _reverb_on is not True:
                rev_time_by_source.append('No RT: Reverb is disabled')
                rev_info_by_source.append('No infos: Reverb is disabled')

            # send information calculated to the Sound Application

            # - osc_msg : osc message
            # - info_osc : list of information on osc communication
            osc_msg = []
            info_osc = []

            # allows to display the information about the sources as an output
            for i in range(10):

                # - osc_port : link port
                iport = (57100 + i)
                info_osc.append(OSC.OSCClient())
                info_osc[i].connect(("127.0.0.1", iport))
                osc_msg.append(OSC.OSCMessage())

                if i < len(sources):
                    osc_msg[i].append(impact_distance_value[i][0])
                    osc_msg[i].append(impact_distance_value[i][1])
                    osc_msg[i].append(list_sources_path[i])
                    osc_msg[i].append(list_sources_panoramic[i])

                    if _lock is True:
                        osc_msg[i].append(0)

                    else:
                        osc_msg[i].append(2)
                        osc_msg[i].append(list_sources_intersection_source_env[i])

                    try:
                        osc_msg[i].append(list_first_reflection_value[i])
                        osc_msg[i].append(list_second_reflection_value[i])
                        osc_msg[i].append(list_rev_time[i])
                    except:
                        osc_msg[i].append(0)
                        osc_msg[i].append(0)
                        osc_msg[i].append(0)

                    osc_msg[i].append(manual_volume[i])
                    osc_msg[i].append(randomize[i])
                    info_osc[i].send(osc_msg[i])

                else:
                    osc_msg[i].append(-127)
                    osc_msg[i].append(0)
                    osc_msg[i].append('/i/NoSource')
                    osc_msg[i].append(0)
                    osc_msg[i].append(0)
                    osc_msg[i].append(0)
                    osc_msg[i].append(0)
                    osc_msg[i].append(0)
                    osc_msg[i].append(0)
                    osc_msg[i].append(0)
                    osc_msg[i].append(0)

                try:
                    info_osc[i].send(osc_msg[i])
                except:
                    self.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Error,
                                           'Connexion Failed, please ensure APP is open (use launcher) then reset the engine (with lock/unlock)')
                    self.Message = 'Connexion Failure'

                print
                "message, source {} : {}".format(i, osc_msg[i])

            return (rev_time_by_source, rev_info_by_source)

        if __name__ == "__main__":
            rt_by_source, rev_info_by_source = main()
            visualization = [environment, listener, sources]
        return (visualization, rt_by_source, rev_info_by_source)
