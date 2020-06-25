def makeSmoothCode(layers,startfunctionID,startZvalue=0.0):
    print "		M13"
    for i in range(layers):
        print "		%s [P114>=%.1f] * [P114<%.1f]"%(["$IF","$ELSEIF"][i>0],i+startZvalue,i+startZvalue+1)
        print "			#CALL %d.NC"%(startfunctionID+i)
    print "		$ENDIF"
def makeSmoothCodeIntoFile(endZvalue,startfunctionID,startZvalue=0.0, thickness=1):
    f=open('d:\output.txt','w')
    text=''
    text+="		M13\n"
    layers=(int)((endZvalue-startZvalue)/thickness)
    for i in range(layers):
        text+="		%s [P114>=%.1f] * [P114<%.1f]\n"%(["$IF","$ELSEIF"][i>0],i*thickness+startZvalue,(i+1)*thickness+startZvalue)
        text+="			#CALL %d.NC\n"%(startfunctionID+i)
    text+="		$ENDIF\n"
    f.write(text)
    f.close()


def makePatchCode(layers, startfunctionID,ifchangeflag = True,startZvalue=0.0):
    for i in range(layers):
        print "		%s [P114>=%.1f] * [P114<%.1f]" % (["$IF", "$ELSEIF"][i > 0], i+startZvalue, i+startZvalue + 1)
        print "			$IF [P213==1]"
        print "				#CALL %d.NC" % (startfunctionID + i + layers * 0)
        if ifchangeflag:print "				P213=2"
        print "			$ELSEIF [P213==2]"
        print "				#CALL %d.NC" % (startfunctionID + i + layers * 2)
        if ifchangeflag:print "				P213=3"
        print "			$ELSEIF [P213==3]"
        print "				#CALL %d.NC" % (startfunctionID + i + layers * 1)
        if ifchangeflag:print "				P213=4"
        print "			$ELSEIF [P213==4]"
        print "				#CALL %d.NC" % (startfunctionID + i + layers * 3)
        if ifchangeflag:print "				P213=1"
        print "			$ENDIF"
    print "		$ENDIF"
def makePatchCodeIntoFile(endZvalue, startfunctionID,ifchangeflag = True,startZvalue=0.0,thickness=1):
    f=open('d:\output.txt','w')
    text=''
    layers=(int)((endZvalue-startZvalue)/thickness)
    for i in range(layers):
        text += "		%s [P114>=%.1f] * [P114<%.1f]\n" % (["$IF", "$ELSEIF"][i > 0], i*thickness+startZvalue, (i+1)*thickness+startZvalue)
        text += "			$IF [P213==1]\n"
        text += "				#CALL %d.NC\n" % (startfunctionID + i + layers * 0)
        if ifchangeflag:text += "				P213=2\n"
        text += "			$ELSEIF [P213==2]\n"
        text += "				#CALL %d.NC\n" % (startfunctionID + i + layers * 2)
        if ifchangeflag:text += "				P213=3\n"
        text += "			$ELSEIF [P213==3]\n"
        text += "				#CALL %d.NC\n" % (startfunctionID + i + layers * 1)
        if ifchangeflag:text += "				P213=4\n"
        text += "			$ELSEIF [P213==4]\n"
        text += "				#CALL %d.NC\n" % (startfunctionID + i + layers * 3)
        if ifchangeflag:text += "				P213=1\n"
        text += "			$ENDIF\n"
    text += "		$ENDIF\n"

    f.write(text)
    f.close()


    
def makeEmptyNCFile(CNCSYS,FunNOList):
    # print FunNOList
    # print "		$ENDIF"
    if CNCSYS==8070:
        for i in FunNOList:
            print "(EMPTY FUNCTION)"
            print "%%L %4d"% i
            print "#RET\n"
    elif CNCSYS==8055:
        for i in FunNOList:
            print ";EMPTY FUNCTION"
            print "(SUB %4d)"% i
            print "(RET)\n"

