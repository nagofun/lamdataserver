# -*- coding: gbk -*-

from django.contrib.auth.models import User
from django.db import models
from lamdataserver.settings import ANALYSE_CNCDATA_URL, ANALYSE_ACCUMULATEDATA_URL, MEDIA_DefectPicture_URL, MEDIA_ReviewSheet_URL,MEDIA_LAMOperationPicture_URL, MEDIA_DingDingRecordPicture_URL
from django.db.models import Aggregate, CharField
# from django.db.models.signals import pre_delete
# from django.dispatch.dispatcher import receiver

# Create your models here.
# CNCStatus_Choice=(
#     (0, 'Windows界面'),
#     (1, '自动界面，正在运行或刀具检查'),
#     (2, '自动界面，未运行'),
#     (3, '手动界面，')
# )
'''框架表'''
# print('start models.py')

class GroupConcat(Aggregate):
    function = 'GROUP_CONCAT'
    template = '%(function)s(%(distinct)s%(expressions)s%(ordering)s%(separator)s)'

    def __init__(self, expression, distinct=False, ordering=None, separator=',', **extra):
        super(GroupConcat, self).__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            ordering=' ORDER BY %s' % ordering if ordering is not None else '',
            separator=' SEPARATOR "%s"' % separator,
            output_field=CharField(),
            **extra
        )

class ModulePermission(models.Model):
    class Meta:
        permissions = (
            ("SystemInformation", u"基础信息"),
            ("Technique", u"技术管理"),
            ("Quality", u"质量管理"),
            ("Manufacture", u"生产管理"),
            ("Operator_LAM", u"激光成形操作者"),
            ("Operator_HT", u"热处理操作者"),
            ("Operator_STOREROOM", u"库房管理者"),
            ("Operator_INSP", u"检验者"),
        )



# 厂房
class Workshop(models.Model):
    # 名称
    name = models.CharField(max_length=30, unique=True)
    # 代号
    code = models.CharField(max_length=10, unique=True)
    # 是否有效
    available = models.BooleanField(default=True)
    def __str__(self):
        return self.name

# 计算机
class Computer(models.Model):
    # 电脑名称
    name = models.CharField(max_length=30, null=True)
    # 型号
    model_number = models.CharField(max_length=30, null=True)
    # 设备编号
    device_Number = models.CharField(max_length=30, null=True)
    # 物理地址
    mac_address = models.CharField(max_length=17)
    # 是否有效
    available = models.BooleanField(default=True)
    def __str__(self):
        return self.name

# 工段
class Worksection(models.Model):
    # 工段名称
    name = models.CharField(max_length=30, unique=True)
    # 工段代号
    code = models.CharField(max_length=10, unique=True)
    # 厂房
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    # oxygen_analyzer = models.ForeignKey(Oxygenanalyzer)
    # 计算机
    desktop_computer = models.ForeignKey(Computer, related_name='desktop_computer', on_delete=models.CASCADE, null=True)
    # CNC计算机
    cnc_computer = models.ForeignKey(Computer, related_name='cnc_computer', on_delete=models.CASCADE, null=True)
    # 是否有效
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# 化学元素
class ChemicalElement(models.Model):
    # 化学元素
    element_code = models.CharField(max_length=3)
    # 化学元素
    element_name = models.CharField(max_length=4)
    # 是否有效
    available = models.BooleanField(default=True)
    def __str__(self):
        return "%s-%s"%(self.element_code, self.element_name)

# 材料
class LAMMaterial(models.Model):
    # 材料牌号
    material_code = models.CharField(max_length=20)
    # 材料名称
    material_name = models.CharField(max_length=50)
    # 名义成分
    nominal_composition = models.CharField(max_length=50, null=True)
    # 名义成分及杂质元素测试项
    chemicalelements = models.ManyToManyField(ChemicalElement)
    # 是否有效
    available = models.BooleanField(default=True)
    def __str__(self):
        return self.material_code

# 原材料类别
class RawStockCategory(models.Model):
    # 原材料类别名称
    Category_name = models.CharField(max_length=20, unique=True)
    # 是否有效
    available = models.BooleanField(default=True)
    def __str__(self):
        return self.Category_name

# 原材料台账
class RawStock(models.Model):
    # 批次号
    batch_number = models.CharField(max_length=30)
    # 材料
    material = models.ForeignKey(LAMMaterial, on_delete=models.CASCADE)
    # 原材料类别
    rawstock_category = models.ForeignKey(RawStockCategory, on_delete=models.CASCADE)
    # 供应商
    rawstock_supplier = models.CharField(max_length=30, null=True, blank=True)
    # 是否已用尽
    # use_up = models.BooleanField(default=False)
    # 是否有效
    available = models.BooleanField(default=True)
    # 入厂复验情况-化学成分 存于检测流水表内
    # 入厂复验情况-力学性能 存于检测流水表内
    def __str__(self):
        return "%s批\t%s\t%s"%(self.batch_number,self.material, self.rawstock_category)

# 激光成形产品类别
class LAMProductCategory(models.Model):
    # 图号
    drawing_code = models.CharField(max_length=30, null=True, unique=True)
    # 名称
    product_name = models.CharField(max_length=30, null=True, unique=True)
    # 代号
    product_symbol = models.CharField(max_length=10, null=True, unique=True)
    # 材料
    material = models.ForeignKey(LAMMaterial, on_delete=models.CASCADE)
    # 是否有效
    available = models.BooleanField(default=True)
    def __str__(self):
        return "%s (%s)"%(self.product_name, self.product_symbol)

# 激光成形产品
class LAMProduct(models.Model):
    # 产品类型
    product_category = models.ForeignKey(LAMProductCategory, on_delete=models.CASCADE)
    # 零件编号
    product_code = models.CharField(max_length=50, null=True, unique=True)
    # 是否有效
    available = models.BooleanField(default=True)
    def __str__(self):
        # return "%s [%s]"%(self.product_code, self.product_category)
        return "%s"%(self.product_code)


# 激光成形参数条件单元
class LAMProcessParameterConditionalCell(models.Model):
    # 优先级别，级别数值越小，表明越基础，级别数值越大，表明越特殊
    level = models.PositiveIntegerField()
    # 本条件单元替换的低级别条件单元 models.ForeignKey('self')
    instead_Cond_Cell = models.ForeignKey('self', null=True, blank=True, verbose_name='替代条件单元', on_delete=models.CASCADE)
    # 先决条件 可传入eval()函数
    precondition = models.TextField(null=True)
    # 工艺范围描述 可传入eval()函数
    expression = models.TextField(null=True)
    '''
    {P_programname}
    {P_laser}
    {P_oxy}
    {P_x}
    {P_y}
    {P_z}
    {P_feed}
    {P_scanspd}
    {P_TimeStamp}                   该条记录的时间戳
    {Sigma} A {Until CertainTime WHILE} B {/Sigma}    当B时累加A
    # {NOW_TimeStamp}                 当前时间戳
    {Last_PowerOFF_TimeStamp}       上次停光时间（仅对停光期间有效）
    # {DeltaTime_To_Now}              至今的时间（按秒计）
    {Last_HeatTreatment_TimeStamp}  上次热处理时间
    '''
    # 简述
    comment = models.CharField(max_length=80, null=True)

    # class Meta:
    #     app_label = 'app_two'
    def __str__(self):
        return "ID%s-%s"%(self.id, self.comment)

