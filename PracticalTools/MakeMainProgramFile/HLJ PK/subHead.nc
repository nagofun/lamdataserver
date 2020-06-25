(Sub program DEFAULT 缺省子程序段)
(using sub number 使用子程序号: 1021~1031, 1041~1048, 1051~1053, 1108~1111, 1120~1122, 1208~1211)
(==================================================)
(Vary SPD scan subs 变速扫描子程序)
(----------------------------------------------)
(New Square Wave scan sub with vary SPD)
%L 1208
(IMPROVED SQUARE-WAVE CYCLE step along X-axis 简化型直道变速扫描的弓字步循环程序，替换原1108子程序)
(SYNTAX: #PCALL 1208 A= B= C=)
(IMPORT: P0=PACE[Original P0 +/-] P1=L[Original P1 +/-] P2=P201)
G91 G01 XP0 FP103
#PCALL 1052 A=P1 B=P2 C=P102
G91 G01 XP0 FP103
#PCALL 1052 A=-P1 B=P2 C=P102
#RET
%L 1209
(IMPROVED SQUARE-WAVE CYCLE step along Y-axis  简化型直道变速扫描的弓字步循环程序，替换原1109子程序)
(SYNTAX: #PCALL 1209 A= B= C=)
(IMPORT: P0=L[Original P0 +/-] P1=PACE[Original P1 +/-] P2=P201)
#PCALL 1051 A=P0 B=P2 C=P102
G91 G01 YP1 FP104
#PCALL 1051 A=-P0 B=P2 C=P102
G91 G01 YP1 FP104
#RET
%L 1210
(IMPROVED SQUARE-WAVE CYCLE step along Y-aixs  简化型直道变速扫描的弓字步循环程序，替换原1110子程序)
(SYNTAX: #PCALL 1210 A= B= C=)
(IMPORT: P0=PACE[Original P0 +/-] P1=L[Original P1 +/-] P2=P201)
G91 G01 YP0 FP104
#PCALL 1051 A=P1 B=P2 C=P102
G91 G01 YP0 FP104
#PCALL 1051 A=-P1 B=P2 C=P102
#RET
%L 1211
(IMPROVED SQUARE-WAVE CYCLE step along X-axis  简化型直道变速扫描的弓字步循环程序，替换原1111子程序)
(SYNTAX: #PCALL 1211 A= B= C=)
(IMPORT: P0=L[Original P0 +/-] P1=PACE[Original P1 +/-] P2=P201)
#PCALL 1052 A=P0 B=P2 C=P102
G91 G01 XP1 FP103
#PCALL 1052 A=-P0 B=P2 C=P102
G91 G01 XP1 FP103
#RET
(----------------------------------------------)
(Simplified vary SPD scan sub called by sub 1208~1211)
%L 1051
(IMPROVED SCAN X REPLACE "G91 G01 X... F..." 简化型直道变速扫描子程序，沿X轴方向)
(SYNTAX: #PCALL 1051 A= B= C=)
(IMPORT: P0=L[+/-]P1=P201[=S1=S2]P2=P102[=V1=V3])
P6=233
$IF [[ABS[P0]]/P1] <= 2
	P4=1
	P6=1
$ELSEIF [[[ABS[P0]]/P1] > 2] * [[[ABS[P0]]/P1] <= 3]
	P4=P202
	P5=P1
$ELSEIF [[[ABS[P0]]/P1] > 3] * [[[ABS[P0]]/P1] <= 4]
	P4=P203
	P5=P1
$ELSEIF [[[ABS[P0]]/P1] > 4] * [[[ABS[P0]]/P1] <= 5]
	P4=P204
	P5=P1
$ELSEIF [[ABS[P0]]/P1] > 5
	P4=P205
	P5=P1
$ENDIF
P3=P2*P4
$IF [P0 >= 0] * [P6 == 233]
	#PCALL 1041 A=P0 B=P5 C=P5 D=P2 E=P3 F=P2
$ENDIF
$IF [P0 < 0] * [P6 == 233]
	#PCALL 1042 A=-P0 B=P5 C=P5 D=P2 E=P3 F=P2
$ENDIF
$IF P6 == 1
	#PCALL 1021 A=P0 B=P2
$ENDIF
#RET
%L 1052
(IMPROVED SCAN Y REPLACE "G91 G01 Y... F..." 简化型直道变速扫描子程序，沿Y轴方向)
(SYNTAX: #PCALL 1052 A= B= C=)
(IMPORT: P0=L[+/-]P1=P201[=S1=S2]P2=P102[=V1=V3])
P6=233
$IF [[ABS[P0]]/P1] <= 2
	P4=1
	P6=1
$ELSEIF [[[ABS[P0]]/P1] > 2] * [[[ABS[P0]]/P1] <= 3]
	P4=P202
	P5=P1
$ELSEIF [[[ABS[P0]]/P1] > 3] * [[[ABS[P0]]/P1] <= 4]
	P4=P203
	P5=P1
$ELSEIF [[[ABS[P0]]/P1] > 4] * [[[ABS[P0]]/P1] <= 5]
	P4=P204
	P5=P1
$ELSEIF [[ABS[P0]]/P1] > 5
	P4=P205
	P5=P1
$ENDIF
P3=P2*P4
$IF [P0 >= 0] * [P6 == 233]
	#PCALL 1043 A=P0 B=P5 C=P5 D=P2 E=P3 F=P2
$ENDIF
$IF [P0 < 0] * [P6 == 233]
	#PCALL 1044 A=-P0 B=P5 C=P5 D=P2 E=P3 F=P2
$ENDIF
$IF P6 == 1
	#PCALL 1022 A=P0 B=P2
$ENDIF
#RET
%L 1053
(IMPROVED SCAN XY REPLACE "G91 G01 X... Y... F..."  简化型直道变速扫描子程序，沿非平行坐标轴方向)
(SYNTAX: #PCALL 1053 A= B= C= D=)
(IMPORT: P0=DELTA X[+/-]P1=DELTA Y[+/-]P2=P201[=S1=S2]P3=P102[=V1=V3])
P8=233
P5=SQRT[P0*P0+P1*P1] (L)
$IF [P5/P2] <= 2
	P4=1
	P8=1
$ELSEIF [[P5/P2] > 2] * [[P5/P2] <= 3]
	P4=P202
	P7=P2
$ELSEIF [[P5/P2] > 3] * [[P5/P2] <= 4]
	P4=P203
	P7=P2
$ELSEIF [[P5/P2] > 4] * [[P5/P2] <= 5]
	P4=P204
	P7=P2
$ELSEIF [P5/P2] > 5
	P4=P205
	P7=P2
$ENDIF
P6=P3*P4
$IF [P0 > 0] * [P1 > 0] * [P8 == 233]
	#PCALL 1045 A=P0 B=P1 C=P7 D=P7 E=P3 F=P6 G=P3
$ELSEIF [P0 < 0] * [P1 > 0] * [P8 == 233]
	#PCALL 1046 A=-P0 B=P1 C=P7 D=P7 E=P3 F=P6 G=P3
$ELSEIF [P0 > 0] * [P1 < 0] * [P8 == 233]
	#PCALL 1047 A=P0 B=-P1 C=P7 D=P7 E=P3 F=P6 G=P3
$ELSEIF [P0 < 0] * [P1 < 0] * [P8 == 233]
	#PCALL 1048 A=-P0 B=-P1 C=P7 D=P7 E=P3 F=P6 G=P3
$ENDIF
$IF P8 == 1
	#PCALL 1023 A=P0 B=P1 C=P3
$ENDIF
#RET
(----------------------------------------------)
(Core vary SPD scan sub called by sub 1051~1053)
%L 1021
(Avoid unexpected spd vary X)
(SYNTAX: #PCALL 1021 A= B=)
(IMPORT: P0=L[+/-]P1=V)
G91 G01 XP0 FP1
#RET
%L 1022
(Avoid unexpected spd vary Y)
(SYNTAX: #PCALL 1022 A= B=)
(IMPORT: P0=L[+/-]P1=V)
G91 G01 YP0 FP1
#RET
%L 1023
(Avoid unexpected spd vary X Y)
(SYNTAX: #PCALL 1023 A= B= C=)
(IMPORT: P0=DELTA X[+/-]P1=DELTA Y[+/-]P2=V)
G91 G01 XP0 YP1 FP2
#RET
%L 1041
(4 Step Vary SPD Scan +X 完整直道变速扫描子程序，双过渡段四级变速，沿+X轴扫描)
(SYNTAX: #PCALL 1041 A= B= C= D= E= F=)
(IMPORT: P0=LP1=S1P2=S2P3=V1P4=V2P5=V3)
P6=P1*0.25 (S1/4)
P7=P2*0.25 (S2/4)
P8=P0-P1-P2 (L-S1-S2)
P9=[P4-P3]*0.25 (SPD Step from V1 to V2)
P10=[P5-P4]*0.25 (SPD Step from V2 to V3)
P11=P3+P9
P12=P3+2*P9
P13=P3+3*P9
P14=P4+P10
P15=P4+2*P10
P16=P4+3*P10
G91 G01 XP6 FP3
             XP6 FP11
             XP6 FP12
             XP6 FP13
             XP8 FP4
             XP7 FP14
             XP7 FP15
             XP7 FP16
             XP7 FP5
#RET
%L 1042
(4 Step Vary SPD Scan -X  完整直道变速扫描子程序，双过渡段四级变速，沿-X轴扫描)
(SYNTAX: #PCALL 1042 A= B= C= D= E= F=)
(IMPORT: P0=LP1=S1P2=S2P3=V1P4=V2P5=V3)
P6=P1*0.25 (S1/4)
P7=P2*0.25 (S2/4)
P8=P0-P1-P2 (L-S1-S2)
P9=[P4-P3]*0.25 (SPD Step from V1 to V2)
P10=[P5-P4]*0.25 (SPD Step from V2 to V3)
P11=P3+P9
P12=P3+2*P9
P13=P3+3*P9
P14=P4+P10
P15=P4+2*P10
P16=P4+3*P10
G91 G01 X-P7 FP5
             X-P7 FP16
             X-P7 FP15
             X-P7 FP14
             X-P8 FP4
             X-P6 FP13
             X-P6 FP12
             X-P6 FP11
             X-P6 FP3
#RET
%L 1043
(4 Step Vary SPD Scan +Y  完整直道变速扫描子程序，双过渡段四级变速，沿+Y轴扫描)
(SYNTAX: #PCALL 1043 A= B= C= D= E= F=)
(IMPORT: P0=LP1=S1P2=S2P3=V1P4=V2P5=V3)
P6=P1*0.25 (S1/4)
P7=P2*0.25 (S2/4)
P8=P0-P1-P2 (L-S1-S2)
P9=[P4-P3]*0.25 (SPD Step from V1 to V2)
P10=[P5-P4]*0.25 (SPD Step from V2 to V3)
P11=P3+P9
P12=P3+2*P9
P13=P3+3*P9
P14=P4+P10
P15=P4+2*P10
P16=P4+3*P10
G91 G01 YP6 FP3
             YP6 FP11
             YP6 FP12
             YP6 FP13
             YP8 FP4
             YP7 FP14
             YP7 FP15
             YP7 FP16
             YP7 FP5
#RET
%L 1044
(4 Step Vary SPD Scan -Y  完整直道变速扫描子程序，双过渡段四级变速，沿-Y轴扫描)
(SYNTAX: #PCALL 1044 A= B= C= D= E= F=)
(IMPORT: P0=LP1=S1P2=S2P3=V1P4=V2P5=V3)
P6=P1*0.25 (S1/4)
P7=P2*0.25 (S2/4)
P8=P0-P1-P2 (L-S1-S2)
P9=[P4-P3]*0.25 (SPD Step from V1 to V2)
P10=[P5-P4]*0.25 (SPD Step from V2 to V3)
P11=P3+P9
P12=P3+2*P9
P13=P3+3*P9
P14=P4+P10
P15=P4+2*P10
P16=P4+3*P10
G91 G01 Y-P7 FP5
             Y-P7 FP16
             Y-P7 FP15
             Y-P7 FP14
             Y-P8 FP4
             Y-P6 FP13
             Y-P6 FP12
             Y-P6 FP11
             Y-P6 FP3
#RET
%L 1045
(4 Step Vary SPD Scan +X+Y  完整直道变速扫描子程序，双过渡段四级变速，沿斜线扫描，终点相对起点在第一象限)
(SYNTAX: #PCALL 1045 A= B= C= D= E= F= G=)
(IMPORT: P0=DELTA XP1=DELTA YP2=S1P3=S2P4=V1P5=V2P6=V3)
P7=ATAN[P1/P0] (THETA)
P8=P2*[COS[P7]]*0.25 (S1/4 DELTA X)
P9=P2*[SIN[P7]]*0.25 (S1/4 DELTA Y)
P10=P3*[COS[P7]]*0.25 (S2/4 DELTA X)
P11=P3*[SIN[P7]]*0.25 (S2/4 DELTA Y)
P12=P0-4*P8-4*P10 (L-S1-S2 DELTA X)
P13=P1-4*P9-4*P11 (L-S1-S2 DELTA Y)
P14=[P5-P4]*0.25 (SPD Step from V1 to V2)
P15=[P6-P5]*0.25 (SPD Step from V2 to V3)
P16=P4+P14
P17=P4+2*P14
P18=P4+3*P14
P19=P5+P15
P20=P5+2*P15
P21=P5+3*P15
G91 G01 XP8 YP9 FP4
             XP8 YP9 FP16
             XP8 YP9 FP17
             XP8 YP9 FP18
             XP12 YP13 FP5
             XP10 YP11 FP19
             XP10 YP11 FP20
             XP10 YP11 FP21
             XP10 YP11 FP6                                                   
#RET
%L 1046
(4 Step Vary SPD Scan -X+Y  完整直道变速扫描子程序，双过渡段四级变速，沿斜线扫描，终点相对起点在第二象限)
(SYNTAX: #PCALL 1046 A= B= C= D= E= F= G=)
(IMPORT: P0=DELTA XP1=DELTA YP2=S1P3=S2P4=V1P5=V2P6=V3)
P7=ATAN[P1/P0] (THETA)
P8=P2*[COS[P7]]*0.25 (S1/4 DELTA X)
P9=P2*[SIN[P7]]*0.25 (S1/4 DELTA Y)
P10=P3*[COS[P7]]*0.25 (S2/4 DELTA X)
P11=P3*[SIN[P7]]*0.25 (S2/4 DELTA Y)
P12=P0-4*P8-4*P10 (L-S1-S2 DELTA X)
P13=P1-4*P9-4*P11 (L-S1-S2 DELTA Y)
P14=[P5-P4]*0.25 (SPD Step from V1 to V2)
P15=[P6-P5]*0.25 (SPD Step from V2 to V3)
P16=P4+P14
P17=P4+2*P14
P18=P4+3*P14
P19=P5+P15
P20=P5+2*P15
P21=P5+3*P15
G91 G01 X-P10 YP11 FP6
             X-P10 YP11 FP21
             X-P10 YP11 FP20
             X-P10 YP11 FP19
             X-P12 YP13 FP5
             X-P8 YP9 FP18
             X-P8 YP9 FP17
             X-P8 YP9 FP16
             X-P8 YP9 FP4
#RET
%L 1047
(4 Step Vary SPD Scan +X-Y  完整直道变速扫描子程序，双过渡段四级变速，沿斜线扫描，终点相对起点在第四象限)
(SYNTAX: #PCALL 1047 A= B= C= D= E= F= G=)
(IMPORT: P0=DELTA XP1=DELTA YP2=S1P3=S2P4=V1P5=V2P6=V3)
P7=ATAN[P1/P0] (THETA)
P8=P2*[COS[P7]]*0.25 (S1/4 DELTA X)
P9=P2*[SIN[P7]]*0.25 (S1/4 DELTA Y)
P10=P3*[COS[P7]]*0.25 (S2/4 DELTA X)
P11=P3*[SIN[P7]]*0.25 (S2/4 DELTA Y)
P12=P0-4*P8-4*P10 (L-S1-S2 DELTA X)
P13=P1-4*P9-4*P11 (L-S1-S2 DELTA Y)
P14=[P5-P4]*0.25 (SPD Step from V1 to V2)
P15=[P6-P5]*0.25 (SPD Step from V2 to V3)
P16=P4+P14
P17=P4+2*P14
P18=P4+3*P14
P19=P5+P15
P20=P5+2*P15
P21=P5+3*P15
G91 G01 XP8 Y-P9 FP4
             XP8 Y-P9 FP16
             XP8 Y-P9 FP17
             XP8 Y-P9 FP18
             XP12 Y-P13 FP5
             XP10 Y-P11 FP19
             XP10 Y-P11 FP20
             XP10 Y-P11 FP21
             XP10 Y-P11 FP6                                                   
#RET
%L 1048
(4 Step Vary SPD Scan -X-Y  完整直道变速扫描子程序，双过渡段四级变速，沿斜线扫描，终点相对起点在第三象限)
(SYNTAX: #PCALL 1048 A= B= C= D= E= F= G=)
(IMPORT: P0=DELTA XP1=DELTA YP2=S1P3=S2P4=V1P5=V2P6=V3)
P7=ATAN[P1/P0] (THETA)
P8=P2*[COS[P7]]*0.25 (S1/4 DELTA X)
P9=P2*[SIN[P7]]*0.25 (S1/4 DELTA Y)
P10=P3*[COS[P7]]*0.25 (S2/4 DELTA X)
P11=P3*[SIN[P7]]*0.25 (S2/4 DELTA Y)
P12=P0-4*P8-4*P10 (L-S1-S2 DELTA X)
P13=P1-4*P9-4*P11 (L-S1-S2 DELTA Y)
P14=[P5-P4]*0.25 (SPD Step from V1 to V2)
P15=[P6-P5]*0.25 (SPD Step from V2 to V3)
P16=P4+P14
P17=P4+2*P14
P18=P4+3*P14
P19=P5+P15
P20=P5+2*P15
P21=P5+3*P15
G91 G01 X-P10 Y-P11 FP6
             X-P10 Y-P11 FP21
             X-P10 Y-P11 FP20
             X-P10 Y-P11 FP19
             X-P12 Y-P13 FP5
             X-P8 Y-P9 FP18
             X-P8 Y-P9 FP17
             X-P8 Y-P9 FP16
             X-P8 Y-P9 FP4
#RET
(----------------------------------------------)

(Cylinder circle fill subs 圆筒圆圈-偏移方式填充子程序)
(Forward Overlap, polar coordinates 正搭接，极坐标编程)
(----------------------------------------------)
(Core subs with Supplement scan)
%L 1024
(COUNTERCLOCKWISE, FULL CIRCLE SCAN)
(SYNTAX: #PCALL 1024, A=, B=, C=, D=, E=)
(IMPORT: P0=cylinder center X,P1=cylinder center Y,)
(P2=d1,P3=d2,P4=start point rotate angle)
P6=0.5*P2 (R1)
P7=0.5*P3 (R2)
P8=P7-P6
P9=ROUND[P8/P194] (NEW PACE NUM)
P10=P8/P9 (NEW PACE)
P11=P9-1 (RPT TIMES)
G30 IP0 JP1
G90 G01 RP6 QP4 FP109
#CALL 1120
G91 G03 Q360 FP108
#CALL 1121
$FOR P12=1, P11, 1
	#PCALL 1028 A=P10 B=360
$ENDFOR
G91 G01 RP10 FP107
#CALL 1120
G91 G03 Q360 FP108
#CALL 1121
P4=P4+60 (补偿外廓起点旋转60度)
$IF P208 == 1
	#PCALL 1030 A=P6 B=360 C=P4 D=P195
$ENDIF
$IF P209 == 1
	#PCALL 1030 A=P7 B=360 C=P4 D=P195
$ENDIF
#RET
%L 1025
(CLOCKWISE, FULL CIRCLE SCAN)
(SYNTAX: #PCALL 1025, A=, B=, C=, D=, E=)
(IMPORT: P0=cylinder center X, P1=cylinder center Y,)
(P2=d1,P3=d2,P4=start point rotate angle)
P6=0.5*P2 (R1)
P7=0.5*P3 (R2)
P8=P7-P6
P9=ROUND[P8/P194] (NEW PACE NUM)
P10=P8/P9 (NEW PACE)
P11=P9-1 (RPT TIMES)
G30 IP0 JP1
G90 G01 RP6 QP4 FP109
#CALL 1120
G91 G02 Q360 FP108
#CALL 1121
$FOR P12=1, P11, 1
	#PCALL 1029 A=P10 B=360
$ENDFOR
G91 G01 RP10 FP109
#CALL 1120
G91 G02 Q360 FP108
#CALL 1121
P4=P4+60 (补偿外廓起点旋转60度)
$IF P208 == 1
	#PCALL 1031 A=P6 B=360 C=P4 D=P195
$ENDIF
$IF P209 == 1
	#PCALL 1031 A=P7 B=360 C=P4 D=P195
$ENDIF
#RET
%L 1026
(COUNTERCLOCKWISE, OVERLAP CIRCLE SCAN)
(SYNTAX: #PCALL 1026, A=, B=, C=, D=, E=)
(IMPORT: P0=cylinder center X, P1=cylinder center Y,)
(P2=d1,P3=d2,P4=start point rotate angle)
P6=0.5*P2 (R1)
P7=0.5*P3 (R2)
P8=P7-P6
P9=ROUND[P8/P194] (NEW PACE NUM)
P10=P8/P9 (NEW PACE)
P11=P9-1 (RPT TIMES)
P12=360-[[[[ABS[P10]]/P6]*180]/3.14] (SCAN ANGLE)
G30 IP0 JP1
G90 G01 RP6 QP4 FP109
#CALL 1120
G91 G03 QP12 FP108
$FOR P13=1, P11, 1
	P6=P6+P10
	P12=360-[[[[ABS[P10]]/P6]*180]/3.14]
	G91 G01 RP10 FP107
	G91 G03 QP12 FP106
$ENDFOR
P6=P6+P10
P12=360-[[[[ABS[P10]]/P6]*180]/3.14]
G91 G01 RP10 FP107
G91 G03 QP12 FP108
#CALL 1121
P4=P4+60
P6=0.5*P2
P12=360-[[[[ABS[P10]]/P6]*180]/3.14]
$IF P208 == 1
	#PCALL 1030 A=P6 B=P12 C=P4 D=P195
$ENDIF
P12=360-[[[[ABS[P10]]/P6]*180]/3.14]
$IF P209 == 1
	#PCALL 1030 A=P7 B=P12 C=P4 D=P195
$ENDIF
#RET
%L 1027
(CLOCKWISE, OVERLAP CIRCLE SCAN)
(SYNTAX: #PCALL 1027, A=, B=, C=, D=, E=)
(IMPORT: P0=cylinder center X, P1=cylinder center Y,)
(P2=d1,P3=d2,P4=start point rotate angle)
P6=0.5*P2 (R1)
P7=0.5*P3 (R2)
P8=P7-P6
P9=ROUND[P8/P194] (NEW PACE NUM)
P10=P8/P9 (NEW PACE)
P11=P9-1 (RPT TIMES)
P12=360-[[[[ABS[P10]]/P6]*180]/3.14] (SCAN ANGLE)
G30 IP0 JP1
G90 G01 RP6 QP4 FP109
#CALL 1120
G91 G02 QP12 FP108
$FOR P13=1, P11, 1
	P6=P6+P10
	P12=360-[[[[ABS[P10]]/P6]*180]/3.14]
	G91 G01 RP10 FP107
	G91 G02 QP12 FP106
$ENDFOR
P6=P6+P10
P12=360-[[[[ABS[P10]]/P6]*180]/3.14]
G91 G01 RP10 FP107
G91 G02 QP12 FP108
#CALL 1121
P4=P4+60
P6=0.5*P2
P12=360-[[[[ABS[P10]]/P6]*180]/3.14]
$IF P208 == 1
	#PCALL 1031 A=P6 B=P12 C=P4 D=P195
$ENDIF
P12=360-[[[[ABS[P10]]/P6]*180]/3.14]
$IF P209 == 1
	#PCALL 1031 A=P7 B=P12 C=P4 D=P195
$ENDIF
#RET
(----------------------------------------------)
(Circle fill sub called by sub 1024~1027)
%L 1028
(COUNTERCLOCKWISE CIRCLE SCAN)
(SYNTAX: #PCALL 1028, A=, B=)
(IMPORT: P0=radius pace [+/-], P1=scan angle)
G91 G01 RP0 FP107
#CALL 1120
G91 G03 QP1 FP106
#CALL 1121
#RET
%L 1029
(CLOCKWISE CIRCLE SCAN)
(SYNTAX: #PCALL 1029, A=, B=)
(IMPORT: P0=radius pace [+/-], P1=scan angle)
G91 G01 RP0 FP107
#CALL 1120
G91 G02 QP1 FP106
#CALL 1121
#RET
(----------------------------------------------)
(Supplement scan sub called by sub 1024~1027)
%L 1030
(CIRCLE SUPPLEMENT COUNTERCLOCKWISE)
(SYNTAX: #PCALL 1030, A=, B=, C=, D=)
(IMPORT: P0=R, P1=scan angle, P2=start point rotate angle, P3=DELTA Z)
G90 G01 RP0 QP2 FP109
G91 G01 Z-P3 FP109
#CALL 1120
G91 G03 QP1 FP115
#CALL 1121
G91 G01 ZP3 FP109
#RET
%L 1031
(CIRCLE SUPPLEMENT CLOCKWISE)
(SYNTAX: #PCALL 1031, A=, B=, C=, D=)
(IMPORT: P0=R, P1=scan angle, P2=start point rotate angle, P3=DELTA Z)
G90 G01 RP0 QP2 FP109
G91 G01 Z-P3 FP109
#CALL 1120
G91 G02 QP1 FP115
#CALL 1121
G91 G01 ZP3 FP109
#RET
(----------------------------------------------)

(Original Square Wave scan subs 原始弓字步循环子程序)
(----------------------------------------------)
%L 1108
( step along x-axis)
G91 G01 XP0 FP103
        YP1 FP102
        XP0 FP103
        Y-P1 FP102
#RET
%L 1109
( step along y-axis)
G91 G01 XP0 FP102
        YP1 FP104
        X-P0 FP102
        YP1 FP104
#RET
%L 1110
( step along y-aixs)
G91 G01 YP0 FP104
        XP1 FP102
        YP0 FP104
        X-P1 FP102
#RET
%L 1111
( step along x-axis)
G91 G01 YP0 FP102
        XP1 FP103
        Y-P0 FP102
        XP1 FP103
#RET
(----------------------------------------------)

(Laser control subs 开、关和中断光/粉子程序)
(----------------------------------------------)
%L 1120
(LASER ON)
M20
G04 K0.2
#RET
%L 1121
(LASER OFF)
G04 K0.4
M21
#RET
%L 1122
(LASER INTERBREAK)
G04 K0.4
M21
G04 KP184
M20
G04 K0.2
#RET
(==================================================)
