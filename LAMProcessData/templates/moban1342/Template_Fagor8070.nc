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

(Variable declaration ��������)
(using parameter number ʹ�ñ�����: 101~112, 115~119, 136~139, 179~185, 191~209)
(==================================================)
P102=1000 (SCANNING VELOCITY ֱ��ɨ������)
P104=1200 (CORNER SPD ֱ��ΪX����ʱ���ɨ������)
P103=1200 (CORNER SPD ֱ��ΪY����ʱ���ɨ������)
P105=800 (SIDE SPD ֱ��ΪX����ʱ�ߵ�ɨ������)
P101=800 (SIDE SPD ֱ��ΪY����ʱ�ߵ�ɨ������)
P109=2000 (IN POSITION SPD ��λ�ƶ�����)
(----------------------------------------------)
P136=800 (Color Spd Red ��ɫ-��ɫ�߶�ɨ������)
P137=800 (Color Spd Green ��ɫ-��ɫ�߶�ɨ������)
P138=800 (Color Spd Blue ��ɫ-��ɫ�߶�ɨ������)
P139=800 (Color Spd Yellow ��ɫ-��ɫ�߶�ɨ������)
(----------------------------------------------)
P181=7250 (SET LASER POWER �趨����������)
P185=P181*0.77 (Controlled Laser Power ���Ӹ���ɨ��ʱ���Ƽ���������)
P184=0.5 (Laser On Stay Time ���⿪����ͣʱ��)
P187=15 (POWDER TIME ��·ͨ��ͣ��ʱ��)
P191=0.7 (Z-INCREMENT �������߶�)
P192=15 (IN POSITION Z UP ��λʱ����Z����λ���ٽ�Z����һ������Z�������߶�)
(----------------------------------------------)
P112=0 (Supplement Sup Before Fill Flag ����-���ǰ������ʶ��ֵȡ1ʱ�Ƚ��бߵ���������������ȡ0ʱ������������ٽ��бߵ�����)
P195=0 (SUPPLEMENT Z DOWN 	����-�ߵ�����ʱZ���½��߶ȣ�ȡ��ֵ)
P200=0 (SUPPLEMENT OUTLINE SWITCH ����-�����������в����Ŀ��أ�ֵȡ1ʱ���бߵ�����)
P115=800 (SUPPLEMENT OUTLINE SPD ����-�����������в�����ɨ������)
(----------------------------------------------)
(P110=1) (Block Type Flag ��ͬ�ֿ鷽ʽ�ı�ʶ��ȡֵ1��2����������ǰ�ֶ�����ȫ�ֱ�����ȱʡֵ1)
(P111=1) (Track Type Flag ��ͬ��㿪ʼ�켣�ı�ʶ������ӡ�����ɨ��ȡֵ1��2�������ȡֵ1��2��3��4����������ǰ�ֶ�����ȫ�ֱ�����ȱʡֵ1)
P186={{ Cooldown_Time }} (Cool down time ��ȴʱ��)
P179=0 (Actual Start Z ��ʵ��ʼZ�߶�ֵ���״����иó���ǰ��ȷ���ò���������ִ��ʱͨ�������Ϊ��һ������������Ϻ��ʵ��Z�߶�ֵ���ó���һ����ʼ���в�Ӧ���޸ĸò���ֵ)
(��ģ��У��ʱ�ɽ�P179��ΪV.A.PPOS.Z������ֻҪZ�ƶ���Χ��λ������λ�ڿ�������λ�ý���У��)
P180=P179-0 (Delta Z ��ʵ��ʼZ�߶���������ʼZ�߶�֮��Ĳ�ֵ��)
(==================================================)
P211=4 (Patch Cycle Times ����������ѭ������)
P212=1 (Patch Current Time ���������ĵ�ǰ�ܴ�)
(P213=1) (Patch Flag �Ը���ӽ��е�����������ͬ�ֿ顢��ͬ���ı�ʶ��ȡ1��2��3��4��������P110��P111������)

(Main program �������)
(==================================================)
#PATH [{{ Program_SubFunctionPath }}]

G73 (Clear Rotation ������ܴ��ڵ�ģ̬��תָ��)
G10 (Clear Mirror ������ܴ��ڵ�ģ̬����ָ��)

G05

{% if Powder_On_Throughout %}
SP181 M3
{{ Powder_On_Order }}
G04 KP187
{% endif %}

(#EXPORT)
P182={{ START_Z_VALUE }}+P180 (START Z ����V.A.PPOS.Z�Զ��жϳ�����û���ֹ-����ʵ��ʼZ�߶��������Z�߶�����)
P183={{ FINISH_Z_VALUE }}+P180 (END Z ����V.A.PPOS.Z�Զ��жϳ�����û���ֹ-����ʵ��ʼZ�߶��������Z�߶�����)
$IF [V.A.PPOS.Z >=P182] * [V.A.PPOS.Z < P183]
	$DO
		(#PREVIEW)
		P114=V.A.PPOS.Z
		$IF [V.A.PPOS.Z >=P182+10]
			P192 = 0
		$ENDIF
		(��������ȴ�趨ʱ��Ҫ���ÿ���)
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
    (2���� �͹���ɨ�¿ڸ���)
    ({{_func.note}})
    $IF [P114>={{ _func.start_z_value }}] * [P114<{{ _func.finish_z_value }}]
      {{ Powder_Off_Order }}
      G04 KP187
      SP185 M3
      #CALL {{ _func.name }}
      (������������г����켣 �� ��������޳����켣����������ȴ�趨ʱ�� ��Ҫ���ÿ���)
      {% if _func.PowderTurnOn %}
      {{ Powder_On_Order }}
      G04 KP187
      SP181 M3
      {% endif %}
    $ENDIF

    {% elif _func.type_code=='6' %}
    (N���� ���ڲ�������)
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
		(��������ȴ�趨ʱ��Ҫ���ùط�)
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