# 激光成形参数应力累加单元
class LAMProcessParameterAccumulateCell(models.Model):
    '''
    # 假定在某一时刻i，单位秒，按分钟取整，零件最大的集中应力Fi与累加热输入P正相关，与停光散热时间加权值1*K正相关，与成形时间正相关。
    假定在某一时刻i，单位秒，按分钟取整，零件最大的集中应力Fi与累加热输入P正相关，与停光散热时间加权值1*K正相关。（暂不考虑到此时刻的成形总时间）

    # Fi=M1*∑P + M2*∑(1*K**(ti-tn)) + M3*(ti-t0)
    Fi=M1*∑P + M2*∑(1*K)
    K=I(i)/(1+e^(l*(delta_t - tm)));
        delta_t=ti-tn,
        I(i)为此时刻分钟内停光时间秒数
        ti为某时刻的时间戳，tn为累加时当时的时间戳，tm为加权系数半衰期（秒）,l为收缩系数，l增大则曲线以tm为中心收缩
    '''
    # 是否启用
    active = models.BooleanField(default=False)
    # 能量系数M1
    M1 = models.FloatField(null=True, blank=True)
    # 停光冷却系数M2
    M2 = models.FloatField(null=True, blank=True)
    # M3 = models.FloatField(null=True, blank=True)
    # 停光冷却-聚集系数l
    l = models.FloatField(null=True, blank=True)
    # 停光冷却-权重半衰期tm
    tm = models.FloatField(null=True, blank=True)
    # 报警值
    alarm_value = models.FloatField(null=True, blank=True)


# 激光成形参数包
class LAMProcessParameters(models.Model):
    # 工序实例中以外键引用本类，参数包可对应多个工序实例
    # 参数包名称
    name = models.CharField(max_length=40, unique=True)
    # 若干条件单元
    conditional_cell = models.ManyToManyField(LAMProcessParameterConditionalCell, related_name='CondCell_Parameter', blank=True)
    # 应力累加单元
    accumulate_cell = models.ForeignKey(LAMProcessParameterAccumulateCell, related_name='AccuCell_Parameter',null=True, blank=True, on_delete=models.CASCADE)
    # 简述
    comment = models.CharField(max_length=80, null=True, unique=True)
    # 是否有效
    available = models.BooleanField(default=True)
    def __str__(self):
        return "%s"%(self.name)



# 激光成形工艺文件
class LAMTechniqueInstruction(models.Model):
    # 工艺规程编号
    instruction_code = models.CharField(max_length=20)
    # 工艺规程名称
    instruction_name = models.CharField(max_length=50)
    # 版本
    version_code = models.CharField(max_length=3)
    # 版次
    version_number = models.PositiveIntegerField()
    # 有效范围：产品类别
    product_category = models.ManyToManyField(LAMProductCategory,  blank=True)
    # 有效范围：产品实例
    product = models.ManyToManyField(LAMProduct,  blank=True)

    # 是否临时
    temporary = models.BooleanField(default=False)
    # 是否归档
    filed = models.BooleanField(default=False)
    # 激光成形工序号列表
    # LAMProcess_serial_number = models.CharField(max_length=50)
    # 激光成形工序说明列表
    # LAMProcess_serial_note = models.CharField(max_length=100)
    # 是否有效
    available = models.BooleanField(default=True)
    class Meta:
        unique_together = ['instruction_code', 'version_code', 'version_number']
    def __str__(self):
        return "%s %s/%d %s"%(self.instruction_code, self.version_code, self.version_number, self.instruction_name)



# # 产品类别与工艺文件关联
# class LAMProdCate_TechInst(models.Model):
#     # 激光成形产品类别
#     lamproductcategory = models.ForeignKey(LAMProductCategory, on_delete=models.CASCADE)
#     # 激光成形工艺文件
#     lamtechniqueinstruction = models.ForeignKey(LAMTechniqueInstruction, on_delete=models.CASCADE)
#     # 是否有效
#     available = models.BooleanField(default=True)




# 激光成形过程工序类别及名称
class LAMProductionWorkType(models.Model):
    # 工序名称
    worktype_name = models.CharField(max_length=50, unique=True)
    # 是否有效
    available = models.BooleanField(default=True)
    def __str__(self):
        return "%s"%(self.worktype_name)

# 图片识别码
class PDFImageCode(models.Model):
    # _choice = (
    #     ('form_code', '表式号'),
    #     ('work_type', '工序'),
    #     ('product_code', '零件编号'),
    #     # ('drawing_code', '产品图号'),
    #     # ('instruction_code', '工艺文件编号'),
    #     # ('Nonconforming_code', '不合格品审理单编号'),
    # )
    # # 该图片的所属类别
    # img_type = models.CharField(verbose_name='图片所属类别', max_length=30, choices=_choice)
    # 图片尺寸
    image_width = models.PositiveIntegerField()
    image_height = models.PositiveIntegerField()
    # 图形哈希码
    # imagecode = models.TextField(null=True, max_length=500)
    imagecode = models.TextField(null=True)
    # 所属的工序类别
    # serial_worktype = models.ForeignKey(LAMProductionWorkType, related_name='WorkType_ImageCode', blank=True, null=True, on_delete=models.CASCADE)
    # 识别出的
    text = models.CharField(max_length=50)
    # 可现实的图片
    OriginalImage = models.ImageField(upload_to='PDFCode/OriginalImage/', null=True, blank=True)
    
    class Meta:
        index_together = ['image_width', 'image_height', 'text']
       
    

# 激光成形工序实例
class LAM_TechInst_Serial(models.Model):
    # 工艺文件
    technique_instruction = models.ForeignKey(LAMTechniqueInstruction, on_delete=models.CASCADE)
    # 工序号
    serial_number = models.PositiveIntegerField()
    # 工序名
    serial_worktype = models.ForeignKey(LAMProductionWorkType, on_delete=models.CASCADE)
    # 工序概述
    serial_note = models.CharField(max_length=50, blank=True)
    # 工序内容
    serial_content = models.CharField(max_length=200, blank=True)
    # 是否有效
    available = models.BooleanField(default=True)
    # 选定成形参数包
    process_parameter = models.ForeignKey(LAMProcessParameters, on_delete=models.CASCADE, null=True, blank=True)
    # 是否可被调度模块选择
    selectable_Scheduling = models.BooleanField(default=True)
    # 是否可被激光成形模块选择
    selectable_LAM = models.BooleanField(default=False)
    # 是否可被热处理模块选择
    selectable_HeatTreatment = models.BooleanField(default=False)
    # 是否可被检验模块选择
    selectable_PhyChemNonDestructiveTest = models.BooleanField(default=False)
    # 是否可被库房模块选择
    selectable_RawStockSendRetrieve = models.BooleanField(default=False)
    # 是否可被称重模块选择
    selectable_Weighing = models.BooleanField(default=False)

    class Meta:
        unique_together = ['technique_instruction', 'serial_number']
    def __str__(self):
        return "%s [%d-%s-%s]"%(self.technique_instruction,self.serial_number, self.serial_worktype, self.serial_note)


