"""EsquisSons Main Engine will calculate the auralisation.
Use Listener, Sources and Geometry objects to connect them here :)
-
AAU / Theo Marchal / BETA VERSION / MARS2020"""

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class MyComponent(component):
    
    def RunScript(self, Listener, Sources, Geometry, Reverb_on, Lock, _Indoor):
        
        __author__ = "theomarchal"
        self.Params.Input[0].Description = "Listener Object (Use Esquissons_Listener component)"
        self.Params.Input[1].Description = "Sources Objects (Use Esquissons_Source component)"
        self.Params.Input[2].Description = "Built environment (Use Esquissons_Built Environment component)"
        self.Params.Input[3].Description = "Set Reverb_On to True to activate Reverberation (Boolean input)(default is off)"
        self.Params.Input[4].Description = "To Lock sources (and sound), set to True, then turn it back to False (Boolean input)(default is unlock)"
        self.Params.Input[4].Description = "*optionnal* Set to 'True' if your scene is indoors, otherwise leave the field empty (Boolean input)(default is outdoor)" 
        self.Params.Output[0].Description = "Visualize output (plug it in visualize components to see rays)"
        self.Params.Output[1].Description = "Reverberation time (in second / for each source)"
        self.Params.Output[2].Description = "Reverberation Info (Time and mix / for each source)"
        
        self.Name = "EsquisSons Main engine"
        self.NickName = "EsquisSons" 
        self.Message = "EsquisSons V3"
        self.Category = "EsquisSons"
        self.SubCategory = "0/ EsquisSons"
        
        import rhinoscriptsyntax as rs
        import math
        import OSC
        import Grasshopper.Kernel as gh
        
        rem = gh.GH_RuntimeMessageLevel.Remark
        ero = gh.GH_RuntimeMessageLevel.Error
        war = gh.GH_RuntimeMessageLevel.Warning
        
        try:
            Lp = ((Listener[0])[0])
            Lh = ((Listener[0])[3])
        except:
            self.AddRuntimeMessage(ero, 'You must connect a Listener component (EsquisSons) !')
            raise Exception('nolistener')
        
        if len(Sources) <= 0:
            self.AddRuntimeMessage(war, 'You must connect at least one Source component (EsquisSons)')
            
        if len(Geometry) <= 0:
            self.AddRuntimeMessage(war, 'You must connect at least one Geometry component (EsquisSons)')
        
        So_dic = dict()
        Si =[]
        SDi =[]
        SPa = []
        SPan = []
        Spl = []
        Sint = []
        Opa = 1
        Srev1 = []
        Srev2 = []
        Str = []
        Vi = []
        MaVol = []
        RTsource = []
        Revinfo = []
        Indoor = _Indoor
        Vi.append(Geometry)
        Vi.append(Listener)
        Vi.append(Sources)
        if Indoor is True :
            Factor = 1.0
        else :
            Factor = 1.5
        def pan(Li,So):
            Tl = ((Li[0])[1])
            Tr = ((Li[0])[2])
            pano =(((rs.Distance(Tl,So))-(rs.Distance(Tr,So))+Lh)*(127/(2*Lh)))
            return pano;
        def DecDist(Ht,Dis):
            Ds = (Dis*1.8)/(Ht)
            dec = (10*math.log10(Ds))
            filter = (1/Ds)*15000
            return [-(dec),filter];
        def inter_S_B(s,div,Lis,br): 
            udiv = div
            vdiv = div
            srf = rs.AddSphere((s[1]),((s[2])*2.5))
            u = rs.SurfaceDomain(srf,0)
            v = rs.SurfaceDomain(srf,1)
            pts = []
            for i in range(0, udiv+1, 1):
                for j in range(0, vdiv+1, 1):
                    pt = (i/udiv,j/vdiv,0)
                    srfP = rs.SurfaceParameter(srf,pt)
                    newpt = rs.EvaluateSurface(srf,srfP[0],srfP[1])
                    pts.append(rs.AddPoint(newpt))
            lig = []
            lid = []
            for p in pts :
                lig.append(rs.AddLine((Lis[0])[1],p))
                lid.append(rs.AddLine((Lis[0])[2],p))
            ig = []
            id = []
            for i in lig :
                for u in br :
                    if type(rs.CurveBrepIntersect(i,(u[0]))) == tuple :
                        ig.append((rs.CurveBrepIntersect(i,(u[0])))+(u[1],))
                    else :
                        ig.append((rs.CurveBrepIntersect(i,(u[0]))))
            for i in lid :
                for u in br:
                    if type(rs.CurveBrepIntersect(i,(u[0]))) == tuple :
                        id.append((rs.CurveBrepIntersect(i,(u[0])))+(u[1],))
                    else :
                        id.append((rs.CurveBrepIntersect(i,(u[0]))))
            if len(id) == 0:
                self.AddRuntimeMessage(war, "it doesn't seem like there's any geometries connected")
                raise Exception('noGeo')
            intg=0
            for i in ig:
                if type(i) is tuple :
                    intg += (1*(i[-1]))
            intd=0
            for i in id:
                if type(i) is tuple :
                    intd += (1*(i[-1]))
            difg = len(ig)-intg
            if difg <= 0 :
                difg = 0.1
            difd = len(id)-intd
            if difd <=0 :
                difd =0.1
            return [(((math.log10(difg*100/len(ig)))*35.3)-70.6),(((math.log10(difd*100/len(id)))*35.3)-70.6)];
        
        def volm(src) :
            if src[3] == 0 or src[3] >=70 :
                srcvlm = 0
            else :
                srcvlm = (src[3]-70)
            return srcvlm
        
        def rev(Ge,Lis,Src,div): 
            udiv = div
            vdiv = div
            Pt_L = Lis [0][0]
            srf = []
            FirstRay = []
            SecondRay = []
            First_RefPoint = []
            drawray =[]
            Reverb = []
            for i in Ge :
                srf.append(i[0])
            sph =(rs.AddSphere(Src[1],Src[2]))
            Src_pt =(Src[1])
            u = rs.SurfaceDomain(sph,0)
            v = rs.SurfaceDomain(sph,1)
            pts = []
            for i in range(0, udiv+1, 1):
                for j in range(0, vdiv+1, 1):
                    pt = (i/udiv,j/vdiv,0)
                    sphP = rs.SurfaceParameter(sph,pt)
                    newpt = rs.EvaluateSurface(sph,sphP[0],sphP[1])
                    pts.append(rs.AddPoint(newpt))
            Dir = []
            for p in pts:
                Dir.append(rs.VectorCreate(p,Src_pt))
            Reflexion = []
            for d in Dir :
                Reflexion.append(rs.ShootRay(srf,Src_pt,d,reflections=4))
            Project = []
            for v in Reflexion :
                Cl_Pt = []
                Ray_v = []
                try :
                    Project.append(v[1])
                    Ray_v.append(rs.AddPolyline(v))
                except :
                    pass
                for u in Ray_v :
                    pt_on = rs.CurveClosestPoint (u,Pt_L)
                    cl = rs.EvaluateCurve(u,pt_on)
                    Dicl = (rs.Distance(Pt_L,cl))
                    if Dicl <= ((Lis [0])[3]):
                        try :
                            First_RefPoint = rs.CurveClosestPoint (u,v[1])
                            Second_RefPoint = rs.CurveClosestPoint (u,v[2])
                            endc=((rs.CurveClosestPoint(u,(rs.CurveEndPoint(u)))))
                            if pt_on > Second_RefPoint :
                                SecondRay.append(pt_on/endc*(rs.CurveLength(u)))
                                drawray.append(u)
                            elif pt_on > First_RefPoint :
                                FirstRay.append(pt_on/endc*(rs.CurveLength(u)))
                        except :
                            pass
            box = rs.AddBox(rs.BoundingBox(Project))
            boxarea = round((rs.SurfaceArea(box)[0]),2)
            Cube = []
            Cube.append(box)
            surfacetorev = []
            for s in srf :
                ptons = []
                for p in Project :
                    if rs.Distance((rs.BrepClosestPoint(s,p)[0]),p) < 0.1 :
                        ptons.append(p)
                if len(ptons) > 0 :
                    surfacetorev.append(s)
            surfaceab = []
            for x in Ge :
                if x[0] in surfacetorev :
                    surfaceab.append(x[2])
            SrfandAb = [(surfacetorev[i], surfaceab[i]) for i in range(0, len(surfacetorev))] 
            bbox = box
            box = round(((rs.SurfaceVolume(box))[0]),1)
            srfvol = []
            srfvolex = []
            absvol = []
            srfarea =[]
            srfrev = []
            areaabs = []
            surfacecenter = []
            absidx = []
            absvoltot = []
            for i in SrfandAb :
                if rs.SurfaceVolume(i[0]) > 0 :
                    srfvol.append(i[0])
                    absvol.append(i[1])
                else :
                    srfarea.append((rs.SurfaceArea(i[0]))[0])
                    absvoltot.append(i[1])
            srfvolex = rs.ExplodePolysurfaces(srfvol)
            for i in srfvolex :
                ptonsrf = []
                usefulsrf = []
                for p in Project :
                    if rs.Distance((rs.BrepClosestPoint(i,p)[0]),p) < 0.01 :
                        ptonsrf.append(p)
                        usefulsrf.append(i)
                if len(ptonsrf) > 0 :
                    srfarea.append(rs.SurfaceArea(i)[0])
                    srfrev.append(i)
            for i in srfrev : 
                surfacecenter.append(rs.SurfaceAreaCentroid(i)[0])
            for b in srfvol :
                for i in surfacecenter :
                    if rs.Distance((rs.BrepClosestPoint(b,i)[0]),i) < 0.01 :
                        absidx.append(srfvol.index(b))
            for i in absidx :
                absvoltot.append(absvol[i]) 
            try:
                areaabs = [srfarea[i]*(absvoltot[i]) for i in range(0, len(absvoltot))]
            except:
                raise Exception('One source must be too deep inside a geometry, try to get it out or to move it a little bit !')
            Builtareaabs = 0
            for i in areaabs :
                Builtareaabs += i
            BuiltArea = 0
            for i in srfarea :
                BuiltArea += i
            BuiltArea = round(BuiltArea,2)
            EmptyArea = 2*(round(boxarea - BuiltArea,2))
            if EmptyArea < 0 :
                EmptyArea = 0
            TR = 1000*(0.16*box)/(Builtareaabs + (EmptyArea*1))
            FRValue = 0
            for f in FirstRay :
                FV = ((((Lis [0])[3])*15)/f)
                FRValue += FV
            if FRValue >=125 :
                FRValue = 125
            SRValue = 0
            for s in SecondRay :
                SV = ((((Lis [0])[3])*20)/s)
                SRValue += SV
            if SRValue > 125 :
                SRValue = 125
            Reverb.append(round(FRValue))
            Reverb.append(round(SRValue))
            Reverb.append(round(TR,2))
            return Reverb

        def main():
            atr =[]
            ManV = []
            totrev = []
            rdm = []
            for iS in range(len(Sources)):
                Closest_pt_on_sphere = (rs.BrepClosestPoint ((rs.AddSphere((Sources[iS])[1],(Sources[iS])[2])), Lp))
                Si.append("S_{}".format(iS+1))
                Distance = (rs.Distance(Lp,(Closest_pt_on_sphere[0])))
                SDi.append(DecDist(Lh,Distance))
                spthi = (Sources[iS][0]).replace('\\','/')
                PathList = (spthi).split()
                PercentS = ("\ ").join(PathList)
                SPa.append(PercentS)
                if Lock == True :
                    SPa[iS] = '/i/NoSource_LOCKED'  
                    self.AddRuntimeMessage(rem,'Your Sketch is locked, no sound until you unlock ;)')
                    self.Message = "EsquisSons is locked"
                SPan.append(pan(Listener,(Sources[iS])[1]))
                Sint.append(inter_S_B((Sources[iS]),3,Listener,Geometry))
                if Reverb_on == True :
                    Srev = (rev(Geometry,Listener,(Sources[iS]),50))
                    Srev1.append((Srev)[0]*Factor)
                    Srev2.append((Srev)[1]*Factor)
                    Str.append((Srev)[2])
                    atr.append((Srev)[2])
                    totrev.append(Srev[0]+Srev[1])
                ManV.append(volm(Sources[iS]))
                rdm.append(Sources[iS][4])   
            if Reverb_on is True :
                for i in range(0,len(atr)) :
                    RTsource.append(round(atr[i]/1000,1))
                    Revinfo.append(str(round(atr[i]/1000,1))+'sec // mix : '+str(totrev[i]*Factor)+'%')
            else :
                RTsource.append('No RT: Reverb is disabled')
                Revinfo.append('No infos: Reverb is disabled')
            io = int((len(Sources)-1))
            i_msg = []
            iosc = []
            for i in range(10):
                try:
                    pathold = oldpath[i]
                except IndexError :
                    oldpath.insert(i,["empty"])
                except NameError :
                    oldpath = []
                    oldpath.append(["empty"])
                iport = (57100+i)
                iosc.append(OSC.OSCClient())
                iosc[i].connect(("127.0.0.1",iport))
                i_msg.append(OSC.OSCMessage())
                if i <= io :
                    i_msg[i].append(SDi[i][0])
                    i_msg[i].append(SDi[i][1])
                    i_msg[i].append(SPa[i])
                    i_msg[i].append(SPan[i])
                    if Lock is True :
                        i_msg[i].append(0)
                    else :
                        if ((i_msg[i])[2]) != (oldpath[i]) :
                            i_msg[i].append(1)
                        else :
                            i_msg[i].append(2)
                        i_msg[i].append(Sint[i])
                    
                    try :
                        i_msg[i].append(Srev1[i])
                        i_msg[i].append(Srev2[i])
                        i_msg[i].append(Str[i])
                    except :
                        i_msg[i].append(0)
                        i_msg[i].append(0)
                        i_msg[i].append(0)
                    i_msg[i].append(ManV[i])
                    i_msg[i].append(rdm[i])
                    iosc[i].send(i_msg[i])
                    oldpath[i] = SPa[i]
        
                else :
                    i_msg[i].append(-127)
                    i_msg[i].append(0)
                    i_msg[i].append('/i/NoSource')
                    i_msg[i].append(0)
                    i_msg[i].append(0)
                    i_msg[i].append(0)
                    i_msg[i].append(0)
                    i_msg[i].append(0)
                    i_msg[i].append(0)
                    i_msg[i].append(0)
                    i_msg[i].append(0)
        
                try :
                    iosc[i].send(i_msg[i])
                except :
                    self.AddRuntimeMessage(ero, 'Connexion Failed, please ensure APP is open (use launcher) then reset the engine (with lock/unlock)')
                    self.Message = 'Connexion Failure'
                print "message, source {} : {}".format(i,i_msg[i])
        if __name__ == "__main__":
            main()
            RT_bySource = RTsource
            Revinfo_bySource = Revinfo
        return (Vi, RT_bySource, Revinfo_bySource)
