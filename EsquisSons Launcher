
"""EsquisSons Launcher
Use 2 boolean toggles to launch the app and then start the sound module :)
-
AAU / Theo Marchal / BETA VERSION / AVRIL2020"""

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class MyComponent(component):
    
    def RunScript(self, Open_Esquissons, On_Off, Alt_path_Optionnal):
        
        __author__ = "theomarchal"
        self.Params.Input[0].Description = "Boolean input, set True to run the Sound Algorythm"
        self.Params.Input[0].Description = "General Status of Esquis'Sons! module"
        self.Params.Input[1].Description = "Alternative Path to -EsquisSons.exe/app-"
        self.Name = "EsquisSons Launcher"
        self.NickName = "Launcher" 
        self.Message = "EsquisSons V3"
        self.Category = "EsquisSons"
        self.SubCategory = "0/ EsquisSons"
        import os
        import OSC
        import platform
        import time
        import subprocess
        import Grasshopper.Kernel as gh

        rem = gh.GH_RuntimeMessageLevel.Remark
        ero = gh.GH_RuntimeMessageLevel.Error
        war = gh.GH_RuntimeMessageLevel.Warning
        
        
        esqpath = Alt_path_Optionnal
        
        if esqpath is None:
            
            if platform.system() == 'Windows':
                esqpath = os.environ["USERPROFILE"]+'\Documents\EsquisSons\EsquisSons.exe'
            
            if platform.system() == 'Darwin':
                esqpath = '/applications/EsquisSons.app'
            
        c = OSC.OSCClient()
        d = OSC.OSCClient()
        c.connect(('127.0.0.1', 58234))  
        oscmsg = OSC.OSCMessage()
        oscmsg.append("no message")
        oscmsg.append("no int")
        
        if Open_Esquissons == True :
            try :
                if platform.system() == 'Windows':
                    os.startfile(esqpath)
                    error = ''
                if platform.system() == 'Darwin':
                    subprocess.call(['open', esqpath])
                    error =''
            except :
                error = 'True'
            if error == 'True' :
                self.AddRuntimeMessage(war, "EsquisSons can't be open ! "+esqpath+' can not be found Please check the installation !')
                self.Message = "EsquisSons is OFF"
            else :
                if On_Off == True :
                    oscmsg[1] = 1
                    oscmsg[0] = "EsquisSons\\ is\\ Online!\\ Let's\\ make\\ some\\ noise"
                    self.AddRuntimeMessage(rem, 'EsquisSons! is Online ! Lets make some noise !')
                    self.Message = "EsquisSons is ON"
                if On_Off == False :
                    oscmsg[0] = 'EsquisSons\\ is\\ not\\ Online\\ turn\\ it\\ on\\ (in\\ Gh)\\ to\\ start\\ the\\ sketch'
                    self.AddRuntimeMessage(war, 'EsquisSons app should be open ! Now turn it ON with a boolean Toogle (On_Off input)!')
                    self.Message = "Almost there : Turn it on !"
        else :
            if On_Off is True :
                oscmsg[1] = 1
                oscmsg[0] = "EsquisSons\\ is\\ Online!\\ Let's\\ make\\ some\\ noise"
                self.AddRuntimeMessage(war, 'Message sent, EsquisSons should be online but...Check if Esquissons app is open ! (if not, use the Open_esquissons input with boolean toggle ;)')
                self.Message = "EsquisSons is ON"
            else :
                self.AddRuntimeMessage(ero, 'EsquisSons is not Online and probably not Open, You should Open_esquissons, then turn it On with On_Off !')
                oscmsg[0] = "EsquisSons\\ is\\ not\\ Online\\ turn\\ it\\ on\\ (in\\ Gh)\\ to\\ start\\ the\\ sketch"
                oscmsg[1] = "0"
                self.Message = "EsquisSons is OFF"
        
        
            
        c.send(oscmsg)
        return 
