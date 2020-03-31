
"""EsquisSons Built-in Sounds provides some basic sounds to start your sketch
Use a value list to visualize sound names
-
AAU / Theo Marchal / BETA VERSION / AVRIL2020"""

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class MyComponent(component):
    
    def RunScript(self, ValueList_gh):
        
        __author__ = "theomarchal"
        self.Params.Input[0].Description = "Connect here a ValueList component (from Grasshopper) and then select the sound you want to use"
        self.Params.Output[0].Description = "Connect to the Source_Path input from the Source Component (EsquisSons)"
        self.Name = "Built-in Sounds"
        self.NickName = "Sounds" 
        self.Message = "EsquisSons V3"
        self.Category = "EsquisSons"
        self.SubCategory = "2/ Options"
        
        
        
        import rhinoscriptsyntax as rs
        import Grasshopper
        import Grasshopper.Kernel as gh
        
        rem = gh.GH_RuntimeMessageLevel.Remark
        ero = gh.GH_RuntimeMessageLevel.Error
        war = gh.GH_RuntimeMessageLevel.Warning
        
        Source_Path = ValueList_gh
        
        Sourcelist = ['Bells','Birds','Fountain','Playground','Urban','talk','cherokee','FemVoice','BusyAvenue','rainstick','duduk','anton','vibes-a1']
        ghdoc2 = self.OnPingDocument()
        if ValueList_gh is None :
            self.AddRuntimeMessage(war, 'You must connect a value list to choose from the built-in sounds')
        
        vallistitems = []
        valuelist = None
        for obj in ghdoc2.ActiveObjects():
        	if self.DependsOn(obj):
        		try:
        			vallistitems = obj.ListItems
        			valuelist = obj
        		except:
        			pass
        
        if valuelist is not None:
        	listnames = []
        	for vitem in vallistitems:
        		listnames.append(vitem.Name)
        	if set(listnames) != set(Sourcelist):
        		vallistitems.Clear()
        		for n in Sourcelist:
        			try: 
        				int(n)
        				rhs = n
        			except ValueError:
        				rhs = '"{}"'.format(n)
        			vallistitems.Add(Grasshopper.Kernel.Special.GH_ValueListItem(n, rhs))
        		valuelist.SelectItem(1)
        		valuelist.Attributes.ExpireLayout()
        		valuelist.Attributes.PerformLayout()
        return Source_Path