# 激光成形生产任务
class LAMProcessMission(models.Model):
    # 产品实例
    # LAM_product = models.ForeignKey(LAMProduct, on_delete=models.CASCADE)
    LAM_product = models.ManyToManyField(LAMProduct, related_name='Product_LAMProcessMission')
    # 激光成形工序实例
    LAM_techinst_serial = models.ForeignKey(LAM_TechInst_Serial, on_delete=models.CASCADE)
    # 成形工段
    work_section = models.ForeignKey(Worksection, on_delete=models.CASCADE)
    # Worksection_Current_LAMProcessMission
    arrangement_date = models.DateField(null=True, blank=True)
    # 完成任务日期
    completion_date = models.DateField(null=True, blank=True)
    # 是否有效
    available = models.BooleanField(default=True)
    def __str__(self):
        return "%s [%s - %s] %s"%(', '.join(list(map(lambda p:str(p), self.LAM_product.all()))),self.work_section, self.LAM_techinst_serial, self.arrangement_date)






# 数控系统屏幕界面类别
class CNCStatusCategory(models.Model):
    # 屏幕状态类别
    status_name = models.CharField(max_length=30, null=True)
    # 是否有效
    available = models.BooleanField(default=True)
    def __str__(self):
        return self.status_name

# 取样部位
class SamplingPosition(models.Model):
    # 取样部位
    PositionName = models.CharField(max_length=30, null=True)
    # 取样部位代号
    PositionCode = models.CharField(max_length=5)
    # 是否有效
    available = models.BooleanField(default=True)
    def __str__(self):
        return self.PositionName

# 取样方向
class SamplingDirection(models.Model):
    # 取样方向
    DirectionName = models.CharField(max_length=30, null=True)
    # 取样方向代号
    DirectionCode = models.CharField(max_length=5)
    # 是否有效
    available = models.BooleanField(default=True)
    def __str__(self):
        return self.DirectionName

# 热处理状态
class HeatTreatmentState(models.Model):
    # 热处理状态-名称
    heattreatmentstate_name = models.CharField(max_length=30, unique=True)
    # 是否有效
    available = models.BooleanField(default=True)
    def __str__(self):
        return self.heattreatmentstate_name
# 机械加工状态
class MachiningState(models.Model):
    # 机械加工状态-名称
    machiningstate_name = models.CharField(max_length=30, unique=True)
    # 是否有效
    available = models.BooleanField(default=True)
    def __str__(self):
        return self.machiningstate_name

'''流水表'''

# 追加发放
class RawStockSendAddition(models.Model):
    # 补发日期
    send_time = models.DateField(null = True)
    # 原材料实例
    raw_stock = models.ForeignKey(RawStock, on_delete=models.CASCADE)
    # 发放原材料数量 仅对粉末有效
    raw_stock_sent_amount = models.FloatField(null=True, blank=True)
    def __str__(self):
        return '%s(%.3f kg)'%(self.raw_stock, self.raw_stock_sent_amount)
    
# 发-回料流水
class RawStockSendRetrieve(models.Model):
    # 发料日期
    send_time = models.DateField(null = True)
    # 生产任务
    LAM_mission = models.ForeignKey(LAMProcessMission, on_delete=models.CASCADE)
    # 原材料实例
    raw_stock = models.ForeignKey(RawStock, on_delete=models.CASCADE)
    # 发放原材料数量 仅对粉末有效
    raw_stock_sent_amount = models.FloatField(null=True, blank=True)
    # 追加发放
    send_addition = models.ManyToManyField(RawStockSendAddition, related_name='RawStockSendAddition_Send', blank=True)
    # 回料日期
    retrieve_time = models.DateField(null=True, blank=True)
    # 未用原材料数量 仅对粉末有效
    raw_stock_unused_amount = models.FloatField(null=True, blank=True)
    # # 一级回收粉实例
    # raw_stock_primaryretrieve = models.ForeignKey(RawStock, related_name='RawStock_RetrieveAsPrimaryFrom',
    #                                               on_delete=models.CASCADE, null=True, blank=True)
    # 回收一级粉末数量 仅对粉末有效
    raw_stock_primaryretrieve_amount = models.FloatField(null=True, blank=True)
    # # 二级回收粉实例
    # raw_stock_secondaryretrieve = models.ForeignKey(RawStock, related_name='RawStock_RetrieveAssecondaryFrom',
    #                                                 on_delete=models.CASCADE, null=True, blank=True)
    # 回收二级粉末数量 仅对粉末有效
    raw_stock_secondaryretrieve_amount = models.FloatField(null=True, blank=True)
    # 是否有效
    available = models.BooleanField(default=True)

    def __str__(self):
        return '首次发粉日期:\t%s\n零件编号:\t%s\n成形设备:\t%s\n工艺文件\t%s\n工序:\t\t%s\n'%(self.send_time,
                                                ','.join(map(lambda product:product.product_code,self.LAM_mission.LAM_product.all())),
                                                self.LAM_mission.work_section,
                                                self.LAM_mission.LAM_techinst_serial.technique_instruction.instruction_code,
                                                self.LAM_mission.LAM_techinst_serial.serial_number
                                                     )


    
    
    
# # 粉末组批组成
# class RawStock_Powder_GroupPart(models.Model):
#     # 原材料实例
#     raw_stock = models.ForeignKey(RawStock, related_name='RawStock_GroupPart' , on_delete=models.CASCADE)
#     # 数量
#     amount = models.FloatField()
#
# # 粉末组批
# class RawStock_Powder_GroupBatch(models.Model):
#     # 原批次
#     parents_RawStock_GroupPart = models.ManyToManyField(RawStock_Powder_GroupPart, related_name='RawStockGroupPart_AsParentsBatch')
#     # 新批次
#     New_RawStock_GroupPart = models.ForeignKey(RawStock_Powder_GroupPart, related_name='RawStockGroupPart_AsNewBatch', on_delete=models.CASCADE)
#     # 组批日期
#     grouped_time = models.DateField()
#     pass



    

# 拉伸测试
class MechanicalTest_Tensile(models.Model):
    # # 测试任务
    # test_mission = models.ForeignKey(PhysicochemicalTest_Mission, on_delete=models.CASCADE)
    # 试样编号
    sample_number = models.CharField(max_length=10, null=True, blank=True)
    # 取样部位
    sampling_position = models.ForeignKey(SamplingPosition, on_delete=models.CASCADE)
    # 取样方向
    sampling_direction = models.ForeignKey(SamplingDirection, on_delete=models.CASCADE)
    # 测试温度
    test_temperature = models.FloatField(default=25, null=True, blank=True)
    # 抗拉强度 MPa
    tensile_strength = models.FloatField(null=True, blank=True)
    # 屈服强度 MPa
    yield_strength = models.FloatField(null=True, blank=True)
    # 断后延伸率 %
    elongation = models.FloatField(null=True, blank=True)
    # 断面收缩率 %
    areareduction = models.FloatField(null=True, blank=True)
    # 弹性模量 GPa
    modulus = models.FloatField(null=True, blank=True)
    # 是否有效
    available = models.BooleanField(default=True)

    # class Meta:
    def __str__(self):
        return self.sample_number


