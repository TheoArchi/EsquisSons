                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     """EsquisSons Source allows you to define a sound source.
Give its position, its size, and the sound file to play :)
-
AAU / Theo Marchal / BETA VERSION / AVRIL2020
with the contribution of Manon COUTIER & Domitille GRANDJEAN """

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import Grasshopper.Kernel as gh


class SoundSource(component):

    def RunScript(self, _source_location, source_path, _source_size, _source_opt):

        # block unit
        __author__ = "theomarchal"
        self.Params.Input[
            0].Description = "Location of the source (as a point -Default is set to 0,0,0 /Disabled for curve shapes in source options)"
        self.Params.Input[1].Description = "Path to the sound file (as a text)"
        self.Params.Input[2].Description = "Source Size (Amplitude Sphere radius - Default is set to 1)"
        self.Params.Input[3].Description = "*Optional* Source Options (From 'Source Options' component)"
        self.Params.Output[0].Description = "Source representation"
        self.Params.Output[1].Description = "Source Object"
        self.Name = "Sound Source"
        self.NickName = "Source"
        self.Category = "EsquisSons"
        self.SubCategory = "1/ Scene"
        self.Message = "EsquisSons V3"

        # set source_location default value
        if _source_location is None:
            _source_location = rs.AddPoint(0, 0, 0)

        # set _source_size default value
        if _source_size is None:
            _source_size = 1

        # set _source_opt default value
        if _source_opt is None:
            _source_opt = [0, 0, 0, 0]

        # source_path check
        if source_path is None or len(source_path) == 0:
            source_path = "NoSound"
            self.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning,
                                   'Source need a sound to be played (source_path input)- '
                                   'you can use built-in sound (EsquiSsons) for a start')

        # display of a message if the source is randomized
        if _source_opt is not None:

            # message displayed on the block about the use of _randomize_source or not in the options
            if _source_opt[0][3] != 0:
                self.Message = "Randomly play source"

            # new functionality in progress
            """if SpS is None:
            else :
                Curve = _source_opt[0][0]
                CrvPts = rs.DivideCurveEquidistant(Curve,(_source_size*2),create_points=False,return_points=True)
                _source_location = []
                source_preview=[]
                for point in CrvPts : _source_location.append(point)
                for point in _source_location : source_preview.append(rs.AddSphere(point,_source_size))
                sound_source = []
                for i in _source_location :
                    sSD =[source_path,i,_source_size,_source_opt[0][2],_source_opt[0][3]]
                    sound_source.append(sSD)
                    source = sound_source"""

        # creation of a source (as a list of list)
        sound_source = [source_path, _source_location, _source_size, _source_opt[0][2], _source_opt[0][3]]
        source = [sound_source]

        # creation of a preview for the source
        # - source_preview : creates a Rhinoceros source with a sphere of a size _source_size
        source_preview = rs.AddSphere(_source_location, _source_size)

        return (source_preview, source)
