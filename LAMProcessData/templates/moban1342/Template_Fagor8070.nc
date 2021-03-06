{% extends "SubWindow_base.html" %}

{% block content %}

(This Program is generated at {{ DateTime }})

{{ CustomFunctionArea }}

%{{ Program_FileCode }}
(Part: {{ Program_DrawingCode }})
(SR: {{ Program_TechInstCode }})
(CS: {{ Program_WorksectionCode }})
(NC: CNC 8070)
(CX: {{ Program_Code }})
(Pace: {{ Program_Pace }})

(Variable declaration 变量声明)
(using parameter number 使用变量号: 101~112, 115~119, 136~139, 179~185, 191~209)
(==================================================)
P102=1000 (SCANNING VELOCITY 直道扫描速率)
P104=1200 (CORNER SPD 直道为X方向时弯道扫描速率)
P103=1200 (CORNER SPD 直道为Y方向时弯道扫描速率)
P105=800 (SIDE SPD 直道为X方向时边道扫描速率)
P101=800 (SIDE SPD 直道为Y方向时边道扫描速率)
P109=2000 (IN POSITION SPD 定位移动速率)
(----------------------------------------------)
P136=800 (Color Spd Red 颜色-红色线段扫描速率)
P137=800 (Color Spd Green 颜色-绿色线段扫描速率)
P138=800 (Color Spd Blue 颜色-蓝色线段扫描速率)
P139=800 (Color Spd Yellow 颜色-黄色线段扫描速率)
(----------------------------------------------)
P181=7250 (SET LASER POWER 设定激光器功率)
P185=P181*0.77 (Controlled Laser Power 外延辅助扫描时控制激光器功率)
P184=0.5 (Laser On Stay Time 激光开光暂停时间)
P187=15 (POWDER TIME 粉路通断停留时间)
P191=0.7 (Z-INCREMENT 层提升高度)
P192=15 (IN POSITION Z UP 定位时先提Z，到位置再降Z，这一过程中Z的提升高度)
(----------------------------------------------)
P112=0 (Supplement Sup Before Fill Flag 补偿-填充前补偿标识，值取1时先进行边道补偿再走填充程序，取0时走完填充程序后再进行边道补偿)
P195=0 (SUPPLEMENT Z DOWN 	补偿-边道补偿时Z的下降高度，取正值)
P200=0 (SUPPLEMENT OUTLINE SWITCH 补偿-对外轮廓进行补偿的开关，值取1时进行边道补偿)
P115=800 (SUPPLEMENT OUTLINE SPD 补偿-对外轮廓进行补偿的扫描速率)
(----------------------------------------------)
(P110=1) (Block Type Flag 不同分块方式的标识，取值1、2。程序运行前手动设置全局变量，缺省值1)
(P111=1) (Track Type Flag 不同起点开始轨迹的标识：负搭接、轮廓扫描取值1、2；正搭接取值1、2、3、4。程序运行前手动设置全局变量，缺省值1)
P186={{ Cooldown_Time }} (Cool down time 冷却时间)
P179=0 (Actual Start Z 真实起始Z高度值。首次运行该程序前需确定该参数，连续执行时通常将其改为上一个程序运行完毕后的实际Z高度值，该程序一旦开始运行不应再修改该参数值)
(在模拟校验时可将P179设为V.A.PPOS.Z，这样只要Z移动范围仍位于软限位内可在任意位置进行校验)
P180=P179-0 (Delta Z 真实起始Z高度与名义起始Z高度之间的差值。)
(==================================================)
P211=4 (Patch Cycle Times 单独补偿的循环周期)
P212=1 (Patch Current Time 单独补偿的当前周次)
(P213=1) (Patch Flag 以负搭接进行单独补偿，不同分块、不同起点的标识，取1、2、3、4，避免与P110与P111混淆。)

(Main program 主程序段)
(==================================================)
#PATH [{{ Program_SubFunctionPath }}]

G73 (Clear Rotation 清除可能存在的模态旋转指令)
G10 (Clear Mirror 清除可能存在的模态镜像指令)

G05