# 冲击测试
class MechanicalTest_Toughness(models.Model):
    # 试样编号
    sample_number = models.CharField(max_length=10, null=True, blank=True)
    # 取样部位
    sampling_position = models.ForeignKey(SamplingPosition, on_delete=models.CASCADE)
    # 取样方向
    sampling_direction = models.ForeignKey(SamplingDirection, on_delete=models.CASCADE)
    # 测试温度
    test_temperature = models.FloatField(default=25, null=True, blank=True)
    # 冲击韧性
    toughness = models.FloatField(null=True, blank=True)
    # 是否有效
    available = models.BooleanField(default=True)
    def __str__(self):
        return self.sample_number

class MechanicalTest_FractureToughness(models.Model):
    # 试样编号
    sample_number = models.CharField(max_length=10, null=True, blank=True)
    # 取样部位
    sampling_position = models.ForeignKey(SamplingPosition, on_delete=models.CASCADE)
    # 取样方向
    sampling_direction = models.ForeignKey(SamplingDirection, on_delete=models.CASCADE)
    # 测试温度
    test_temperature = models.FloatField(default=25, null=True, blank=True)
    # 断裂韧性
    fracturetoughness_KIC = models.FloatField(null=True, blank=True)
    # 断裂韧性
    fracturetoughness_KQ = models.FloatField(null=True, blank=True)
    # 数据有效性判定
    Effectiveness = models.BooleanField(null=True, blank=True)
    # 是否有效
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.sample_number


# 化学成分测试
class ChemicalTest_Element(models.Model):
    # ELEMENT_CHOICES = (
    #     ('Ti', 'Ti-钛'),
    #     ('Al', 'Al-铝'),
    #     ('Sn', 'Sn-锡'),
    #     ('Mo', 'Mo-钼'),
    #     ('Si', 'Si-硅'),
    #     ('Cr', 'Cr-铬'),
    #     ('Zr', 'Zr-锆'),
    #     ('V', 'V-钒'),
    #     ('Fe', 'Fe-铁'),
    #     ('Mn', 'Mn-锰'),
    #     ('C', 'C-碳'),
    #     ('H', 'H-氢'),
    #     ('O', 'O-氧'),
    #     ('N', 'N-氮'),
    # )
    # 选定元素
    element = models.ForeignKey(ChemicalElement, on_delete=models.DO_NOTHING)
    # 测定含量
    value = models.FloatField()


# 化学成分测试
class ChemicalTest(models.Model):
    # 试样编号
    sample_number = models.CharField(max_length=10, null=True, blank=True)
    # 取样部位
    sampling_position = models.ForeignKey(SamplingPosition, on_delete=models.PROTECT)
    # 元素含量
    elements = models.ManyToManyField(ChemicalTest_Element)
    def __str__(self):
        return self.sample_number



# 零件理化测试任务
class PhysicochemicalTest_Mission(models.Model):
    # 产品实例 应改为多选
    # LAM_product = models.ForeignKey(LAMProduct, on_delete=models.CASCADE, null=True)
    LAM_product = models.ManyToManyField(LAMProduct, blank=True)
    # 原材料实例
    RawStock = models.ForeignKey(RawStock, on_delete=models.CASCADE, null=True)
    # 激光成形工序实例
    LAM_techinst_serial = models.ForeignKey(LAM_TechInst_Serial, on_delete=models.CASCADE)
    # 委托日期
    commission_date = models.DateField(null=True)
    # 热处理状态
    heat_treatment_state = models.ForeignKey(HeatTreatmentState, on_delete=models.DO_NOTHING)
    # 拉伸测试
    mechanicaltest_tensile = models.ManyToManyField(MechanicalTest_Tensile, blank=True)
    # 冲击测试
    mechanicaltest_toughness = models.ManyToManyField(MechanicalTest_Toughness, blank=True)
    # 断裂韧度测试
    mechanicaltest_fracturetoughness = models.ManyToManyField(MechanicalTest_FractureToughness, blank=True)
    # 化学成分测试
    chemicaltest = models.ManyToManyField(ChemicalTest, blank=True)
        # models.ForeignKey(ChemicalTest, on_delete=models.DO_NOTHING, null=True, blank=True)

    # 是否有效
    available = models.BooleanField(default=True)


# 不合格品审理
class QualityReviewSheet(models.Model):
    # 产品实例
    LAM_product = models.ManyToManyField(LAMProduct, related_name='Product_QualityReviewSheet')
    # 工序实例
    LAM_techinst_serial = models.ForeignKey(LAM_TechInst_Serial, on_delete=models.CASCADE)
    # 开具日期
    detection_date = models.DateField(null=True)
    # 审理单文件  待更改
    file = models.FileField(upload_to='.' + MEDIA_ReviewSheet_URL, null=True)

# 零件分区
class LAMProductSubarea(models.Model):
    product_category = models.ForeignKey(LAMProductCategory, on_delete=models.CASCADE, verbose_name='产品类别')
    subarea_name = models.CharField(max_length = 20, verbose_name='分区名称')# 是否有效
    available = models.BooleanField(default=True, verbose_name='是否有效')
    def __str__(self):
        return '%s-%s'%(self.product_category.product_symbol, self.subarea_name)

class DefectPicture(models.Model):
    picture = models.ImageField(verbose_name='缺陷照片', upload_to='.'+MEDIA_DefectPicture_URL)

# 一个超声缺陷
class UTDefectInformation(models.Model):
    # 缺陷编号
    defect_number = models.CharField(max_length = 10, blank=True, null=True, verbose_name = u'编号')
    # 缺陷类型
    defect_type = models.CharField(max_length = 10,
                                choices = (('Single','单个不连续性指示'),('Multiple','多个不连续性指示'),('Strip','长条不连续性指示'),('Noise','噪声')),
                                verbose_name = u'超声缺陷类别')
    # 当量
    equivalent_hole_diameter = models.FloatField(blank=True, null=True, verbose_name = u'当量平底孔直径(mm)')
    # 辐射当量  增益调节的单位
    radiation_equivalent = models.IntegerField(blank=True, null=True, verbose_name = u'辐射当量(db)')
    # 所在分区
    product_subarea = models.ForeignKey(LAMProductSubarea, on_delete=models.CASCADE, blank=True, null=True,verbose_name = u'缺陷所在分区')
    # 半精加工状态统一坐标位置 - x
    X_coordinate = models.FloatField(blank=True, null=True, verbose_name = u'加工数模内坐标X')
    # 半精加工状态统一坐标位置 - y
    Y_coordinate = models.FloatField(blank=True, null=True, verbose_name = u'加工数模内坐标Y')
    # 半精加工状态统一坐标位置 - z
    Z_coordinate = models.FloatField(blank=True, null=True, verbose_name = u'加工数模内坐标Z')
    # 多个缺陷照片
    photos = models.ManyToManyField(DefectPicture, related_name='DefectPicture_UTDefectInfo')
    def __str__(self):
        return '%s-%s (φ%.1f%+ddb)'%(self.defect_number,
                                self.get_defect_type_display(),
                                self.equivalent_hole_diameter,
                                self.radiation_equivalent)
    