def makePositiveOverlapCode(layers, startfunctionID, ifchangeflag=True, startZvalue=0.0):
    for i in range(layers):
        print "     %s [P114>=%.1f] * [P114<%.1f]" % (["$IF", "$ELSEIF"][i > 0], i+startZvalue, i+startZvalue + 1)
        print "         $IF [P110==1] * [P111==1] * [P113==1]"
        print "             $IF [P200 == 1] * [P112==1]"
        print "                 #CALL %d.NC" % (startfunctionID + i + layers * 8)
        print "             $ENDIF"
        print "             #CALL %d.NC" % (startfunctionID + i + layers * 0)
        print "             $IF [P200 == 1] * [P112==0]"
        print "                 #CALL %d.NC" % (startfunctionID + i + layers * 8)
        print "             $ENDIF"
        if ifchangeflag:
            print "             P110=2"
            print "             P111=1"
            print "             P113=1"

        print "         $ELSEIF [P110==2] * [P111==1] * [P113==1]"
        print "             $IF [P200 == 1] * [P112==1]"
        print "                 #CALL %d.NC" % (startfunctionID + i + layers * 9)
        print "             $ENDIF"
        print "             #CALL %d.NC" % (startfunctionID + i + layers * 4)
        print "             $IF [P200 == 1] * [P112==0]"
        print "                 #CALL %d.NC" % (startfunctionID + i + layers * 9)
        print "             $ENDIF"
        if ifchangeflag:
            print "             P110=1"
            print "             P111=2"
            print "             P113=1"

        print "         $ELSEIF [P110==1] * [P111==2] * [P113==1]"
        print "             $IF [P200 == 1] * [P112==1]"
        print "                 #CALL %d.NC" % (startfunctionID + i + layers * 8)
        print "             $ENDIF"
        print "             #CALL %d.NC" % (startfunctionID + i + layers * 1)
        print "             $IF [P200 == 1] * [P112==0]"
        print "                 #CALL %d.NC" % (startfunctionID + i + layers * 8)
        print "             $ENDIF"
        if ifchangeflag:
            print "             P110=2"
            print "             P111=2"
            print "             P113=1"

        print "         $ELSEIF [P110==2] * [P111==2] * [P113==1]"
        print "             $IF [P200 == 1] * [P112==1]"
        print "                 #CALL %d.NC" % (startfunctionID + i + layers * 9)
        print "             $ENDIF"
        print "             #CALL %d.NC" % (startfunctionID + i + layers * 5)
        print "             $IF [P200 == 1] * [P112==0]"
        print "                 #CALL %d.NC" % (startfunctionID + i + layers * 9)
        print "             $ENDIF"
        if ifchangeflag:
            print "             P110=1"
            print "             P111=1"
            print "             P113=2"

        print "         $ELSEIF [P110==1] * [P111==1] * [P113==2]"
        print "             $IF [P200 == 1] * [P112==1]"
        print "                 #CALL %d.NC" % (startfunctionID + i + layers * 8)
        print "             $ENDIF"
        print "             #CALL %d.NC" % (startfunctionID + i + layers * 2)
        print "             $IF [P200 == 1] * [P112==0]"
        print "                 #CALL %d.NC" % (startfunctionID + i + layers * 8)
        print "             $ENDIF"
        if ifchangeflag:
            print "             P110=2"
            print "             P111=1"
            print "             P113=2"

        print "         $ELSEIF [P110==2] * [P111==1] * [P113==2]"
        print "             $IF [P200 == 1] * [P112==1]"
        print "                 #CALL %d.NC" % (startfunctionID + i + layers * 9)
        print "             $ENDIF"
        print "             #CALL %d.NC" % (startfunctionID + i + layers * 6)
        print "             $IF [P200 == 1] * [P112==0]"
        print "                 #CALL %d.NC" % (startfunctionID + i + layers * 9)
        print "             $ENDIF"
        if ifchangeflag:
            print "             P110=1"
            print "             P111=2"
            print "             P113=2"

        print "         $ELSEIF [P110==1] * [P111==2] * [P113==2]"
        print "             $IF [P200 == 1] * [P112==1]"
        print "                 #CALL %d.NC" % (startfunctionID + i + layers * 8)
        print "             $ENDIF"
        print "             #CALL %d.NC" % (startfunctionID + i + layers * 3)
        print "             $IF [P200 == 1] * [P112==0]"
        print "                 #CALL %d.NC" % (startfunctionID + i + layers * 8)
        print "             $ENDIF"
        if ifchangeflag:
            print "             P110=2"
            print "             P111=2"
            print "             P113=2"

        print "         $ELSEIF [P110==2] * [P111==2] * [P113==2]"
        print "             $IF [P200 == 1] * [P112==1]"
        print "                 #CALL %d.NC" % (startfunctionID + i + layers * 9)
        print "             $ENDIF"
        print "             #CALL %d.NC" % (startfunctionID + i + layers * 7)
        print "             $IF [P200 == 1] * [P112==0]"
        print "                 #CALL %d.NC" % (startfunctionID + i + layers * 9)
        print "             $ENDIF"
        if ifchangeflag:
            print "             P110=1"
            print "             P111=1"
            print "             P113=1"
        print "         $ENDIF"
    print "     $ENDIF"

def getBlockDistance(L,W=30,w=6):
	num = round(1.0*(L+w)/W)
	return "Block Width:%.4f, Block Number: %d"%((L+w)/num-w, num)