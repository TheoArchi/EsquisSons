"""EsquisSons Built-in Sounds provides some basic sounds to start your sketch
Use a value list to visualize sound names
-
AAU / Theo Marchal / BETA VERSION / AVRIL2020"""

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import Grasshopper.Kernel as gh


class BuiltInSounds(component):

    def RunScript(self, valuelist_gh):

        # block init
        __author__ = "theomarchal"
        self.Params.Input[
            0].Description = "Connect here a Value List component (from Grasshopper) and then select the sound you want to use"
        self.Params.Output[0].Description = "Connect to the source_path input from the Source component (EsquisSons)"
        self.Name = "Built-in Sounds"
        self.NickName = "Sounds"
        self.Message = "EsquisSons V3"
        self.Category = "EsquisSons"
        self.SubCategory = "2/ Options"

        # - source_list : a list of every name of Grasshopper pre-installed sounds
        source_list = ['Bells', 'Birds', 'Fountain', 'Playground', 'Urban', 'talk', 'cherokee', 'FemVoice',
                       'BusyAvenue', 'rainstick', 'duduk', 'anton', 'vibes-a1']

        # check valuelist_gh
        if valuelist_gh is None:
            self.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning,
                                   'You must connect a Value List to choose from the built-in sounds')

        # access to the objects connected to the block on the document
        # - document : grasshopper document where the block is used
        # - value_list : objects connected to the block
        document = self.OnPingDocument()
        value_list = None
        for object in document.ActiveObjects():
            if self.DependsOn(object):
                value_list = object

        # apply the source_list to the Value List connected to the block,
        # so the user can choose a Grasshopper sound from the Grasshopper Value List

        if value_list is not None:
            # creation of a list of the names of the items already in value_list
            # raise an exception if the value_list has no attributes ListItems,
            # i.e. if the value_list is not a Grasshopper Value List
            # - list_names : list of name of every item from value_list
            list_names = []
            try:
                for item in value_list.ListItems:
                    list_names.append(item.Name)
            except:
                raise Exception('You must connect a Value List to valuelist_gh')

            # if list_names is different from the source_list, then the source_list must be applied
            if set(list_names) != set(source_list):
                # clear the value_list
                value_list.ListItems.Clear()
                # create a new value list with items name = path
                # - path : the name of the sound in quotes
                for name in source_list:
                    path = '"{}"'.format(name)
                    value_list.ListItems.Add(Grasshopper.Kernel.Special.GH_ValueListItem(name, path))

                # update of value_list
                value_list.SelectItem(1)
                value_list.Attributes.ExpireLayout()
                value_list.Attributes.PerformLayout()

        # source_path is the value chosen from valuelist_gh
        source_path = valuelist_gh

        return source_path