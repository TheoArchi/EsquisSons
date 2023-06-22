"""EsquisSons Source Options allows you to more precisely define a source (shuffle, volume, mute etc.)
-
AAU / Theo Marchal / BETA VERSION / AVRIL2020
With the Contribution of Manon COUTIER & Domitille GRANDJEAN"""

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import math


class SourceOptions(component):

    def RunScript(self, _source_on, _randomize_source, _manual_volume):

        # block init
        __author__ = "theomarchal"
        self.Params.Input[0].Description = "Mute the source if set to False (use boolean here)"
        self.Params.Input[
            1].Description = "Set chance of playing the source (1/x chance where x is the input)(Int input, if none the source is continuously looped)"
        self.Params.Input[
            2].Description = "Manual Volume from 1 to 70 (disengage the mainengine calculation for volume if connected - not active if volume is set to 0)"
        self.Params.Output[0].Description = "Source options (connect to Source component)"
        self.Name = "Source options"
        self.NickName = "Source_Opt"
        self.Message = "EsquisSons V3"
        self.Category = "EsquisSons"
        self.SubCategory = "2/ Option"

        # set _source_on values
        if _source_on is None:
            _source_on = True
        if _source_on is False:
            _manual_volume = 1

        # set _manual_volume value :
        # 1 means no sound, 0 means no _manual_volume set
        if _manual_volume is None:
            _manual_volume = 0
        elif _manual_volume > 70:
            _manual_volume = 70
        elif _manual_volume < 1:
            _manual_volume = 1
        elif _manual_volume != 0:
            _manual_volume = ((10 * math.log10(1 + _manual_volume)))
            _manual_volume = 3.49 * _manual_volume

        # set _randomize_source
        if _randomize_source is None or _randomize_source == 1:
            _randomize_source = 0

        # create source options as a list of list
        options = ['None', _source_on, _manual_volume, _randomize_source]
        source_opt = [options]

        return source_opt