# 一个X射线缺陷
class RTDefectInformation(models.Model):
    # 缺陷编号
    defect_number =  models.CharField(max_length = 10, blank=True, null=True, verbose_name = u'编号')
    # 缺陷类型
    defect_type = models.CharField(max_length=10,
                                   choices=(('Single', '单个缺陷'), ('Group', '成组缺陷')),
                                   verbose_name=u'X射线缺陷类别')
    # 缺陷大小
    size = models.FloatField(verbose_name=u'缺陷大小(mm)')
    # 所在分区
    product_subarea = models.ForeignKey(LAMProductSubarea, on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name=u'缺陷所在分区')
    # 加工状态统一坐标位置 - x
    X_coordinate = models.FloatField(blank=True, null=True, verbose_name=u'加工数模内坐标X')
    # 加工状态统一坐标位置 - y
    Y_coordinate = models.FloatField(blank=True, null=True, verbose_name=u'加工数模内坐标Y')
    # 加工状态统一坐标位置 - z
    Z_coordinate = models.FloatField(blank=True, null=True, verbose_name=u'加工数模内坐标Z')
    # 多个缺陷照片
    photos = models.ManyToManyField(DefectPicture, related_name='DefectPicture_RTDefectInfo')
    def __str__(self):
        return '%s-%s'%(self.defect_number, self.get_defect_type_display())

# 一个荧光缺陷
class PTDefectInformation(models.Model):
    # 缺陷编号
    defect_number =  models.CharField(max_length = 10, blank=True, null=True, verbose_name = u'编号')
    # 缺陷类型
    defect_type = models.CharField(max_length=10,
                                   choices=(('Single', '单个缺陷'), ('Group', '成组缺陷')),
                                   verbose_name=u'荧光缺陷类别')
    # 所在分区
    product_subarea = models.ForeignKey(LAMProductSubarea, on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name=u'缺陷所在分区')
    # 加工状态统一坐标位置 - x
    X_coordinate = models.FloatField(blank=True, null=True, verbose_name=u'加工数模内坐标X')
    # 加工状态统一坐标位置 - y
    Y_coordinate = models.FloatField(blank=True, null=True, verbose_name=u'加工数模内坐标Y')
    # 加工状态统一坐标位置 - z
    Z_coordinate = models.FloatField(blank=True, null=True, verbose_name=u'加工数模内坐标Z')
    # 多个缺陷照片
    photos = models.ManyToManyField(DefectPicture, related_name='DefectPicture_PTDefectInfo')
    def __str__(self):
        return '%s-%s'%(self.defect_number, self.get_defect_type_display())

# 一个磁粉缺陷
class MTDefectInformation(models.Model):
    # 缺陷编号
    defect_number =  models.CharField(max_length = 10, blank=True, null=True, verbose_name = u'编号')
    # 缺陷类型
    defect_type = models.CharField(max_length=10,
                                   choices=(('Single', '单个缺陷'), ('Group', '成组缺陷')),
                                   verbose_name=u'磁粉缺陷类别')
    # 所在分区
    product_subarea = models.ForeignKey(LAMProductSubarea, on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name=u'缺陷所在分区')
    # 加工状态统一坐标位置 - x
    X_coordinate = models.FloatField(blank=True, null=True, verbose_name=u'加工数模内坐标X')
    # 加工状态统一坐标位置 - y
    Y_coordinate = models.FloatField(blank=True, null=True, verbose_name=u'加工数模内坐标Y')
    # 加工状态统一坐标位置 - z
    Z_coordinate = models.FloatField(blank=True, null=True, verbose_name=u'加工数模内坐标Z')
    # 多个缺陷照片
    photos = models.ManyToManyField(DefectPicture, related_name='DefectPicture_MTDefectInfo')
    def __str__(self):
        return '%s-%s'%(self.defect_number, self.get_defect_type_display())
# 无损检测
class NonDestructiveTest_Mission(models.Model):
    # 产品实例
    LAM_product = models.ForeignKey(LAMProduct, on_delete=models.CASCADE, null=True, verbose_name = u'产品编号')
    # 原材料实例
    RawStock = models.ForeignKey(RawStock, on_delete=models.CASCADE, null=True, verbose_name = u'原材料批号')
    # 激光成形工序实例
    LAM_techinst_serial = models.ForeignKey(LAM_TechInst_Serial, on_delete=models.CASCADE, verbose_name = u'检测工序')
    # 产品加工状态
    machining_state = models.ForeignKey(MachiningState, on_delete=models.CASCADE, verbose_name = u'加工状态')
    # 产品热处理状态
    heat_treatment_state = models.ForeignKey(HeatTreatmentState, on_delete=models.CASCADE, verbose_name = u'热处理状态')
    # 无损检测任务下达时间
    arrangement_date = models.DateField(null=True, blank=True, verbose_name = u'任务开始时间')
    # 完成任务日期
    completion_date = models.DateField(null=True, blank=True,  verbose_name = u'任务完成时间')
    # 是否有效
    available = models.BooleanField(default=True,  verbose_name = u'是否有效')
    # # 无损检测类别  超声、射线、荧光、磁粉
    # NDT_type = models.CharField(max_length = 8,
    #                             choices = (('UT','超声波检测'),('RT','X射线检测'),('PT','渗透检测'),('MT','磁粉检测')),
    #                             verbose_name = u'无损检测类别')
    
    # 超声检测缺陷信息
    UT_defect = models.ManyToManyField(UTDefectInformation, related_name='UTDefect_NDTMission', verbose_name = u'超声缺陷')

    # X射线检测缺陷信息
    RT_defect = models.ManyToManyField(RTDefectInformation, related_name='RTDefect_NDTMission', verbose_name = u'X射线缺陷')

    # 荧光渗透缺陷信息
    PT_defect = models.ManyToManyField(PTDefectInformation, related_name='PTDefect_NDTMission', verbose_name = u'荧光缺陷')

    # 磁粉检测缺陷信息
    MT_defect = models.ManyToManyField(MTDefectInformation, related_name='MTDefect_NDTMission', verbose_name = u'磁粉缺陷')
    

    # 超声缺陷信息 多对多 缺陷编号，所属区域，坐标位置，大小，缺陷类型，照片
    # 射线缺陷信息 多对多 缺陷编号，所属区域，坐标位置，大小，缺陷类型，照片
    # 荧光缺陷信息 多对多 缺陷编号，所属区域，坐标位置，大小，缺陷类型，照片
    # 返修次数
    rewelding_number = models.PositiveIntegerField(null=True, blank=True, verbose_name = u'返修次数')
    # 审理单 外键
    quality_reviewsheet = models.ForeignKey(QualityReviewSheet, on_delete=models.CASCADE,null=True, blank=True, verbose_name = u'不合格品审理单')
    