{% if Powder_On_Throughout %}
SP181 M3
{{ Powder_On_Order }}
G04 KP187
{% endif %}

(#EXPORT)
P182={{ START_Z_VALUE }}+P180 (START Z 根据V.A.PPOS.Z自动判断程序调用或终止-经真实起始Z高度修正后的Z高度下限)
P183={{ FINISH_Z_VALUE }}+P180 (END Z 根据V.A.PPOS.Z自动判断程序调用或终止-经真实起始Z高度修正后的Z高度上限)
$IF [V.A.PPOS.Z >=P182] * [V.A.PPOS.Z < P183]
	$DO
		(#PREVIEW)
		P114=V.A.PPOS.Z
		$IF [V.A.PPOS.Z >=P182+10]
			P192 = 0
		$ENDIF
		(当存在冷却设定时需要设置开粉)
		{% if not Powder_On_Throughout %}
		SP181 M3
		{{ Powder_On_Order }}
		G04 KP187
		{% endif %}

		{% for _func in FunctionList %}
		{% if _func.type_code in ['1', '2', '3', '4'] %}
    ({{_func.note}})
    $IF [P114>={{ _func.start_z_value }}] * [P114<{{ _func.finish_z_value }}]
      #CALL {{ _func.name }}
    $ENDIF
    {% endif %}

    {% if _func.type_code=='5'  %}
    (2周期 低功率扫坡口根部)
    ({{_func.note}})
    $IF [P114>={{ _func.start_z_value }}] * [P114<{{ _func.finish_z_value }}]
      {{ Powder_Off_Order }}
      G04 KP187
      SP185 M3
      #CALL {{ _func.name }}
      (当本层后续还有沉积轨迹 或 本层后续无沉积轨迹但本层无冷却设定时， 需要设置开粉)
      {% if _func.PowderTurnOn %}
      {{ Powder_On_Order }}
      G04 KP187
      SP181 M3
      {% endif %}
    $ENDIF

    {% elif _func.type_code=='6' %}
    (N周期 定期补偿成形)
    ({{_func.note}})
    $IF [P212==P211]
      #CALL {{ _func.name }}
    $ENDIF

    {% endif %}
		{% endfor %}



		(Change Patch Flag)
		$IF [P212==P211]
			P212=1
		$ELSE
			P212=P212+1
		$ENDIF

		(Change Flag)
#		$IF [P110==1] * [P111==1]
#			P110=2
#			P111=1
#		$ELSEIF [P110==2] * [P111==1]
#			P110=1
#			P111=2
#		$ELSEIF [P110==1] * [P111==2]
#			P110=2
#			P111=2
#		$ELSEIF [P110==2] * [P111==2]
#			P110=1
#			P111=1
#		$ENDIF

		$IF [P110==1] * [P111==1]
			P110=2
			P111=1
		$ELSEIF [P110==2] * [P111==1]
			P110=1
			P111=2
		$ELSEIF [P110==1] * [P111==2]
			P110=2
			P111=2
		$ELSEIF [P110==2] * [P111==2]
			P110=1
			P111=3
		$ELSEIF [P110==1] * [P111==3]
			P110=2
			P111=3
		$ELSEIF [P110==2] * [P111==3]
			P110=1
			P111=4
		$ELSEIF [P110==1] * [P111==4]
			P110=2
			P111=4
		$ELSEIF [P110==2] * [P111==4]
			P110=1
			P111=1
		$ENDIF


    G91 G01 ZP191 FP109
		(当存在冷却设定时需要设置关粉)
		{% if not Powder_On_Throughout %}
		{{ Powder_Off_Order }}
		G04 KP186
		{% endif %}


		(#NEXTPREVIEW)
		
	$ENDDO V.A.PPOS.Z < P183
$ENDIF
(----------------------------------------------)

$IF [V.A.PPOS.Z >=P183] * [V.A.PPOS.Z < P183+1]
		SP181 M3
		M60
		G04 KP187
		#CALL 4049.NC
$ENDIF
(#DISEXPORT)
{{ Powder_Off_Order }}
M30
(==================================================)
{% endblock %}