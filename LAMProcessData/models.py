# -*- coding: gbk -*-

from django.contrib.auth.models import User
from django.db import models
# from django.db.models.signals import pre_delete
# from django.dispatch.dispatcher import receiver

# Create your models here.

'''框架表'''
# print('start models.py')
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
    Category_name = models.CharField(max_length=10, unique=True)
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
    rawstock_supplier =models.CharField(max_length=30, null=True, blank=True)
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
        return "%s [%s]"%(self.product_code, self.product_category)


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

# 激光成形参数包
class LAMProcessParameters(models.Model):
    # 工序实例中以外键引用本类，参数包可对应多个工序实例
    # 参数包名称
    name = models.CharField(max_length=40, unique=True)
    # 若干条件单元
    conditional_cell = models.ManyToManyField(LAMProcessParameterConditionalCell, related_name='CondCell_Parameter', blank=True)
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
    def __str__(self):
        return "%s [%d-%s-%s]"%(self.technique_instruction,self.serial_number, self.serial_worktype, self.serial_note)


# 激光成形生产任务
class LAMProcessMission(models.Model):
    # 产品实例
    LAM_product = models.ForeignKey(LAMProduct, on_delete=models.CASCADE)
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
        return "%s [%s - %s] %s"%(self.LAM_product.product_code,self.work_section, self.LAM_techinst_serial, self.arrangement_date)






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


'''流水表'''
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
    # 回料日期
    retrieve_time = models.DateField(null=True, blank=True)
    # 未用原材料数量 仅对粉末有效
    raw_stock_unused_amount = models.FloatField(null=True, blank=True)
    # 回收一级粉末数量 仅对粉末有效
    raw_stock_primaryretrieve_amount = models.FloatField(null=True, blank=True)
    # 回收二级粉末数量 仅对粉末有效
    raw_stock_secondaryretrieve_amount = models.FloatField(null=True, blank=True)
    # 是否有效
    available = models.BooleanField(default=True)



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
    # 产品实例
    LAM_product = models.ForeignKey(LAMProduct, on_delete=models.CASCADE, null=True)
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
    # 化学成分测试
    chemicaltest = models.ManyToManyField(ChemicalTest, blank=True)
        # models.ForeignKey(ChemicalTest, on_delete=models.DO_NOTHING, null=True, blank=True)

    # 是否有效
    available = models.BooleanField(default=True)

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
    process_mission = models.OneToOneField(LAMProcessMission, on_delete=models.DO_NOTHING, null=True)
    # 开始时间
    process_start_time = models.DateTimeField(null=True, blank=True)
    # 结束时间
    process_finish_time = models.DateTimeField(null=True, blank=True)
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


class Process_Realtime_FineData_By_WorkSectionID(models.Model):
    # 获取的时间戳
    acquisition_timestamp = models.PositiveIntegerField(unique=True)
    # 获取的时间str
    acquisition_datetime = models.DateTimeField(null=True, blank=True)
    # 氧含量
    oxygen_value = models.FloatField(null=True)
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

    class Meta:
        abstract = True
        index_together = ['process_mission', 'acquisition_timestamp']

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

class LAMProcess_Worksection_Operate(models.Model):
    # 任务信息
    process_mission = models.ForeignKey(LAMProcessMission, on_delete=models.DO_NOTHING, null=True, blank=True)
    # 获取的时间戳
    acquisition_timestamp = models.PositiveIntegerField(unique=True)
    # 操作
    operate_information = models.CharField(max_length=50, null=True)
    # 操作者
    # https://www.cnblogs.com/wcwnina/p/9246228.html
    operator = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)


# 检出成形过程数据中不符合工艺参数包的记录
class Process_Inspect_FineData_DiscordantRecords(models.Model):
    # 任务信息
    process_mission = models.ForeignKey(LAMProcessMission, on_delete=models.DO_NOTHING, null=True, blank=True)
    # 不符合阶段开始时间戳
    start_timestamp = models.PositiveIntegerField(unique=True)
    # 不符合阶段结束时间戳
    finish_timestamp = models.PositiveIntegerField(unique=True)
    # 不符合条目
    parameter_conditionalcell = models.ForeignKey(LAMProcessParameterConditionalCell, on_delete=models.DO_NOTHING, null=True, blank=True)
    # 实际值
    parameter_realvalue = models.CharField(max_length=50, null=True)



# @receiver(pre_delete, sender=CNCProcessStatus)
# def file_delete(sender, instance, **kwargs):
#     # Pass false so FileField doesn't save the model.
#     # print('进入文件删除方法，删的是',instance.alter_file)
#     instance.file.delete(False)





# print('end models.py')