class Oxygendata(models.Model):
    work_section = models.ForeignKey(Worksection, on_delete=models.DO_NOTHING)
    process_mission = models.ForeignKey(LAMProcessMission, on_delete=models.DO_NOTHING, null=True)
    acquisition_time = models.DateTimeField()
    # 获取的时间戳
    acquisition_timestamp = models.PositiveIntegerField(null=True)
    oxygen_value = models.IntegerField()
    oxygen_sensor_value = models.FloatField()
    internal_pressure_value = models.FloatField()
    class Meta:
        index_together = ['work_section','process_mission','acquisition_timestamp']
    def __str__(self):
        return str(self.oxygen_value)

class Laserdata(models.Model):
    work_section = models.ForeignKey(Worksection, on_delete=models.DO_NOTHING)
    process_mission = models.ForeignKey(LAMProcessMission, on_delete=models.DO_NOTHING, null=True)
    acquisition_time = models.DateTimeField()
    # 获取的时间戳
    acquisition_timestamp = models.PositiveIntegerField( null=True)
    laser_power = models.IntegerField()
    laser_lightpath_temperature = models.FloatField()
    laser_laser_temperature = models.FloatField()

    def __str__(self):
        return str(self.laser_power)
    class Meta:
        index_together = ['work_section', 'process_mission', 'acquisition_timestamp']



# 数控系统加工过程程序运行/中断状态且auto界面下的各项参数
class CNCProcessAutoData(models.Model):
    # oxygen_analyzer = models.ForeignKey(Oxygenanalyzer)

    # work_section = models.ForeignKey(Worksection, on_delete=models.CASCADE)
    # process_mission = models.ForeignKey(LAMProcessMission, on_delete=models.CASCADE, null=True)
    # program_name = models.CharField(max_length=20, null=True)

    program_name = models.CharField(max_length=20, null=True)
    # If_Interrupted = models.BooleanField()
    # acquisition_time = models.DateTimeField(auto_now_add=True)
    # screen_image = models.ImageField(upload_to='img/%Y/%m/%d')
    X_value = models.FloatField(null=True)
    Y_value = models.FloatField(null=True)
    Z_value = models.FloatField(null=True)
    ScanningRate_value = models.FloatField(null = True)
    SReal_value = models.FloatField(null=True)
    FeedRate_value = models.IntegerField(null = True)
    GState_value = models.CharField(max_length=50, null=True)
    MState_value = models.CharField(max_length=50, null=True)


# 数控系统加工过程实时状态
class CNCProcessStatus(models.Model):
    # 工段
    work_section = models.ForeignKey(Worksection, on_delete=models.DO_NOTHING)
    # 任务号
    process_mission = models.ForeignKey(LAMProcessMission, on_delete=models.DO_NOTHING, null=True)
    # 获取的时间
    acquisition_time = models.DateTimeField(null=True)
    # 获取的时间戳
    acquisition_timestamp = models.PositiveIntegerField(null=True)
    # 截图
    screen_image = models.ImageField(upload_to='img/%Y/%m/%d', null=True, blank=True)
    # 本图片是否处理过或检查过
    if_checked = models.BooleanField(default=False)
    # 检查日期
    check_datetime = models.DateTimeField(null=True, blank=True)
    # 是否为自动界面
    if_auto_exec_intr = models.BooleanField(null=True, blank=True)
    # 是否正在运行程序
    if_exec_intr = models.BooleanField(null=True, blank=True)
    # 是否在运行程序过程中断
    if_interrupt_intr = models.BooleanField(null=True, blank=True)
    # 运行程序或中断的参数
    autodata = models.ForeignKey(CNCProcessAutoData, on_delete=models.DO_NOTHING,null=True, blank=True)
    # 数控系统屏幕界面所属类别
    status_category = models.ForeignKey(CNCStatusCategory, on_delete=models.DO_NOTHING, null=True, blank=True)
    # 选中的程序文件名
    program_name = models.CharField(max_length=20, null=True)
    # 如果正在运行程序，则复制Z高度至此
    Z_value = models.FloatField(null=True)
    class Meta:
        index_together = ['work_section', 'process_mission', 'acquisition_timestamp']



# # 临时-辅助参数表
class TemporaryParameter_ID(models.Model):
    # id号
    '''
    1: CNCProcessStatus_SendImage_MAX_ID    最大分发img的id  下一分发id为此数+1
        SELECT max(id) FROM lamdataserver.lamprocessdata_cncprocessautodata;
    2: CNCProcessStatus_NotRecoge_Min_ID    最小经识别img的id 下次查询自此数查起
        SELECT min(id) FROM lamdataserver.lamprocessdata_cncprocessstatus WHERE if_checked=0;
    3: Process_Oxygendata_Date_Worksection_indexing中整理的最新id号
    4: Process_Laserdata_Date_Worksection_indexing中整理的最新id号
    5: Process_CNCStatusdata_Date_Worksection_indexing中整理的最新id号
    6: Process_Realtime_FineData_By_WorkSectionID 的更新时间戳(秒)
    '''
    item_id = models.IntegerField(null=True)
    note = models.CharField(max_length=100, null=True)

# 根据成形过程起止时间划分激光、氧含量、CNC等参数的id信息
class Process_Mission_timecut(models.Model):
    # 任务号
    process_mission = models.OneToOneField(LAMProcessMission, related_name='Mission_Timecut', on_delete=models.DO_NOTHING, null=True)
    # 开始时间
    process_start_time = models.DateTimeField(null=True, blank=True)
    # 结束时间
    process_finish_time = models.DateTimeField(null=True, blank=True)
    # 按工序精细表id
    finedata_start_recordid = models.PositiveIntegerField(null=True, blank=True)
    finedata_finish_recordid = models.PositiveIntegerField(null=True, blank=True)
    # 激光起始元素
    # laserdata_start_item = models.ForeignKey(Laserdata, related_name='laserdata_start_item', on_delete=models.DO_NOTHING, null=True, blank=True)
    laserdata_start_recordid = models.PositiveIntegerField(null=True, blank=True)
    # 激光终止元素
    # laserdata_finish_item = models.ForeignKey(Laserdata, related_name='laserdata_finish_item', on_delete=models.DO_NOTHING, null=True, blank=True)
    laserdata_finish_recordid = models.PositiveIntegerField(null=True, blank=True)
    # 氧含量起始元素
    # oxygendata_start_item = models.ForeignKey(Oxygendata, related_name='oxygendata_start_item', on_delete=models.DO_NOTHING, null=True, blank=True)
    oxygendata_start_recordid = models.PositiveIntegerField(null=True, blank=True)
    # 氧含量终止元素
    # oxygendata_finish_item = models.ForeignKey(Oxygendata, related_name='oxygendata_finish_item', on_delete=models.DO_NOTHING, null=True, blank=True)
    oxygendata_finish_recordid = models.PositiveIntegerField(null=True, blank=True)
    # 机床状态起始元素
    # cncstatusdata_start_item = models.ForeignKey(CNCProcessStatus, related_name='cncstatusdata_start_item', on_delete=models.DO_NOTHING, null=True, blank=True)
    cncstatusdata_start_recordid = models.PositiveIntegerField(null=True, blank=True)
    # 机床状态终止元素
    # cncstatusdata_finish_item = models.ForeignKey(CNCProcessStatus, related_name='cncstatusdata_finish_item', on_delete=models.DO_NOTHING, null=True, blank=True)
    cncstatusdata_finish_recordid = models.PositiveIntegerField(null=True, blank=True)

