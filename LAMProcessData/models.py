# -*- coding: gbk -*-

from django.contrib.auth.models import User
from django.db import models
from lamdataserver.settings import ANALYSE_CNCDATA_URL, ANALYSE_ACCUMULATEDATA_URL, MEDIA_DefectPicture_URL, MEDIA_ReviewSheet_URL
from django.db.models import Aggregate, CharField
# from django.db.models.signals import pre_delete
# from django.dispatch.dispatcher import receiver

# Create your models here.
# CNCStatus_Choice=(
#     (0, 'Windows����'),
#     (1, '�Զ����棬�������л򵶾߼��'),
#     (2, '�Զ����棬δ����'),
#     (3, '�ֶ����棬')
# )
'''��ܱ�'''
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
            ("SystemInformation", u"������Ϣ"),
            ("Technique", u"��������"),
            ("Quality", u"��������"),
            ("Manufacture", u"��������"),
            ("Operator_LAM", u"������β�����"),
            ("Operator_HT", u"�ȴ��������"),
            ("Operator_STOREROOM", u"�ⷿ������"),
            ("Operator_INSP", u"������"),
        )



# ����
class Workshop(models.Model):
    # ����
    name = models.CharField(max_length=30, unique=True)
    # ����
    code = models.CharField(max_length=10, unique=True)
    # �Ƿ���Ч
    available = models.BooleanField(default=True)
    def __str__(self):
        return self.name

# �����
class Computer(models.Model):
    # ��������
    name = models.CharField(max_length=30, null=True)
    # �ͺ�
    model_number = models.CharField(max_length=30, null=True)
    # �豸���
    device_Number = models.CharField(max_length=30, null=True)
    # �����ַ
    mac_address = models.CharField(max_length=17)
    # �Ƿ���Ч
    available = models.BooleanField(default=True)
    def __str__(self):
        return self.name

# ����
class Worksection(models.Model):
    # ��������
    name = models.CharField(max_length=30, unique=True)
    # ���δ���
    code = models.CharField(max_length=10, unique=True)
    # ����
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    # oxygen_analyzer = models.ForeignKey(Oxygenanalyzer)
    # �����
    desktop_computer = models.ForeignKey(Computer, related_name='desktop_computer', on_delete=models.CASCADE, null=True)
    # CNC�����
    cnc_computer = models.ForeignKey(Computer, related_name='cnc_computer', on_delete=models.CASCADE, null=True)
    # �Ƿ���Ч
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# ��ѧԪ��
class ChemicalElement(models.Model):
    # ��ѧԪ��
    element_code = models.CharField(max_length=3)
    # ��ѧԪ��
    element_name = models.CharField(max_length=4)
    # �Ƿ���Ч
    available = models.BooleanField(default=True)
    def __str__(self):
        return "%s-%s"%(self.element_code, self.element_name)

# ����
class LAMMaterial(models.Model):
    # �����ƺ�
    material_code = models.CharField(max_length=20)
    # ��������
    material_name = models.CharField(max_length=50)
    # ����ɷ�
    nominal_composition = models.CharField(max_length=50, null=True)
    # ����ɷּ�����Ԫ�ز�����
    chemicalelements = models.ManyToManyField(ChemicalElement)
    # �Ƿ���Ч
    available = models.BooleanField(default=True)
    def __str__(self):
        return self.material_code

# ԭ�������
class RawStockCategory(models.Model):
    # ԭ�����������
    Category_name = models.CharField(max_length=20, unique=True)
    # �Ƿ���Ч
    available = models.BooleanField(default=True)
    def __str__(self):
        return self.Category_name

# ԭ����̨��
class RawStock(models.Model):
    # ���κ�
    batch_number = models.CharField(max_length=30)
    # ����
    material = models.ForeignKey(LAMMaterial, on_delete=models.CASCADE)
    # ԭ�������
    rawstock_category = models.ForeignKey(RawStockCategory, on_delete=models.CASCADE)
    # ��Ӧ��
    rawstock_supplier = models.CharField(max_length=30, null=True, blank=True)
    # �Ƿ����þ�
    # use_up = models.BooleanField(default=False)
    # �Ƿ���Ч
    available = models.BooleanField(default=True)
    # �볧�������-��ѧ�ɷ� ���ڼ����ˮ����
    # �볧�������-��ѧ���� ���ڼ����ˮ����
    def __str__(self):
        return "%s��\t%s\t%s"%(self.batch_number,self.material, self.rawstock_category)

# ������β�Ʒ���
class LAMProductCategory(models.Model):
    # ͼ��
    drawing_code = models.CharField(max_length=30, null=True, unique=True)
    # ����
    product_name = models.CharField(max_length=30, null=True, unique=True)
    # ����
    product_symbol = models.CharField(max_length=10, null=True, unique=True)
    # ����
    material = models.ForeignKey(LAMMaterial, on_delete=models.CASCADE)
    # �Ƿ���Ч
    available = models.BooleanField(default=True)
    def __str__(self):
        return "%s (%s)"%(self.product_name, self.product_symbol)

# ������β�Ʒ
class LAMProduct(models.Model):
    # ��Ʒ����
    product_category = models.ForeignKey(LAMProductCategory, on_delete=models.CASCADE)
    # ������
    product_code = models.CharField(max_length=50, null=True, unique=True)
    # �Ƿ���Ч
    available = models.BooleanField(default=True)
    def __str__(self):
        # return "%s [%s]"%(self.product_code, self.product_category)
        return "%s"%(self.product_code)


