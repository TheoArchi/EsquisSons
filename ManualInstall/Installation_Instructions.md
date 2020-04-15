## MANUAL INSTALLATION 
**RHINOCEROS3D(V6) AND GRASSHOPPER ARE REQUIRED TO WORK WITH ESQUISSONS**

### 1/ You first have to move the sketch application to the default directory :

**Windows :** Move the folder "EsquisSons" from *\EsquisSons* **to** 
>C:\Users\<yourusername>\Documents\

**Mac :** Move the app EsquisSons.app from */EsquisSons* **to** 
>/Applications/

### 2/ Then, you need to place the OSC.py library in the rhino script folder :

**Windows :** Move OSC.py from *\EsquisSons\Components* **to**
>C:\Users\<yourusername>\AppData\Roaming\McNeel\Rhinoceros\6.0\scripts

**Mac :** Move OSC.py from *EsquisSons/Components* **to**
>/Users/<yourusername>/Library/Application Support/McNeel/Rhinoceros/6.0/scripts

### 3/ Last step is to move the component to grasshopper libraries (windows) or UserObjects (mac) :

**Windows :** Move <ComponentName>.ghpy from *\EsquisSons\Components* **to**
>C:\Users\<use name>\AppData\Roaming\Grasshopper\Libraries
** And EsquisSons Main engine_UO.ghuser from *\EsquisSons\Components* **to**
>C:\Users\<use name>\AppData\Roaming\Grasshopper\UserObjects

**Mac :** Move <ComponentName>.ghuser from *EsquisSons/ressources* **to**
>/Users/<yourusername>/Library/Application Support/McNeel/Rhinoceros/6.0/Plug-ins/Grasshopper (b45a29b1-4343-4035-989e-044e8580d9cf)/UserObjects
  
### Now you can launch rhinoceros & grasshopper and start sketching !