# 记录各个工段当前所进行的任务
class Worksection_Current_LAMProcessMission(models.Model):
    # 工段
    work_section = models.OneToOneField(Worksection, on_delete=models.DO_NOTHING, null=True)
    # 选中的任务
    process_mission = models.ForeignKey(LAMProcessMission, on_delete=models.DO_NOTHING, null=True, blank=True)
    # 是否在执行任务中
    if_onwork = models.BooleanField(default=False)


# 针对氧含量数据，每日、每工段各占1行数据，内容包含氧含量数据的起止object
class Process_Oxygendata_Date_Worksection_indexing(models.Model):
    # 工段
    work_section = models.ForeignKey(Worksection, on_delete=models.DO_NOTHING)
    # 日期
    index_date = models.DateField()
    # 日期对应的整数 8位 YYYYMMDD
    index_date_int= models.IntegerField(null=True)
    # 氧含量起始元素
    # oxygendata_start_item = models.ForeignKey(Oxygendata, related_name='oxygendata_start_item', on_delete=models.DO_NOTHING, null=True, blank=True)
    data_start_id = models.PositiveIntegerField(null=True)
    # 氧含量终止元素
    # oxygendata_finish_item = models.ForeignKey(Oxygendata, related_name='oxygendata_finish_item', on_delete=models.DO_NOTHING, null=True, blank=True)
    data_finish_id = models.PositiveIntegerField(null=True)
    # 以','间隔的当天的每分钟的数据列表  str
    data_string = models.TextField(null=True)


# 针对激光数据，每日、每工段各占1行数据，内容包含激光数据的起止object
class Process_Laserdata_Date_Worksection_indexing(models.Model):
    # 工段
    work_section = models.ForeignKey(Worksection, on_delete=models.DO_NOTHING)
    # 日期
    index_date = models.DateField()
    # 日期对应的整数 8位 YYYYMMDD
    index_date_int= models.IntegerField(null=True)
    # 激光起始元素
    # laserdata_start_item = models.ForeignKey(Laserdata, related_name='laserdata_start_item', on_delete=models.DO_NOTHING, null=True, blank=True)
    data_start_id = models.PositiveIntegerField(null=True)
    # 激光终止元素
    # laserdata_finish_item = models.ForeignKey(Laserdata, related_name='laserdata_finish_item', on_delete=models.DO_NOTHING, null=True, blank=True)
    data_finish_id = models.PositiveIntegerField(null=True)
    # 以','间隔的当天的每分钟的数据列表  str
    data_string = models.TextField(null=True)


# 针对数控机床数据，每日、每工段各占1行数据，内容包含数控机床状态数据的起止object
class Process_CNCStatusdata_Date_Worksection_indexing(models.Model):
    # 工段
    work_section = models.ForeignKey(Worksection, on_delete=models.DO_NOTHING)
    # 日期
    index_date = models.DateField()
    # 日期对应的整数 8位 YYYYMMDD
    index_date_int= models.IntegerField(null=True)
    # 机床状态起始元素
    # cncstatusdata_start_item = models.ForeignKey(CNCProcessStatus, related_name='cncstatusdata_start_item', on_delete=models.DO_NOTHING, null=True, blank=True)
    data_start_id = models.PositiveIntegerField(null=True)
    # 机床状态终止元素
    # cncstatusdata_finish_item = models.ForeignKey(CNCProcessStatus, related_name='cncstatusdata_finish_item', on_delete=models.DO_NOTHING, null=True, blank=True)
    data_finish_id = models.PositiveIntegerField(null=True)
    # 以','间隔的当天的每分钟的数据列表  str
    data_string = models.TextField(null=True)


# 针对任务，按照现存的类假数据参数，以及任务过程记录中开光停光数据计算累加值，按天存入本表中
class Process_Accumulatedata_Mission(models.Model):
    # 任务信息
    process_mission = models.ForeignKey(LAMProcessMission, related_name='Mission_Accumulatedata', on_delete=models.DO_NOTHING, null=True, blank=True)
    # 存储数据 包含P, K, 等
    data_file = models.FileField(upload_to='.'+ANALYSE_ACCUMULATEDATA_URL, null=True)
    # 能量系数M1
    M1 = models.FloatField(null=True, blank=True)
    # 停光冷却系数M2
    M2 = models.FloatField(null=True, blank=True)
    # 停光冷却-聚集系数l
    l = models.FloatField(null=True, blank=True)
    # 停光冷却-权重半衰期tm
    tm = models.FloatField(null=True, blank=True)
    # # 日期
    # index_date = models.DateField()
    # # 日期对应的整数 8位 YYYYMMDD
    # index_date_int = models.IntegerField(null=True)
    # # 第一个数据为自任务开始后第几分钟
    # minute_index = models.IntegerField(null=True)
    # # (list:24*60), 列表  1分钟内开光功率累加值
    # P = models.TextField(null=True)
    # # (list:24*60), 列表  1分钟内停光秒数
    # K = models.TextField(null=True)

# 针对任务，按照现存的类假数据参数，以及任务过程记录中开光停光数据计算累加值，按天存入本表中
class Process_CNCData_Mission(models.Model):
    # 任务信息
    process_mission = models.ForeignKey(LAMProcessMission, related_name='Mission_CNCData', on_delete=models.DO_NOTHING, null=True, blank=True)
    # 存储数据 包含Z_value, layer_thickness 等
    # zip(missionid_list, productcode_list, minute_index_list, ZValue_list, _P191_list)
    zvalue_data_file = models.FileField(upload_to='.'+ANALYSE_CNCDATA_URL, null=True)
    # 存储数据 包含每分钟开光能量累计总数、每分钟停光秒数。
    accumulate_data_file = models.FileField(upload_to='.'+ANALYSE_ACCUMULATEDATA_URL, null=True)
    # # 日期
    # index_date = models.DateField()
    # # 日期对应的整数 8位 YYYYMMDD
    # index_date_int = models.IntegerField(null=True)
    # # 第一个数据为自任务开始后第几分钟
    # minute_index = models.IntegerField(null=True)
    # # (list:24*60), 列表  1分钟内Z最小值
    # Z_value = models.TextField(null=True)
    # # (list:24*60), 列表  1分钟内层厚度
    # layer_thickness = models.TextField(null=True)

class Process_CNCData_Layer_Mission(models.Model):
    # 任务信息
    process_mission = models.ForeignKey(LAMProcessMission, related_name='Mission_LayerCNCData', on_delete=models.DO_NOTHING, null=True, blank=True)
    # 存储数据 包含X_value, Y_value, Z_value, ScanSpd 等
    data_file = models.FileField(upload_to='.'+ANALYSE_CNCDATA_URL, null=True)

