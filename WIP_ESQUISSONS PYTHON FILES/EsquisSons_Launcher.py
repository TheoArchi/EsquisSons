"""EsquisSons Launcher
Use 2 boolean toggles to launch the app and then start the sound module :)
-
AAU / Theo Marchal / BETA VERSION / AVRIL2020
With the Contribution of Manon COUTIER & Domitille GRANDJEAN"""

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import os
import OSC
import platform
import time
import subprocess
import Grasshopper.Kernel as gh


class EsquisSonsLauncher(component):

    def RunScript(self, open_esquissons, on_off, _alt_path):

        # block init
        __author__ = "theomarchal"
        self.Params.Input[0].Description = "Boolean input, set True to run the sound algorythm"
        self.Params.Input[1].Description = "General Status of EsquisSons module"
        self.Params.Input[2].Description = "Alternative Path to -EsquisSons.exe/app-"
        self.Name = "EsquisSons Launcher"
        self.NickName = "Launcher"
        self.Message = "EsquisSons V3"
        self.Category = "EsquisSons"
        self.SubCategory = "0/ EsquisSons"

        # path to Esquissons Sound App. If _alt_path is None, it's the default one.
        esq_path = _alt_path
        if esq_path is None:
            if platform.system() == 'Windows':
                esq_path = os.getenv('APPDATA') + '\Grasshopper\Libraries\EsquisSons\EsquisSons.exe'
            if platform.system() == 'Darwin':
                esq_path = '/applications/EsquisSons.app'

        # connection to Esquissons Sound App initialization (OSC protocol)
        client = OSC.OSCClient()
        client.connect(('127.0.0.1', 58234))
        osc_message = OSC.OSCMessage()
        osc_message.append("no message")
        osc_message.append("no int")

        if open_esquissons == True:

            # launching of Esquissons Sound App
            # display error if the Sound App can't be found in esq_path
            try:
                if platform.system() == 'Windows':
                    os.startfile(esq_path)
                    error = False
                if platform.system() == 'Darwin':
                    subprocess.call(['open', esq_path])
                    error = False
            except:
                error = True
            if error == True:
                self.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning,
                                       "EsquisSons can't be open ! " + esq_path + " can not be found. Please check the installation !")
                self.Message = "EsquisSons is OFF"

            else:

                # display of different messages depending on the status of Esquissons Sound App
                if on_off == True:
                    osc_message[0] = "EsquisSons\\ is\\ Online!\\ Let's\\ make\\ some\\ noise"
                    osc_message[1] = 1
                    self.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Remark,
                                           'EsquisSons is online ! Let''s make some noise !')
                    self.Message = "EsquisSons is ON"
                else:
                    osc_message[
                        0] = 'EsquisSons\\ is\\ not\\ online\\ turn\\ it\\ on\\ (in\\ Gh)\\ to\\ start\\ the\\ sketch'
                    osc_message[1] = 0
                    self.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning,
                                           'EsquisSons app should be open ! Now turn it on with a boolean toogle (on_off input)!')
                    self.Message = "Almost there : Turn it on !"

        else:

            # display of different messages depending on the status of Esquissons Sound App
            if on_off is True:
                osc_message[0] = "EsquisSons\\ is\\ Online!\\ Let's\\ make\\ some\\ noise"
                osc_message[1] = 1
                self.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning,
                                       'Message sent, EsquisSons should be online but...Check if EsquisSons app is open ! (if not, use the open_esquissons input with boolean toggle ;)')
                self.Message = "EsquisSons is ON"
            else:
                self.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Error,
                                       'EsquisSons is not online and probably not open. You should open_esquissons, then turn it on with on_off !')
                osc_message[
                    0] = "EsquisSons\\ is\\ not\\ online\\ turn\\ it\\ on\\ (in\\ Gh)\\ to\\ start\\ the\\ sketch"
                osc_message[1] = 0
                self.Message = "EsquisSons is OFF"

        # send osc_message to Esquissons Sound App
        client.send(osc_message)

        return 
