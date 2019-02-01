#This will account for the scaling, dealing with 1024 size box instead of 896
import numpy as np

def isSameVertex(l1, l2):
    if abs(float(l1[11]) - float(l2[11])) < 0.1 and abs(float(l1[12]) - float(l2[12])) < 0.1:
        return True
    else:
        return False

def indices(value, lst):
     return [i for i,x in enumerate(lst) if x==value]

def handleGroup(imageGroup):
    groups = [[0]]
    for i in range(1,len(imageGroup)): # i = 1 - 60
        sign = 0
        for g in groups: 
            if isSameVertex(imageGroup[i], imageGroup[g[0]]):
                g.append(i)  
                sign = 1
        if sign == 0:
            groups.append([i])

    coordName = imageGroup[0][0].split('@')
    coordName_star = "./bin1_ind."+format(int(coordName[0])-1,"02")+'.star' # coordName = 0000001.star
    print coordName_star
    coord = open("./bin1/particles_largevertex/"+coordName_star,'w')
    coord.write("data_\n\
\n\
loop_\n\
_rlnImageName #1 \n\
_rlnMicrographName #2 \n\
_rlnDefocusU #3 \n\
_rlnDefocusV #4 \n\
_rlnDefocusAngle #5 \n\
_rlnVoltage #6 \n\
_rlnSphericalAberration #7 \n\
_rlnAmplitudeContrast #8 \n\
_rlnOriginX #9 \n\
_rlnOriginY #10 \n\
_rlnAngleRot #11 \n\
_rlnAngleTilt #12 \n\
_rlnAnglePsi #13 \n\
_rlnCoordinateX #14\n\
_rlnCoordinateY #15\n")


    k=np.pi/180.0
    for item in groups:
        j = imageGroup[item[0]]
        (rot,tilt,psi) = np.array([float(j[10])*k,float(j[11])*k,float(j[12])*k],dtype=np.float)
        t = np.array([np.cos(psi),-np.sin(psi)],dtype=np.float)*np.sin(tilt)*224+512

        coord.write(j[0]+" "+"./"+"bin1_ind."+format(int(coordName[0])-1,"02")+".mrc ")

        coord.write(str(float(j[2]))+" ")
        coord.write(str(float(j[3]))+" ")

        for item in j[4:8]:
            coord.write(item+" ")
        new_x=int(t[0]/2-float(j[8])/2)*2-(t[0]/2-float(j[8])/2)*2
        new_y=int(t[1]/2-float(j[9])/2)*2-(t[1]/2-float(j[9])/2)*2
        coord.write(format(new_x,".3f")+" "+format(new_y,".3f")+" ")
        for item in j[10:13]:
            coord.write(item+" ")
        coord.write(str(int(t[0]/2-float(j[8])/2)*2)+' '+str(int(t[1]/2-float(j[9])/2)*2)+'\n')
    coord.close()

if __name__=='__main__':
    forg=open('all_images_i3_bin1_all_expandi3.star','r')
    fo = forg.readlines()
    i=0
    o=len(fo)

    for line in fo:
        i=i+1
        if i < 18:
            print line,
        elif i == 18:
            print "_rlnCoordinateX #14"
            print "_rlnCoordinateY #15"
            l=line.split()
            imageGroup =[l]
        else:
            l=line.split()
            
            if len(l)>0 and imageGroup[0][0] == l[0]:
                imageGroup.append(l)

                if i == o:
                    handleGroup(imageGroup)
            else:
                handleGroup(imageGroup)
                imageGroup=[l]
