"""EsquisSons Listener is used to declare the listening point.
Define its position, orientation and size :)
-
AAU / Theo Marchal / BETA VERSION / AVRIL2020
With the Contribution of Manon COUTIER & Domitille GRANDJEAN"""

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs


class ListenerPoint(component):

    def RunScript(self, _listener_location, _listener_direction, _listener_height):

        # block init
        __author__ = "theomarchal"
        self.Params.Input[0].Description = "Location of the listener foots [as a point] (default = (0,0,0))"
        self.Params.Input[1].Description = "Direction of the listener [in degrees from 0 to 360]"
        self.Params.Input[2].Description = "How tall is the listener (default = 1.80)"
        self.Params.Output[0].Description = "Listener geometry, size and direction"
        self.Params.Output[1].Description = "Listener object (plug it into EsquisSons MainEngine)"
        self.Name = "Listener Point"
        self.NickName = "Listener"
        self.Message = "EsquisSons V3"
        self.Category = "EsquisSons"
        self.SubCategory = "1/ Scene"

        # set default values
        if _listener_location is None:
            _listener_location = rs.AddPoint(0, 0, 0)
        if _listener_direction is None:
            _listener_direction = 0
        if _listener_height is None:
            _listener_height = 1.8

        # creation of a listener (as a list of list)

        # - height_trans_matrix : matrix transfering a vector or a point along the z-axis with a lenght of _listener_height
        height_trans_matrix = rs.XformTranslation((0, 0, _listener_height))

        # - listener_head : point representing the head of the listener
        listener_head = rs.PointTransform(_listener_location, height_trans_matrix)

        # creation of three vectors :
        # - direction_vect : listening direction vector
        # - left_vect : vector orthogonal to direction_vect, on the left
        # - right_vect : vector orthogonal to direction_vect, on the right
        direction_vect = rs.VectorRotate([0, (_listener_height), 0], _listener_direction, [0, 0, 1])
        left_vect = rs.VectorScale((rs.VectorRotate(direction_vect, 90, [0, 0, 1])), 0.5)
        right_vect = rs.VectorScale((rs.VectorRotate(direction_vect, -90, [0, 0, 1])), 0.5)

        # creation of a triangle/arrow pointing toward the listener_direction
        # - triangle_peak : point at the end of direction_vect
        # - triangle_left : point at the end of left_vect
        # - triangle_right : point at the end of right_vect
        # - triangle_list : list of the three points of the triangle
        triangle_peak = rs.PointTransform(_listener_location, (rs.XformTranslation(direction_vect)))
        triangle_left = rs.PointTransform(_listener_location, (rs.XformTranslation(left_vect)))
        triangle_right = rs.PointTransform(_listener_location, (rs.XformTranslation(right_vect)))
        triangle_list = [triangle_peak, triangle_left, triangle_right]

        # - listener_preview : creates a Rhinoceros listener with a sphere for the head,
        # - a line for the body and an arrow for the listening direction
        listener_preview = [rs.AddSphere(listener_head, (_listener_height / 10)),
                            rs.AddLine(_listener_location, listener_head), rs.AddSrfPt(triangle_list)]

        # transfer triangle_left and triangle_right to the listener_height
        triangle_left = rs.PointTransform(triangle_left, height_trans_matrix)
        triangle_right = rs.PointTransform(triangle_right, height_trans_matrix)

        listener_point = [listener_head, triangle_left, triangle_right, _listener_height]
        listener = [listener_point]

        return (listener_preview, listener)