# ������β���������Ԫ
class LAMProcessParameterConditionalCell(models.Model):
    # ���ȼ��𣬼�����ֵԽС������Խ������������ֵԽ�󣬱���Խ����
    level = models.PositiveIntegerField()
    # ��������Ԫ�滻�ĵͼ���������Ԫ models.ForeignKey('self')
    instead_Cond_Cell = models.ForeignKey('self', null=True, blank=True, verbose_name='���������Ԫ', on_delete=models.CASCADE)
    # �Ⱦ����� �ɴ���eval()����
    precondition = models.TextField(null=True)
    # ���շ�Χ���� �ɴ���eval()����
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
    {P_TimeStamp}                   ������¼��ʱ���
    {Sigma} A {Until CertainTime WHILE} B {/Sigma}    ��Bʱ�ۼ�A
    # {NOW_TimeStamp}                 ��ǰʱ���
    {Last_PowerOFF_TimeStamp}       �ϴ�ͣ��ʱ�䣨����ͣ���ڼ���Ч��
    # {DeltaTime_To_Now}              �����ʱ�䣨����ƣ�
    {Last_HeatTreatment_TimeStamp}  �ϴ��ȴ���ʱ��
    '''
    # ����
    comment = models.CharField(max_length=80, null=True)

    # class Meta:
    #     app_label = 'app_two'
    def __str__(self):
        return "ID%s-%s"%(self.id, self.comment)

# ������β���Ӧ���ۼӵ�Ԫ
class LAMProcessParameterAccumulateCell(models.Model):
    '''
    # �ٶ���ĳһʱ��i����λ�룬������ȡ����������ļ���Ӧ��Fi���ۼ�������P����أ���ͣ��ɢ��ʱ���Ȩֵ1*K����أ������ʱ������ء�
    �ٶ���ĳһʱ��i����λ�룬������ȡ����������ļ���Ӧ��Fi���ۼ�������P����أ���ͣ��ɢ��ʱ���Ȩֵ1*K����ء����ݲ����ǵ���ʱ�̵ĳ�����ʱ�䣩

    # Fi=M1*��P + M2*��(1*K**(ti-tn)) + M3*(ti-t0)
    Fi=M1*��P + M2*��(1*K)
    K=I(i)/(1+e^(l*(delta_t - tm)));
        delta_t=ti-tn,
        I(i)Ϊ��ʱ�̷�����ͣ��ʱ������
        tiΪĳʱ�̵�ʱ�����tnΪ�ۼ�ʱ��ʱ��ʱ�����tmΪ��Ȩϵ����˥�ڣ��룩,lΪ����ϵ����l������������tmΪ��������
    '''
    # �Ƿ�����
    active = models.BooleanField(default=False)
    # ����ϵ��M1
    M1 = models.FloatField(null=True, blank=True)
    # ͣ����ȴϵ��M2
    M2 = models.FloatField(null=True, blank=True)
    # M3 = models.FloatField(null=True, blank=True)
    # ͣ����ȴ-�ۼ�ϵ��l
    l = models.FloatField(null=True, blank=True)
    # ͣ����ȴ-Ȩ�ذ�˥��tm
    tm = models.FloatField(null=True, blank=True)
    # ����ֵ
    alarm_value = models.FloatField(null=True, blank=True)


# ������β�����
class LAMProcessParameters(models.Model):
    # ����ʵ������������ñ��࣬�������ɶ�Ӧ�������ʵ��
    # ����������
    name = models.CharField(max_length=40, unique=True)
    # ����������Ԫ
    conditional_cell = models.ManyToManyField(LAMProcessParameterConditionalCell, related_name='CondCell_Parameter', blank=True)
    # Ӧ���ۼӵ�Ԫ
    accumulate_cell = models.ForeignKey(LAMProcessParameterAccumulateCell, related_name='AccuCell_Parameter',null=True, blank=True, on_delete=models.CASCADE)
    # ����
    comment = models.CharField(max_length=80, null=True, unique=True)
    # �Ƿ���Ч
    available = models.BooleanField(default=True)
    def __str__(self):
        return "%s"%(self.name)



# ������ι����ļ�
class LAMTechniqueInstruction(models.Model):
    # ���չ�̱��
    instruction_code = models.CharField(max_length=20)
    # ���չ������
    instruction_name = models.CharField(max_length=50)
    # �汾
    version_code = models.CharField(max_length=3)
    # ���
    version_number = models.PositiveIntegerField()
    # ��Ч��Χ����Ʒ���
    product_category = models.ManyToManyField(LAMProductCategory,  blank=True)
    # ��Ч��Χ����Ʒʵ��
    product = models.ManyToManyField(LAMProduct,  blank=True)

    # �Ƿ���ʱ
    temporary = models.BooleanField(default=False)
    # �Ƿ�鵵
    filed = models.BooleanField(default=False)
    # ������ι�����б�
    # LAMProcess_serial_number = models.CharField(max_length=50)
    # ������ι���˵���б�
    # LAMProcess_serial_note = models.CharField(max_length=100)
    # �Ƿ���Ч
    available = models.BooleanField(default=True)
    class Meta:
        unique_together = ['instruction_code', 'version_code', 'version_number']
    def __str__(self):
        return "%s %s/%d %s"%(self.instruction_code, self.version_code, self.version_number, self.instruction_name)



# # ��Ʒ����빤���ļ�����
# class LAMProdCate_TechInst(models.Model):
#     # ������β�Ʒ���
#     lamproductcategory = models.ForeignKey(LAMProductCategory, on_delete=models.CASCADE)
#     # ������ι����ļ�
#     lamtechniqueinstruction = models.ForeignKey(LAMTechniqueInstruction, on_delete=models.CASCADE)
#     # �Ƿ���Ч
#     available = models.BooleanField(default=True)




# ������ι��̹����������
class LAMProductionWorkType(models.Model):
    # ��������
    worktype_name = models.CharField(max_length=50, unique=True)
    # �Ƿ���Ч
    available = models.BooleanField(default=True)
    def __str__(self):
        return "%s"%(self.worktype_name)

# ͼƬʶ����
class PDFImageCode(models.Model):
    # _choice = (
    #     ('form_code', '��ʽ��'),
    #     ('work_type', '����'),
    #     ('product_code', '������'),
    #     # ('drawing_code', '��Ʒͼ��'),
    #     # ('instruction_code', '�����ļ����'),
    #     # ('Nonconforming_code', '���ϸ�Ʒ�������'),
    # )
    # # ��ͼƬ���������
    # img_type = models.CharField(verbose_name='ͼƬ�������', max_length=30, choices=_choice)
    # ͼƬ�ߴ�
    image_width = models.PositiveIntegerField()
    image_height = models.PositiveIntegerField()
    # ͼ�ι�ϣ��
    # imagecode = models.TextField(null=True, max_length=500)
    imagecode = models.TextField(null=True)
    # �����Ĺ������
    # serial_worktype = models.ForeignKey(LAMProductionWorkType, related_name='WorkType_ImageCode', blank=True, null=True, on_delete=models.CASCADE)
    # ʶ�����
    text = models.CharField(max_length=50)
    # ����ʵ��ͼƬ
    OriginalImage = models.ImageField(upload_to='PDFCode/OriginalImage/', null=True, blank=True)
    
    class Meta:
        index_together = ['image_width', 'image_height', 'text']
       
    

# ������ι���ʵ��
class LAM_TechInst_Serial(models.Model):
    # �����ļ�
    technique_instruction = models.ForeignKey(LAMTechniqueInstruction, on_delete=models.CASCADE)
    # �����
    serial_number = models.PositiveIntegerField()
    # ������
    serial_worktype = models.ForeignKey(LAMProductionWorkType, on_delete=models.CASCADE)
    # �������
    serial_note = models.CharField(max_length=50, blank=True)
    # ��������
    serial_content = models.CharField(max_length=200, blank=True)
    # �Ƿ���Ч
    available = models.BooleanField(default=True)
    # ѡ�����β�����
    process_parameter = models.ForeignKey(LAMProcessParameters, on_delete=models.CASCADE, null=True, blank=True)
    # �Ƿ�ɱ�����ģ��ѡ��
    selectable_Scheduling = models.BooleanField(default=True)
    # �Ƿ�ɱ��������ģ��ѡ��
    selectable_LAM = models.BooleanField(default=False)
    # �Ƿ�ɱ��ȴ���ģ��ѡ��
    selectable_HeatTreatment = models.BooleanField(default=False)
    # �Ƿ�ɱ�����ģ��ѡ��
    selectable_PhyChemNonDestructiveTest = models.BooleanField(default=False)
    # �Ƿ�ɱ��ⷿģ��ѡ��
    selectable_RawStockSendRetrieve = models.BooleanField(default=False)
    # �Ƿ�ɱ�����ģ��ѡ��
    selectable_Weighing = models.BooleanField(default=False)

    class Meta:
        unique_together = ['technique_instruction', 'serial_number']
    def __str__(self):
        return "%s [%d-%s-%s]"%(self.technique_instruction,self.serial_number, self.serial_worktype, self.serial_note)


# ���������������
class LAMProcessMission(models.Model):
    # ��Ʒʵ��
    # LAM_product = models.ForeignKey(LAMProduct, on_delete=models.CASCADE)
    LAM_product = models.ManyToManyField(LAMProduct, related_name='Product_LAMProcessMission')
    # ������ι���ʵ��
    LAM_techinst_serial = models.ForeignKey(LAM_TechInst_Serial, on_delete=models.CASCADE)
    # ���ι���
    work_section = models.ForeignKey(Worksection, on_delete=models.CASCADE)
    # Worksection_Current_LAMProcessMission
    arrangement_date = models.DateField(null=True, blank=True)
    # �����������
    completion_date = models.DateField(null=True, blank=True)
    # �Ƿ���Ч
    available = models.BooleanField(default=True)
    def __str__(self):
        return "%s [%s - %s] %s"%(', '.join(list(map(lambda p:str(p), self.LAM_product.all()))),self.work_section, self.LAM_techinst_serial, self.arrangement_date)






# ����ϵͳ��Ļ�������
class CNCStatusCategory(models.Model):
    # ��Ļ״̬���
    status_name = models.CharField(max_length=30, null=True)
    # �Ƿ���Ч
    available = models.BooleanField(default=True)
    def __str__(self):
        return self.status_name

# ȡ����λ
class SamplingPosition(models.Model):
    # ȡ����λ
    PositionName = models.CharField(max_length=30, null=True)
    # ȡ����λ����
    PositionCode = models.CharField(max_length=5)
    # �Ƿ���Ч
    available = models.BooleanField(default=True)
    def __str__(self):
        return self.PositionName

# ȡ������
class SamplingDirection(models.Model):
    # ȡ������
    DirectionName = models.CharField(max_length=30, null=True)
    # ȡ���������
    DirectionCode = models.CharField(max_length=5)
    # �Ƿ���Ч
    available = models.BooleanField(default=True)
    def __str__(self):
        return self.DirectionName

# �ȴ���״̬
class HeatTreatmentState(models.Model):
    # �ȴ���״̬-����
    heattreatmentstate_name = models.CharField(max_length=30, unique=True)
    # �Ƿ���Ч
    available = models.BooleanField(default=True)
    def __str__(self):
        return self.heattreatmentstate_name
# ��е�ӹ�״̬
class MachiningState(models.Model):
    # ��е�ӹ�״̬-����
    machiningstate_name = models.CharField(max_length=30, unique=True)
    # �Ƿ���Ч
    available = models.BooleanField(default=True)
    def __str__(self):
        return self.machiningstate_name

'''��ˮ��'''

# ׷�ӷ���
class RawStockSendAddition(models.Model):
    # ��������
    send_time = models.DateField(null = True)
    # ԭ����ʵ��
    raw_stock = models.ForeignKey(RawStock, on_delete=models.CASCADE)
    # ����ԭ�������� ���Է�ĩ��Ч
    raw_stock_sent_amount = models.FloatField(null=True, blank=True)
    def __str__(self):
        return '%s(%.3f kg)'%(self.raw_stock, self.raw_stock_sent_amount)
    
# ��-������ˮ
class RawStockSendRetrieve(models.Model):
    # ��������
    send_time = models.DateField(null = True)
    # ��������
    LAM_mission = models.ForeignKey(LAMProcessMission, on_delete=models.CASCADE)
    # ԭ����ʵ��
    raw_stock = models.ForeignKey(RawStock, on_delete=models.CASCADE)
    # ����ԭ�������� ���Է�ĩ��Ч
    raw_stock_sent_amount = models.FloatField(null=True, blank=True)
    # ׷�ӷ���
    send_addition = models.ManyToManyField(RawStockSendAddition, related_name='RawStockSendAddition_Send', blank=True)
    # ��������
    retrieve_time = models.DateField(null=True, blank=True)
    # δ��ԭ�������� ���Է�ĩ��Ч
    raw_stock_unused_amount = models.FloatField(null=True, blank=True)
    # # һ�����շ�ʵ��
    # raw_stock_primaryretrieve = models.ForeignKey(RawStock, related_name='RawStock_RetrieveAsPrimaryFrom',
    #                                               on_delete=models.CASCADE, null=True, blank=True)
    # ����һ����ĩ���� ���Է�ĩ��Ч
    raw_stock_primaryretrieve_amount = models.FloatField(null=True, blank=True)
    # # �������շ�ʵ��
    # raw_stock_secondaryretrieve = models.ForeignKey(RawStock, related_name='RawStock_RetrieveAssecondaryFrom',
    #                                                 on_delete=models.CASCADE, null=True, blank=True)
    # ���ն�����ĩ���� ���Է�ĩ��Ч
    raw_stock_secondaryretrieve_amount = models.FloatField(null=True, blank=True)
    # �Ƿ���Ч
    available = models.BooleanField(default=True)

    def __str__(self):
        return '�״η�������:\t%s\n������:\t%s\n�����豸:\t%s\n�����ļ�\t%s\n����:\t\t%s\n'%(self.send_time,
                                                ','.join(map(lambda product:product.product_code,self.LAM_mission.LAM_product.all())),
                                                self.LAM_mission.work_section,
                                                self.LAM_mission.LAM_techinst_serial.technique_instruction.instruction_code,
                                                self.LAM_mission.LAM_techinst_serial.serial_number
                                                     )


    
    
    
# # ��ĩ�������
# class RawStock_Powder_GroupPart(models.Model):
#     # ԭ����ʵ��
#     raw_stock = models.ForeignKey(RawStock, related_name='RawStock_GroupPart' , on_delete=models.CASCADE)
#     # ����
#     amount = models.FloatField()
#
# # ��ĩ����
# class RawStock_Powder_GroupBatch(models.Model):
#     # ԭ����
#     parents_RawStock_GroupPart = models.ManyToManyField(RawStock_Powder_GroupPart, related_name='RawStockGroupPart_AsParentsBatch')
#     # ������
#     New_RawStock_GroupPart = models.ForeignKey(RawStock_Powder_GroupPart, related_name='RawStockGroupPart_AsNewBatch', on_delete=models.CASCADE)
#     # ��������
#     grouped_time = models.DateField()
#     pass



    

# �������
class MechanicalTest_Tensile(models.Model):
    # # ��������
    # test_mission = models.ForeignKey(PhysicochemicalTest_Mission, on_delete=models.CASCADE)
    # �������
    sample_number = models.CharField(max_length=10, null=True, blank=True)
    # ȡ����λ
    sampling_position = models.ForeignKey(SamplingPosition, on_delete=models.CASCADE)
    # ȡ������
    sampling_direction = models.ForeignKey(SamplingDirection, on_delete=models.CASCADE)
    # �����¶�
    test_temperature = models.FloatField(default=25, null=True, blank=True)
    # ����ǿ�� MPa
    tensile_strength = models.FloatField(null=True, blank=True)
    # ����ǿ�� MPa
    yield_strength = models.FloatField(null=True, blank=True)
    # �Ϻ������� %
    elongation = models.FloatField(null=True, blank=True)
    # ���������� %
    areareduction = models.FloatField(null=True, blank=True)
    # ����ģ�� GPa
    modulus = models.FloatField(null=True, blank=True)
    # �Ƿ���Ч
    available = models.BooleanField(default=True)

    # class Meta:
    def __str__(self):
        return self.sample_number


# �������
class MechanicalTest_Toughness(models.Model):
    # �������
    sample_number = models.CharField(max_length=10, null=True, blank=True)
    # ȡ����λ
    sampling_position = models.ForeignKey(SamplingPosition, on_delete=models.CASCADE)
    # ȡ������
    sampling_direction = models.ForeignKey(SamplingDirection, on_delete=models.CASCADE)
    # �����¶�
    test_temperature = models.FloatField(default=25, null=True, blank=True)
    # �������
    toughness = models.FloatField(null=True, blank=True)
    # �Ƿ���Ч
    available = models.BooleanField(default=True)
    def __str__(self):
        return self.sample_number

class MechanicalTest_FractureToughness(models.Model):
    # �������
    sample_number = models.CharField(max_length=10, null=True, blank=True)
    # ȡ����λ
    sampling_position = models.ForeignKey(SamplingPosition, on_delete=models.CASCADE)
    # ȡ������
    sampling_direction = models.ForeignKey(SamplingDirection, on_delete=models.CASCADE)
    # �����¶�
    test_temperature = models.FloatField(default=25, null=True, blank=True)
    # ��������
    fracturetoughness_KIC = models.FloatField(null=True, blank=True)
    # ��������
    fracturetoughness_KQ = models.FloatField(null=True, blank=True)
    # ������Ч���ж�
    Effectiveness = models.BooleanField(null=True, blank=True)
    # �Ƿ���Ч
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.sample_number


# ��ѧ�ɷֲ���
class ChemicalTest_Element(models.Model):
    # ELEMENT_CHOICES = (
    #     ('Ti', 'Ti-��'),
    #     ('Al', 'Al-��'),
    #     ('Sn', 'Sn-��'),
    #     ('Mo', 'Mo-��'),
    #     ('Si', 'Si-��'),
    #     ('Cr', 'Cr-��'),
    #     ('Zr', 'Zr-�'),
    #     ('V', 'V-��'),
    #     ('Fe', 'Fe-��'),
    #     ('Mn', 'Mn-��'),
    #     ('C', 'C-̼'),
    #     ('H', 'H-��'),
    #     ('O', 'O-��'),
    #     ('N', 'N-��'),
    # )
    # ѡ��Ԫ��
    element = models.ForeignKey(ChemicalElement, on_delete=models.DO_NOTHING)
    # �ⶨ����
    value = models.FloatField()


# ��ѧ�ɷֲ���
class ChemicalTest(models.Model):
    # �������
    sample_number = models.CharField(max_length=10, null=True, blank=True)
    # ȡ����λ
    sampling_position = models.ForeignKey(SamplingPosition, on_delete=models.PROTECT)
    # Ԫ�غ���
    elements = models.ManyToManyField(ChemicalTest_Element)
    def __str__(self):
        return self.sample_number



# �������������
class PhysicochemicalTest_Mission(models.Model):
    # ��Ʒʵ�� Ӧ��Ϊ��ѡ
    # LAM_product = models.ForeignKey(LAMProduct, on_delete=models.CASCADE, null=True)
    LAM_product = models.ManyToManyField(LAMProduct, blank=True)
    # ԭ����ʵ��
    RawStock = models.ForeignKey(RawStock, on_delete=models.CASCADE, null=True)
    # ������ι���ʵ��
    LAM_techinst_serial = models.ForeignKey(LAM_TechInst_Serial, on_delete=models.CASCADE)
    # ί������
    commission_date = models.DateField(null=True)
    # �ȴ���״̬
    heat_treatment_state = models.ForeignKey(HeatTreatmentState, on_delete=models.DO_NOTHING)
    # �������
    mechanicaltest_tensile = models.ManyToManyField(MechanicalTest_Tensile, blank=True)
    # �������
    mechanicaltest_toughness = models.ManyToManyField(MechanicalTest_Toughness, blank=True)
    # �����ͶȲ���
    mechanicaltest_fracturetoughness = models.ManyToManyField(MechanicalTest_FractureToughness, blank=True)
    # ��ѧ�ɷֲ���
    chemicaltest = models.ManyToManyField(ChemicalTest, blank=True)
        # models.ForeignKey(ChemicalTest, on_delete=models.DO_NOTHING, null=True, blank=True)

    # �Ƿ���Ч
    available = models.BooleanField(default=True)


# ���ϸ�Ʒ����
class QualityReviewSheet(models.Model):
    # ��Ʒʵ��
    LAM_product = models.ManyToManyField(LAMProduct, related_name='Product_QualityReviewSheet')
    # ����ʵ��
    LAM_techinst_serial = models.ForeignKey(LAM_TechInst_Serial, on_delete=models.CASCADE)
    # ��������
    detection_date = models.DateField(null=True)
    # �����ļ�  ������
    file = models.FileField(upload_to='.' + MEDIA_ReviewSheet_URL, null=True)

# �������
class LAMProductSubarea(models.Model):
    product_category = models.ForeignKey(LAMProductCategory, on_delete=models.CASCADE, verbose_name='��Ʒ���')
    subarea_name = models.CharField(max_length = 20, verbose_name='��������')# �Ƿ���Ч
    available = models.BooleanField(default=True, verbose_name='�Ƿ���Ч')
    def __str__(self):
        return '%s-%s'%(self.product_category.product_symbol, self.subarea_name)

class DefectPicture(models.Model):
    picture = models.ImageField(verbose_name='ȱ����Ƭ', upload_to='.'+MEDIA_DefectPicture_URL)

# һ������ȱ��
class UTDefectInformation(models.Model):
    # ȱ�ݱ��
    defect_number = models.CharField(max_length = 10, blank=True, null=True, verbose_name = u'���')
    # ȱ������
    defect_type = models.CharField(max_length = 10,
                                choices = (('Single','������������ָʾ'),('Multiple','�����������ָʾ'),('Strip','������������ָʾ'),('Noise','����')),
                                verbose_name = u'����ȱ�����')
    # ����
    equivalent_hole_diameter = models.FloatField(blank=True, null=True, verbose_name = u'����ƽ�׿�ֱ��(mm)')
    # ���䵱��  ������ڵĵ�λ
    radiation_equivalent = models.IntegerField(blank=True, null=True, verbose_name = u'���䵱��(db)')
    # ���ڷ���
    product_subarea = models.ForeignKey(LAMProductSubarea, on_delete=models.CASCADE, blank=True, null=True,verbose_name = u'ȱ�����ڷ���')
    # �뾫�ӹ�״̬ͳһ����λ�� - x
    X_coordinate = models.FloatField(blank=True, null=True, verbose_name = u'�ӹ���ģ������X')
    # �뾫�ӹ�״̬ͳһ����λ�� - y
    Y_coordinate = models.FloatField(blank=True, null=True, verbose_name = u'�ӹ���ģ������Y')
    # �뾫�ӹ�״̬ͳһ����λ�� - z
    Z_coordinate = models.FloatField(blank=True, null=True, verbose_name = u'�ӹ���ģ������Z')
    # ���ȱ����Ƭ
    photos = models.ManyToManyField(DefectPicture, related_name='DefectPicture_UTDefectInfo')
    def __str__(self):
        return '%s-%s (%.1f%+ddb)'%(self.defect_number,
                                self.get_defect_type_display(),
                                self.equivalent_hole_diameter,
                                self.radiation_equivalent)
    

# һ��X����ȱ��
class RTDefectInformation(models.Model):
    # ȱ�ݱ��
    defect_number =  models.CharField(max_length = 10, blank=True, null=True, verbose_name = u'���')
    # ȱ������
    defect_type = models.CharField(max_length=10,
                                   choices=(('Single', '����ȱ��'), ('Group', '����ȱ��')),
                                   verbose_name=u'X����ȱ�����')
    # ȱ�ݴ�С
    size = models.FloatField(verbose_name=u'ȱ�ݴ�С(mm)')
    # ���ڷ���
    product_subarea = models.ForeignKey(LAMProductSubarea, on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name=u'ȱ�����ڷ���')
    # �ӹ�״̬ͳһ����λ�� - x
    X_coordinate = models.FloatField(blank=True, null=True, verbose_name=u'�ӹ���ģ������X')
    # �ӹ�״̬ͳһ����λ�� - y
    Y_coordinate = models.FloatField(blank=True, null=True, verbose_name=u'�ӹ���ģ������Y')
    # �ӹ�״̬ͳһ����λ�� - z
    Z_coordinate = models.FloatField(blank=True, null=True, verbose_name=u'�ӹ���ģ������Z')
    # ���ȱ����Ƭ
    photos = models.ManyToManyField(DefectPicture, related_name='DefectPicture_RTDefectInfo')
    def __str__(self):
        return '%s-%s'%(self.defect_number, self.get_defect_type_display())

# һ��ӫ��ȱ��
class PTDefectInformation(models.Model):
    # ȱ�ݱ��
    defect_number =  models.CharField(max_length = 10, blank=True, null=True, verbose_name = u'���')
    # ȱ������
    defect_type = models.CharField(max_length=10,
                                   choices=(('Single', '����ȱ��'), ('Group', '����ȱ��')),
                                   verbose_name=u'ӫ��ȱ�����')
    # ���ڷ���
    product_subarea = models.ForeignKey(LAMProductSubarea, on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name=u'ȱ�����ڷ���')
    # �ӹ�״̬ͳһ����λ�� - x
    X_coordinate = models.FloatField(blank=True, null=True, verbose_name=u'�ӹ���ģ������X')
    # �ӹ�״̬ͳһ����λ�� - y
    Y_coordinate = models.FloatField(blank=True, null=True, verbose_name=u'�ӹ���ģ������Y')
    # �ӹ�״̬ͳһ����λ�� - z
    Z_coordinate = models.FloatField(blank=True, null=True, verbose_name=u'�ӹ���ģ������Z')
    # ���ȱ����Ƭ
    photos = models.ManyToManyField(DefectPicture, related_name='DefectPicture_PTDefectInfo')
    def __str__(self):
        return '%s-%s'%(self.defect_number, self.get_defect_type_display())

# һ���ŷ�ȱ��
class MTDefectInformation(models.Model):
    # ȱ�ݱ��
    defect_number =  models.CharField(max_length = 10, blank=True, null=True, verbose_name = u'���')
    # ȱ������
    defect_type = models.CharField(max_length=10,
                                   choices=(('Single', '����ȱ��'), ('Group', '����ȱ��')),
                                   verbose_name=u'�ŷ�ȱ�����')
    # ���ڷ���
    product_subarea = models.ForeignKey(LAMProductSubarea, on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name=u'ȱ�����ڷ���')
    # �ӹ�״̬ͳһ����λ�� - x
    X_coordinate = models.FloatField(blank=True, null=True, verbose_name=u'�ӹ���ģ������X')
    # �ӹ�״̬ͳһ����λ�� - y
    Y_coordinate = models.FloatField(blank=True, null=True, verbose_name=u'�ӹ���ģ������Y')
    # �ӹ�״̬ͳһ����λ�� - z
    Z_coordinate = models.FloatField(blank=True, null=True, verbose_name=u'�ӹ���ģ������Z')
    # ���ȱ����Ƭ
    photos = models.ManyToManyField(DefectPicture, related_name='DefectPicture_MTDefectInfo')
    def __str__(self):
        return '%s-%s'%(self.defect_number, self.get_defect_type_display())
# ������
class NonDestructiveTest_Mission(models.Model):
    # ��Ʒʵ��
    LAM_product = models.ForeignKey(LAMProduct, on_delete=models.CASCADE, null=True, verbose_name = u'��Ʒ���')
    # ԭ����ʵ��
    RawStock = models.ForeignKey(RawStock, on_delete=models.CASCADE, null=True, verbose_name = u'ԭ��������')
    # ������ι���ʵ��
    LAM_techinst_serial = models.ForeignKey(LAM_TechInst_Serial, on_delete=models.CASCADE, verbose_name = u'��⹤��')
    # ��Ʒ�ӹ�״̬
    machining_state = models.ForeignKey(MachiningState, on_delete=models.CASCADE, verbose_name = u'�ӹ�״̬')
    # ��Ʒ�ȴ���״̬
    heat_treatment_state = models.ForeignKey(HeatTreatmentState, on_delete=models.CASCADE, verbose_name = u'�ȴ���״̬')
    # �����������´�ʱ��
    arrangement_date = models.DateField(null=True, blank=True, verbose_name = u'����ʼʱ��')
    # �����������
    completion_date = models.DateField(null=True, blank=True,  verbose_name = u'�������ʱ��')
    # �Ƿ���Ч
    available = models.BooleanField(default=True,  verbose_name = u'�Ƿ���Ч')
    # # ���������  ���������ߡ�ӫ�⡢�ŷ�
    # NDT_type = models.CharField(max_length = 8,
    #                             choices = (('UT','���������'),('RT','X���߼��'),('PT','��͸���'),('MT','�ŷۼ��')),
    #                             verbose_name = u'���������')
    
    # �������ȱ����Ϣ
    UT_defect = models.ManyToManyField(UTDefectInformation, related_name='UTDefect_NDTMission', verbose_name = u'����ȱ��')

    # X���߼��ȱ����Ϣ
    RT_defect = models.ManyToManyField(RTDefectInformation, related_name='RTDefect_NDTMission', verbose_name = u'X����ȱ��')

    # ӫ����͸ȱ����Ϣ
    PT_defect = models.ManyToManyField(PTDefectInformation, related_name='PTDefect_NDTMission', verbose_name = u'ӫ��ȱ��')

    # �ŷۼ��ȱ����Ϣ
    MT_defect = models.ManyToManyField(MTDefectInformation, related_name='MTDefect_NDTMission', verbose_name = u'�ŷ�ȱ��')
    

    # ����ȱ����Ϣ ��Զ� ȱ�ݱ�ţ�������������λ�ã���С��ȱ�����ͣ���Ƭ
    # ����ȱ����Ϣ ��Զ� ȱ�ݱ�ţ�������������λ�ã���С��ȱ�����ͣ���Ƭ
    # ӫ��ȱ����Ϣ ��Զ� ȱ�ݱ�ţ�������������λ�ã���С��ȱ�����ͣ���Ƭ
    # ���޴���
    rewelding_number = models.PositiveIntegerField(null=True, blank=True, verbose_name = u'���޴���')
    # ���� ���
    quality_reviewsheet = models.ForeignKey(QualityReviewSheet, on_delete=models.CASCADE,null=True, blank=True, verbose_name = u'���ϸ�Ʒ����')
    



class Oxygendata(models.Model):
    work_section = models.ForeignKey(Worksection, on_delete=models.DO_NOTHING)
    process_mission = models.ForeignKey(LAMProcessMission, on_delete=models.DO_NOTHING, null=True)
    acquisition_time = models.DateTimeField()
    # ��ȡ��ʱ���
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
    # ��ȡ��ʱ���
    acquisition_timestamp = models.PositiveIntegerField( null=True)
    laser_power = models.IntegerField()
    laser_lightpath_temperature = models.FloatField()
    laser_laser_temperature = models.FloatField()

    def __str__(self):
        return str(self.laser_power)
    class Meta:
        index_together = ['work_section', 'process_mission', 'acquisition_timestamp']



# ����ϵͳ�ӹ����̳�������/�ж�״̬��auto�����µĸ������
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


# ����ϵͳ�ӹ�����ʵʱ״̬
class CNCProcessStatus(models.Model):
    # ����
    work_section = models.ForeignKey(Worksection, on_delete=models.DO_NOTHING)
    # �����
    process_mission = models.ForeignKey(LAMProcessMission, on_delete=models.DO_NOTHING, null=True)
    # ��ȡ��ʱ��
    acquisition_time = models.DateTimeField(null=True)
    # ��ȡ��ʱ���
    acquisition_timestamp = models.PositiveIntegerField(null=True)
    # ��ͼ
    screen_image = models.ImageField(upload_to='img/%Y/%m/%d', null=True, blank=True)
    # ��ͼƬ�Ƿ���������
    if_checked = models.BooleanField(default=False)
    # �������
    check_datetime = models.DateTimeField(null=True, blank=True)
    # �Ƿ�Ϊ�Զ�����
    if_auto_exec_intr = models.BooleanField(null=True, blank=True)
    # �Ƿ��������г���
    if_exec_intr = models.BooleanField(null=True, blank=True)
    # �Ƿ������г�������ж�
    if_interrupt_intr = models.BooleanField(null=True, blank=True)
    # ���г�����жϵĲ���
    autodata = models.ForeignKey(CNCProcessAutoData, on_delete=models.DO_NOTHING,null=True, blank=True)
    # ����ϵͳ��Ļ�����������
    status_category = models.ForeignKey(CNCStatusCategory, on_delete=models.DO_NOTHING, null=True, blank=True)
    # ѡ�еĳ����ļ���
    program_name = models.CharField(max_length=20, null=True)
    # ����������г�������Z�߶�����
    Z_value = models.FloatField(null=True)
    class Meta:
        index_together = ['work_section', 'process_mission', 'acquisition_timestamp']



# # ��ʱ-����������
class TemporaryParameter_ID(models.Model):
    # id��
    '''
    1: CNCProcessStatus_SendImage_MAX_ID    ���ַ�img��id  ��һ�ַ�idΪ����+1
        SELECT max(id) FROM lamdataserver.lamprocessdata_cncprocessautodata;
    2: CNCProcessStatus_NotRecoge_Min_ID    ��С��ʶ��img��id �´β�ѯ�Դ�������
        SELECT min(id) FROM lamdataserver.lamprocessdata_cncprocessstatus WHERE if_checked=0;
    3: Process_Oxygendata_Date_Worksection_indexing�����������id��
    4: Process_Laserdata_Date_Worksection_indexing�����������id��
    5: Process_CNCStatusdata_Date_Worksection_indexing�����������id��
    6: Process_Realtime_FineData_By_WorkSectionID �ĸ���ʱ���(��)
    '''
    item_id = models.IntegerField(null=True)
    note = models.CharField(max_length=100, null=True)

# ���ݳ��ι�����ֹʱ�仮�ּ��⡢��������CNC�Ȳ�����id��Ϣ
class Process_Mission_timecut(models.Model):
    # �����
    process_mission = models.OneToOneField(LAMProcessMission, related_name='Mission_Timecut', on_delete=models.DO_NOTHING, null=True)
    # ��ʼʱ��
    process_start_time = models.DateTimeField(null=True, blank=True)
    # ����ʱ��
    process_finish_time = models.DateTimeField(null=True, blank=True)
    # ������ϸ��id
    finedata_start_recordid = models.PositiveIntegerField(null=True, blank=True)
    finedata_finish_recordid = models.PositiveIntegerField(null=True, blank=True)
    # ������ʼԪ��
    # laserdata_start_item = models.ForeignKey(Laserdata, related_name='laserdata_start_item', on_delete=models.DO_NOTHING, null=True, blank=True)
    laserdata_start_recordid = models.PositiveIntegerField(null=True, blank=True)
    # ������ֹԪ��
    # laserdata_finish_item = models.ForeignKey(Laserdata, related_name='laserdata_finish_item', on_delete=models.DO_NOTHING, null=True, blank=True)
    laserdata_finish_recordid = models.PositiveIntegerField(null=True, blank=True)
    # ��������ʼԪ��
    # oxygendata_start_item = models.ForeignKey(Oxygendata, related_name='oxygendata_start_item', on_delete=models.DO_NOTHING, null=True, blank=True)
    oxygendata_start_recordid = models.PositiveIntegerField(null=True, blank=True)
    # ��������ֹԪ��
    # oxygendata_finish_item = models.ForeignKey(Oxygendata, related_name='oxygendata_finish_item', on_delete=models.DO_NOTHING, null=True, blank=True)
    oxygendata_finish_recordid = models.PositiveIntegerField(null=True, blank=True)
    # ����״̬��ʼԪ��
    # cncstatusdata_start_item = models.ForeignKey(CNCProcessStatus, related_name='cncstatusdata_start_item', on_delete=models.DO_NOTHING, null=True, blank=True)
    cncstatusdata_start_recordid = models.PositiveIntegerField(null=True, blank=True)
    # ����״̬��ֹԪ��
    # cncstatusdata_finish_item = models.ForeignKey(CNCProcessStatus, related_name='cncstatusdata_finish_item', on_delete=models.DO_NOTHING, null=True, blank=True)
    cncstatusdata_finish_recordid = models.PositiveIntegerField(null=True, blank=True)

# ��¼�������ε�ǰ�����е�����
class Worksection_Current_LAMProcessMission(models.Model):
    # ����
    work_section = models.OneToOneField(Worksection, on_delete=models.DO_NOTHING, null=True)
    # ѡ�е�����
    process_mission = models.ForeignKey(LAMProcessMission, on_delete=models.DO_NOTHING, null=True, blank=True)
    # �Ƿ���ִ��������
    if_onwork = models.BooleanField(default=False)


# ������������ݣ�ÿ�ա�ÿ���θ�ռ1�����ݣ����ݰ������������ݵ���ֹobject
class Process_Oxygendata_Date_Worksection_indexing(models.Model):
    # ����
    work_section = models.ForeignKey(Worksection, on_delete=models.DO_NOTHING)
    # ����
    index_date = models.DateField()
    # ���ڶ�Ӧ������ 8λ YYYYMMDD
    index_date_int= models.IntegerField(null=True)
    # ��������ʼԪ��
    # oxygendata_start_item = models.ForeignKey(Oxygendata, related_name='oxygendata_start_item', on_delete=models.DO_NOTHING, null=True, blank=True)
    data_start_id = models.PositiveIntegerField(null=True)
    # ��������ֹԪ��
    # oxygendata_finish_item = models.ForeignKey(Oxygendata, related_name='oxygendata_finish_item', on_delete=models.DO_NOTHING, null=True, blank=True)
    data_finish_id = models.PositiveIntegerField(null=True)
    # ��','����ĵ����ÿ���ӵ������б�  str
    data_string = models.TextField(null=True)


# ��Լ������ݣ�ÿ�ա�ÿ���θ�ռ1�����ݣ����ݰ����������ݵ���ֹobject
class Process_Laserdata_Date_Worksection_indexing(models.Model):
    # ����
    work_section = models.ForeignKey(Worksection, on_delete=models.DO_NOTHING)
    # ����
    index_date = models.DateField()
    # ���ڶ�Ӧ������ 8λ YYYYMMDD
    index_date_int= models.IntegerField(null=True)
    # ������ʼԪ��
    # laserdata_start_item = models.ForeignKey(Laserdata, related_name='laserdata_start_item', on_delete=models.DO_NOTHING, null=True, blank=True)
    data_start_id = models.PositiveIntegerField(null=True)
    # ������ֹԪ��
    # laserdata_finish_item = models.ForeignKey(Laserdata, related_name='laserdata_finish_item', on_delete=models.DO_NOTHING, null=True, blank=True)
    data_finish_id = models.PositiveIntegerField(null=True)
    # ��','����ĵ����ÿ���ӵ������б�  str
    data_string = models.TextField(null=True)


# ������ػ������ݣ�ÿ�ա�ÿ���θ�ռ1�����ݣ����ݰ������ػ���״̬���ݵ���ֹobject
class Process_CNCStatusdata_Date_Worksection_indexing(models.Model):
    # ����
    work_section = models.ForeignKey(Worksection, on_delete=models.DO_NOTHING)
    # ����
    index_date = models.DateField()
    # ���ڶ�Ӧ������ 8λ YYYYMMDD
    index_date_int= models.IntegerField(null=True)
    # ����״̬��ʼԪ��
    # cncstatusdata_start_item = models.ForeignKey(CNCProcessStatus, related_name='cncstatusdata_start_item', on_delete=models.DO_NOTHING, null=True, blank=True)
    data_start_id = models.PositiveIntegerField(null=True)
    # ����״̬��ֹԪ��
    # cncstatusdata_finish_item = models.ForeignKey(CNCProcessStatus, related_name='cncstatusdata_finish_item', on_delete=models.DO_NOTHING, null=True, blank=True)
    data_finish_id = models.PositiveIntegerField(null=True)
    # ��','����ĵ����ÿ���ӵ������б�  str
    data_string = models.TextField(null=True)


# ������񣬰����ִ��������ݲ������Լ�������̼�¼�п���ͣ�����ݼ����ۼ�ֵ��������뱾����
class Process_Accumulatedata_Mission(models.Model):
    # ������Ϣ
    process_mission = models.ForeignKey(LAMProcessMission, related_name='Mission_Accumulatedata', on_delete=models.DO_NOTHING, null=True, blank=True)
    # �洢���� ����P, K, ��
    data_file = models.FileField(upload_to='.'+ANALYSE_ACCUMULATEDATA_URL, null=True)
    # ����ϵ��M1
    M1 = models.FloatField(null=True, blank=True)
    # ͣ����ȴϵ��M2
    M2 = models.FloatField(null=True, blank=True)
    # ͣ����ȴ-�ۼ�ϵ��l
    l = models.FloatField(null=True, blank=True)
    # ͣ����ȴ-Ȩ�ذ�˥��tm
    tm = models.FloatField(null=True, blank=True)
    # # ����
    # index_date = models.DateField()
    # # ���ڶ�Ӧ������ 8λ YYYYMMDD
    # index_date_int = models.IntegerField(null=True)
    # # ��һ������Ϊ������ʼ��ڼ�����
    # minute_index = models.IntegerField(null=True)
    # # (list:24*60), �б�  1�����ڿ��⹦���ۼ�ֵ
    # P = models.TextField(null=True)
    # # (list:24*60), �б�  1������ͣ������
    # K = models.TextField(null=True)

# ������񣬰����ִ��������ݲ������Լ�������̼�¼�п���ͣ�����ݼ����ۼ�ֵ��������뱾����
class Process_CNCData_Mission(models.Model):
    # ������Ϣ
    process_mission = models.ForeignKey(LAMProcessMission, related_name='Mission_CNCData', on_delete=models.DO_NOTHING, null=True, blank=True)
    # �洢���� ����Z_value, layer_thickness ��
    # zip(missionid_list, productcode_list, minute_index_list, ZValue_list, _P191_list)
    zvalue_data_file = models.FileField(upload_to='.'+ANALYSE_CNCDATA_URL, null=True)
    # �洢���� ����ÿ���ӿ��������ۼ�������ÿ����ͣ��������
    accumulate_data_file = models.FileField(upload_to='.'+ANALYSE_ACCUMULATEDATA_URL, null=True)
    # # ����
    # index_date = models.DateField()
    # # ���ڶ�Ӧ������ 8λ YYYYMMDD
    # index_date_int = models.IntegerField(null=True)
    # # ��һ������Ϊ������ʼ��ڼ�����
    # minute_index = models.IntegerField(null=True)
    # # (list:24*60), �б�  1������Z��Сֵ
    # Z_value = models.TextField(null=True)
    # # (list:24*60), �б�  1�����ڲ���
    # layer_thickness = models.TextField(null=True)

class Process_CNCData_Layer_Mission(models.Model):
    # ������Ϣ
    process_mission = models.ForeignKey(LAMProcessMission, related_name='Mission_LayerCNCData', on_delete=models.DO_NOTHING, null=True, blank=True)
    # �洢���� ����X_value, Y_value, Z_value, ScanSpd ��
    data_file = models.FileField(upload_to='.'+ANALYSE_CNCDATA_URL, null=True)

class Process_Realtime_FineData_By_WorkSectionID(models.Model):
    # ��ȡ��ʱ���
    acquisition_timestamp = models.PositiveIntegerField(unique=True)
    # ��ȡ��ʱ��str
    acquisition_datetime = models.DateTimeField(null=True, blank=True)
    # ������
    oxygen_value = models.FloatField(default=-1)
    # ���⹦��
    laser_power = models.IntegerField(null=True)
    # ������Ϣ
    X_value = models.FloatField(null=True)
    Y_value = models.FloatField(null=True)
    Z_value = models.FloatField(null=True)
    ScanningRate_value = models.FloatField(null=True)
    FeedRate_value = models.IntegerField(null=True)
    program_name = models.CharField(max_length=20, null=True)
    # ������Ϣ
    process_mission = models.ForeignKey(LAMProcessMission, on_delete=models.DO_NOTHING, null=True, blank=True)
    # �Ƿ��������г���
    if_exec_intr = models.BooleanField(null=True, blank=True)
    # �Ƿ������г�������ж�
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

class LAMProcess_Worksection_Operate(models.Model):
    # ������Ϣ
    process_mission = models.ForeignKey(LAMProcessMission, on_delete=models.DO_NOTHING, null=True, blank=True)
    # ��ȡ��ʱ���
    acquisition_timestamp = models.PositiveIntegerField(unique=True)
    # ����
    operate_information = models.CharField(max_length=50, null=True)
    # ������
    # https://www.cnblogs.com/wcwnina/p/9246228.html
    operator = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)


# ������ι��������в����Ϲ��ղ������ļ�¼
class Process_Inspect_FineData_DiscordantRecords(models.Model):
    # ������Ϣ
    process_mission = models.ForeignKey(LAMProcessMission, on_delete=models.DO_NOTHING, null=True, blank=True)
    # ����ʱ��
    inspect_timestamp = models.PositiveIntegerField()
    # �����Ͻ׶ο�ʼʱ���
    start_timestamp = models.PositiveIntegerField()
    # �����Ͻ׶ν���ʱ���
    finish_timestamp = models.PositiveIntegerField()
    # ��������Ŀ
    parameter_conditionalcell = models.ForeignKey(LAMProcessParameterConditionalCell, on_delete=models.DO_NOTHING, null=True, blank=True)
    # # ʵ��ֵ
    # parameter_realvalue = models.CharField(max_length=50, null=True)



# @receiver(pre_delete, sender=CNCProcessStatus)
# def file_delete(sender, instance, **kwargs):
#     # Pass false so FileField doesn't save the model.
#     # print('�����ļ�ɾ��������ɾ����',instance.alter_file)
#     instance.file.delete(False)





# print('end models.py')