class Process_Realtime_FineData_By_WorkSectionID(models.Model):
    # 获取的时间戳
    acquisition_timestamp = models.PositiveIntegerField(unique=True)
    # 获取的时间str
    acquisition_datetime = models.DateTimeField(null=True, blank=True)
    # 氧含量
    oxygen_value = models.FloatField(default=-1)
    # 激光功率
    laser_power = models.IntegerField(null=True)
    # 机床信息
    X_value = models.FloatField(null=True)
    Y_value = models.FloatField(null=True)
    Z_value = models.FloatField(null=True)
    ScanningRate_value = models.FloatField(null=True)
    FeedRate_value = models.IntegerField(null=True)
    program_name = models.CharField(max_length=20, null=True)
    # 任务信息
    process_mission = models.ForeignKey(LAMProcessMission, on_delete=models.DO_NOTHING, null=True, blank=True)
    # 是否正在运行程序
    if_exec_intr = models.BooleanField(null=True, blank=True)
    # 是否在运行程序过程中断
    if_interrupt_intr = models.BooleanField(null=True, blank=True)

    class Meta:
        abstract = True
        index_together = ['process_mission', 'acquisition_timestamp', 'Z_value', 'laser_power', 'ScanningRate_value']

class Process_Realtime_FineData_By_WorkSectionID_1(Process_Realtime_FineData_By_WorkSectionID):
    pass
class Process_Realtime_FineData_By_WorkSectionID_2(Process_Realtime_FineData_By_WorkSectionID):
    pass
class Process_Realtime_FineData_By_WorkSectionID_3(Process_Realtime_FineData_By_WorkSectionID):
    pass
class Process_Realtime_FineData_By_WorkSectionID_4(Process_Realtime_FineData_By_WorkSectionID):
    pass
class Process_Realtime_FineData_By_WorkSectionID_5(Process_Realtime_FineData_By_WorkSectionID):
    pass
class Process_Realtime_FineData_By_WorkSectionID_6(Process_Realtime_FineData_By_WorkSectionID):
    pass

class OperatePicture(models.Model):
    picture = models.ImageField(verbose_name='照片', upload_to='.'+MEDIA_LAMOperationPicture_URL)

class DingDingPicture(models.Model):
    picture = models.ImageField(verbose_name='照片', upload_to='.'+MEDIA_DingDingRecordPicture_URL)

# 瞬时事件
class LAMProcess_TransientEvent(models.Model):
    '''
    修改成形参数
    更换粉嘴
    调整Z高度
    调整零点坐标
    其他
    '''
    # 获取的时间戳
    acquisition_timestamp = models.PositiveIntegerField()
    # 操作类型
    defect_type = models.CharField(max_length=2,
                                   choices=(
                                       ('1', '修改全局变量'),
                                       ('2', '调整Z高度'),
                                       ('3', '调整零点坐标'),
                                       ('4', '更换粉嘴'),
                                       ('5', '清理粉嘴'),
                                       ('6', '吹除积粉'),
                                       ('7', '更换隔挡镜'),
                                       ('0', '其他'),
                                       # ('EditParam', '修改全局变量'),
                                       # ('EditZvalue', '调整Z高度'),
                                       # ('EditZero', '调整零点坐标'),
                                       # ('ChangeNozzle', '更换粉嘴'),
                                       # ('CleanNozzle', '清理粉嘴'),
                                       # ('RemovePowder', '吹除积粉'),
                                       # ('ChangeSeptalMirror ', '更换隔挡镜'),
                                       # ('Others', '其他')
                                   ),
                                   verbose_name=u'操作类别')
    # 概述
    summary = models.CharField(max_length=200, blank=True)
# 操作与事件是否分开？

class LAMProcess_PeriodEvent(models.Model):
    '''
    局部手动减速处理
    程序修复处理
    氧含量超标，等待换气
    设备故障
    开箱处理
    其他
    '''
    # 开始时间
    start_timestamp = models.PositiveIntegerField()
    # 结束时间
    finish_timestamp = models.PositiveIntegerField(blank=True)
    # 概述
    summary = models.CharField(max_length=200, blank=True)
    


# 激光成形过程现场操作记录
class LAMProcess_Worksection_Operate(models.Model):
    # 任务信息
    process_mission = models.ForeignKey(LAMProcessMission, on_delete=models.DO_NOTHING, null=True, blank=True)
    # 获取的时间戳
    acquisition_timestamp = models.PositiveIntegerField()
    # 操作简述
    operate_information = models.CharField(max_length=100, null=True)
    # 瞬时、阶段性、周期性
    # 瞬时事件时间戳
    instant_timestamp = models.PositiveIntegerField()
    
    # 操作者
    # https://www.cnblogs.com/wcwnina/p/9246228.html
    operator = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    # 多个照片
    photos = models.ManyToManyField(OperatePicture, related_name='OperatePicture_LAMProcessOperation')

# 钉钉日志  激光成形过程事件
class LAMProcess_DingDingRecord(models.Model):
    # 填报时间
    acquisition_time = models.DateTimeField(verbose_name='时间')
    # 获取的时间戳
    acquisition_timestamp = models.PositiveIntegerField()
    # 事件描述
    description = models.TextField(null=True, blank=True, verbose_name='事件描述')
    # 日志填报人
    writer = models.CharField(max_length=30, null=True, blank=True, verbose_name='日志填报人')
    # 汇报人
    reporter = models.CharField(max_length=30, null=True, blank=True, verbose_name='汇报人')
    # 设备
    worksection_code = models.CharField(max_length=50, null=True, blank=True, verbose_name='成形工段编号')
    # 零件编号
    product_code = models.CharField(max_length=200, null=True, blank=True, verbose_name='零件编号')
    # 工段实例
    work_section = models.ForeignKey(Worksection, on_delete=models.CASCADE, null=True, blank=True, verbose_name='成形工段实例')
    # 产品实例
    product = models.ManyToManyField(LAMProduct, null=True, blank=True, verbose_name='零件实例')
    # 评论信息
    comment = models.TextField(null=True, blank=True, verbose_name='评论信息')
    # 多个照片
    photos = models.ManyToManyField(DingDingPicture, related_name='DingDingPicture_Record', verbose_name='照片')

# 检出成形过程数据中不符合工艺参数包的记录
class Process_Inspect_FineData_DiscordantRecords(models.Model):
    # 任务信息
    process_mission = models.ForeignKey(LAMProcessMission, on_delete=models.DO_NOTHING, null=True, blank=True)
    # 计算时间
    inspect_timestamp = models.PositiveIntegerField()
    # 不符合阶段开始时间戳
    start_timestamp = models.PositiveIntegerField()
    # 不符合阶段结束时间戳
    finish_timestamp = models.PositiveIntegerField()
    # 不符合条目
    parameter_conditionalcell = models.ForeignKey(LAMProcessParameterConditionalCell, on_delete=models.DO_NOTHING, null=True, blank=True)
    # # 实际值
    # parameter_realvalue = models.CharField(max_length=50, null=True)



# @receiver(pre_delete, sender=CNCProcessStatus)
# def file_delete(sender, instance, **kwargs):
#     # Pass false so FileField doesn't save the model.
#     # print('进入文件删除方法，删的是',instance.alter_file)
#     instance.file.delete(False)





# print('end models.py')