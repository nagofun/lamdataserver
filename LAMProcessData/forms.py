# coding=utf-8
from LAMProcessData.models import *
from django import forms
from django.forms import ModelForm, widgets
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
import datetime
# print('start forms.py')

# 厂房
class WorkshopForm(ModelForm):
	title = '厂房信息维护'
	modelname = 'Workshop'

	class Meta:
		model = Workshop
		fields = "__all__"
		labels = {
			'name': _('厂房名称'),
			'code': _('厂房代号'),
			'available': _('是否激活'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['available'].disabled = True
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


# 生产现场计算机
class ComputerForm(ModelForm):
	title = '现场计算机信息维护'
	modelname = 'Computer'

	class Meta:
		model = Computer
		fields = "__all__"
		# widgets = {
		#     'name': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入计算机名称', 'max_length':30}),
		#     'model_number': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入计算机型号', 'max_length':30}),
		#     'mac_address': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入计算机物理地址', 'max_length':17}),
		# }
		labels = {
			'name': _('计算机名称'),
			'model_number': _('计算机型号'),
			'mac_address': _('计算机物理地址'),
			'device_Number': _('设备编号'),
			'available': _('是否激活'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['available'].disabled = True
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


class WorksectionForm(ModelForm):
	title = '工段信息维护'
	modelname = 'Worksection'

	class Meta:
		model = Worksection
		fields = "__all__"
		# widgets = {
		#     'name': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入工段名称'}),
		#     'code': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入工段代号'}),
		#     'workshop': widgets.Select(attrs={'class': "form-control"}),
		#     'desktop_computer': widgets.Select(attrs={'class': "form-control"}),
		#     'cnc_computer': widgets.Select(attrs={'class': "form-control"}),
		# }
		labels = {
			'name': _('工段名称'),
			'code': _('工段代号'),
			'workshop': _('所属厂房'),
			'desktop_computer': _('桌面计算机'),
			'cnc_computer': _('数控计算机'),
			'available': _('是否激活'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.fields['available'].
		self.fields['workshop'].queryset = Workshop.objects.filter(available=True)
		self.fields['desktop_computer'].queryset = Computer.objects.filter(available=True)
		self.fields['cnc_computer'].queryset = Computer.objects.filter(available=True)
		self.fields['available'].disabled = True
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


# 材料
class LAMMaterialForm(ModelForm):
	title = '材料信息维护'
	modelname = 'LAMMaterial'

	class Meta:
		model = LAMMaterial
		fields = "__all__"
		# fields = ['material_code', 'material_name', 'nominal_composition',
		#                      'available']
		# widgets = {
		#     'material_code': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入材料牌号'}),
		#     'material_name': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入材料名称'}),
		#
		# }
		labels = {
			'material_name': _('材料牌号'),
			'material_code': _('材料名称'),
			'nominal_composition': _('名义成分'),
			'chemicalelements': _('化学元素测试项'),
			'available': _('是否激活'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['available'].disabled = True
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


# 原材料类别
class RawStockCategoryForm(ModelForm):
	title = '原材料类别信息维护'
	modelname = 'RawStockCategory'

	class Meta:
		model = RawStockCategory
		fields = "__all__"
		labels = {
			'Category_name': _('原材料类别'),
			'available': _('是否激活'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['available'].disabled = True
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


# 数控系统屏幕界面类别
class CNCStatusCategoryForm(ModelForm):
	title = '数控系统屏幕界面类别信息维护'
	modelname = 'CNCStatusCategory'

	class Meta:
		model = CNCStatusCategory
		fields = "__all__"
		labels = {
			'status_name': _('界面名称'),
			'available': _('是否激活'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['available'].disabled = True
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})
# print(this.title)


# 原材料台账
class RawStockForm(ModelForm):
	title = '原材料记录'
	modelname = 'RawStock'

	class Meta:
		model = RawStock
		fields = "__all__"
		widgets = {
			'batch_number': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入原材料批号'}),
			'material': widgets.Select(attrs={'class': "form-control"}),
			'rawstock_category': widgets.Select(attrs={'class': "form-control"}),

		}
		labels = {
			'batch_number': _('原材料批号'),
			'material': _('材料牌号'),
			'rawstock_category': _('原材料类别'),
			'rawstock_supplier': _('供应商'),
			'available': _('是否激活'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['available'].disabled = True
		self.fields['material'].queryset = LAMMaterial.objects.filter(available=True)
		self.fields['rawstock_category'].queryset = RawStockCategory.objects.filter(available=True)
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


# 原材料台账_编辑
class RawStockForm_Edit(ModelForm):
	title = '原材料记录'
	modelname = 'RawStock'

	class Meta:
		model = RawStock
		fields = "__all__"
		widgets = {
			'batch_number': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入原材料批号'}),
			'material': widgets.Select(attrs={'class': "form-control"}),
			'rawstock_category': widgets.Select(attrs={'class': "form-control"}),

		}
		labels = {
			'batch_number': _('原材料批号'),
			'material': _('材料牌号'),
			'rawstock_category': _('原材料类别'),
			'rawstock_supplier': _('供应商'),
			'available': _('是否激活'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['available'].disabled = True
		self.fields['batch_number'].disabled = True
		self.fields['material'].disabled = True
		self.fields['rawstock_category'].disabled = True
		self.fields['material'].queryset = LAMMaterial.objects.filter(available=True)
		self.fields['rawstock_category'].queryset = RawStockCategory.objects.filter(available=True)
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


# 原材料发放台账
class RawStockSendForm(ModelForm):
	title = '原材料发放记录'
	modelname = 'RawStockSendRetrieve'

	class Meta:
		model = RawStockSendRetrieve
		fields = "__all__"
		widgets = {
			'send_time': widgets.TextInput(
				attrs={'type': 'date', 'value': str(datetime.date.today()), 'placeholder': '请选择发料日期'}),
			'retrieve_time': widgets.TextInput(attrs={'type': 'date', 'placeholder': '请选择收料日期'}),

		}
		labels = {
			'send_time': _('发料日期'),
			'LAM_mission': _('生产任务实例'),
			'raw_stock': _('原材料实例'),
			'raw_stock_sent_amount': _('发放粉末数量'),
			'retrieve_time': _('回收日期'),
			'raw_stock_unused_amount': _('未用粉末数量'),
			'raw_stock_primaryretrieve_amount': _('一级回收粉数量'),
			'raw_stock_secondaryretrieve_amount': _('二级回收粉数量'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['LAM_mission'].queryset = LAMProcessMission.objects.filter(available=True)
		self.fields['raw_stock'].queryset = RawStock.objects.filter(available=True)
		self.fields['retrieve_time'].disabled = True
		self.fields['raw_stock_unused_amount'].disabled = True
		self.fields['raw_stock_primaryretrieve_amount'].disabled = True
		self.fields['raw_stock_secondaryretrieve_amount'].disabled = True
		self.fields['available'].disabled = True

		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


# 原材料发放台账
class RawStockRetrieveForm(ModelForm):
	title = '原材料回收记录'
	modelname = 'RawStockSendRetrieve'

	class Meta:
		model = RawStockSendRetrieve
		fields = "__all__"
		# fields =  ['send_time','LAM_mission','raw_stock',
		#            'raw_stock_sent_amount','retrieve_time',
		#            'raw_stock_unused_amount','raw_stock_primaryretrieve_amount','raw_stock_secondaryretrieve_amount']
		widgets = {
			'retrieve_time': widgets.TextInput(
				attrs={'type': 'date', 'value': str(datetime.date.today()), 'placeholder': '请选择收料日期'}),

		}
		labels = {
			'send_time': _('发料日期'),
			'LAM_mission': _('生产任务实例'),
			'raw_stock': _('原材料实例'),
			'raw_stock_sent_amount': _('发放粉末数量'),
			'retrieve_time': _('回收日期'),
			'raw_stock_unused_amount': _('未用粉末数量'),
			'raw_stock_primaryretrieve_amount': _('一级回收粉数量'),
			'raw_stock_secondaryretrieve_amount': _('二级回收粉数量'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['LAM_mission'].queryset = LAMProcessMission.objects.filter(available=True)
		self.fields['raw_stock'].queryset = RawStock.objects.filter(available=True)
		# print(self.fields)
		self.fields['send_time'].disabled = True
		self.fields['LAM_mission'].disabled = True
		self.fields['raw_stock'].disabled = True
		self.fields['raw_stock_sent_amount'].disabled = True

		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


# 产品类别
class LAMProductCategoryForm(ModelForm):
	title = '产品类别'
	modelname = 'LAMProductCategory'

	class Meta:
		model = LAMProductCategory
		fields = "__all__"
		labels = {
			'drawing_code': _('产品图号'),
			'product_name': _('产品名称'),
			'product_symbol': _('产品代号'),
			'material': _('材料'),
			'available': _('是否激活'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['available'].disabled = True
		self.fields['material'].queryset = LAMMaterial.objects.filter(available=True)
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


# 基础工序类别
class LAMProductionWorkTypeForm(ModelForm):
	title = '基础工序类别'
	modelname = 'LAMProductionWorkType'

	class Meta:
		model = LAMProductionWorkType
		fields = "__all__"
		labels = {
			'worktype_name': _('工序名称'),
			'available': _('是否激活'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['available'].disabled = True
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


# 激光成形工艺文件
class LAMTechniqueInstructionForm(ModelForm):
	title = '激光成形工艺文件'
	modelname = 'LAMTechniqueInstruction'

	class Meta:
		model = LAMTechniqueInstruction
		fields = "__all__"
		labels = {
			'instruction_code': _('文件编号'),
			'instruction_name': _('文件名称'),
			'version_code': _('版本'),
			'version_number': _('版次'),
			'product_category': _('产品类别有效范围'),
			'product': _('产品有效范围'),
			'temporary': _('是否为临时文件'),
			'filed': _('是否已归档'),
			'available': _('是否激活'),
		}
		# widgets = {
		#     'LAMProcess_serial_number': widgets.TextInput(
		#         attrs={'class': 'form-control', 'id': 'LAMProcess_serial_number', 'onfocus' : 'CheckSeria()', 'placeholder': "工序号以,分隔"}),
		#     'LAMProcess_serial_note': widgets.TextInput(
		#         attrs={'class': 'form-control', 'id': 'LAMProcess_serial_note', 'onfocus': 'CheckSeria()', 'placeholder': "工序名称以,分隔"}),
		#
		# }
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.fields['LAMProcess_serial_number'].disabled = True
		# self.fields['LAMProcess_serial_note'].disabled = True
		# self.fields['LAMProcess_serial_note'].widget.attrs.update({'name':'LAMProcess_serial_note'})
		self.fields['available'].disabled = True
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


# 基础工序实例
class LAMTechInstSerialForm(ModelForm):
	title = '基础工序实例'
	modelname = 'LAM_TechInst_Serial'

	previewtableTitle = '工艺文件工序'
	# showPreviewTable = True
	previewtablefields = {'serial_number': _('工序号'), 'serial_worktype': _('工序名称'), 'serial_note': _('工序概述')}

	class Meta:
		model = LAM_TechInst_Serial
		fields = ['technique_instruction', 'serial_number', 'serial_worktype', 'serial_note', 'serial_content','process_parameter']
		# widgets = {
		#     'technique_instruction': widgets.TextInput(attrs={'class': 'form-control', 'list':"techinst_list"}),
		#     'serial_worktype': widgets.TextInput(attrs={'class': 'form-control', 'list': "worktype_list"}),
		#
		# }
		# fields = "__all__"
		labels = {
			'technique_instruction': _('工艺文件'),
			'serial_number': _('工序号'),
			'serial_worktype': _('工序名称'),
			'serial_note': _('工序概述'),
			'serial_content': _('工序内容'),
			'process_parameter':_('激光成形参数包'),
			# 'available': _('是否激活'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# 20190725 增加检查功能，失去焦点检查是否为正确项，否则振动
		# 辅助筛选工具
		self.techinst_datalist = LAMTechniqueInstruction.objects.filter(available=True).order_by('instruction_code',
		                                                                                         '-version_code',
		                                                                                         '-version_number')
		self.worktype_datalist = LAMProductionWorkType.objects.filter(available=True)

		self.fields['filter_techinst'] = forms.CharField(max_length=50, required=False)
		self.fields['filter_techinst'].widget.attrs.update(
			{'list': 'techinst_list', 'onchange': 'check_FilterTechinstField(this.value)'})
		self.fields['filter_techinst'].label = '辅助筛选工艺文件'

		self.fields['filter_worktype'] = forms.CharField(max_length=50, required=False)
		self.fields['filter_worktype'].widget.attrs.update(
			{'list': 'worktype_list', 'onchange': 'check_FilterWorktypeField(this.value)'})
		self.fields['filter_worktype'].label = '辅助筛选工序'

		self.fields['technique_instruction'].widget.attrs.update(
			{'onchange': 'loadTableData(this.value)'})

		self.field_order = ['id', 'filter_techinst', 'technique_instruction', 'serial_number', 'serial_worktype',
		                    'serial_note', 'serial_content', 'process_parameter', 'available']
		# self.fields['technique_instruction'] = forms.CharField(max_length=50)
		# self.fields['technique_instruction'].widget.attrs.update({'list':'techinst_list'})

		# self.fields['datalist_techinst'] = forms.CharField()
		# self.fields['datalist_techinst'].widget.attrs.update({'type': 'datalist', 'id':'list'})
		# self.fields['datalist_techinst'].queryset =LAMTechniqueInstruction.objects.filter(available=True)

		# self.fields['datalist_techinst'] = forms.ModelChoiceField(queryset=LAMTechniqueInstruction.objects.filter(available=True))
		# self.fields['datalist_techinst'].widget.attrs.update({'id':'list','type':'datalist'})

		self.fields['technique_instruction'].queryset = LAMTechniqueInstruction.objects.filter(available=True).order_by(
			'instruction_code', '-version_code', '-version_number')
		self.fields['serial_worktype'].queryset = LAMProductionWorkType.objects.filter(available=True)
		self.fields['technique_instruction'].widget.attrs.update({'type': 'text'})
		self.fields['process_parameter'].queryset = LAMProcessParameters.objects.filter(available=True).order_by('name')

		# self.fields['available'].disabled = True
		self.AuxiliarySelection = ('filter_techinst',
		                           'filter_worktype')
		self.OriginalFields = (
			'technique_instruction', 'serial_number', 'serial_worktype', 'serial_note', 'serial_content', 'process_parameter')
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})

	# 初始赋值 , technique_instruction_id = -1
	# if 'technique_instruction_id' in kwargs and kwargs['technique_instruction_id']>0:
	#     self.data['technique_instruction'] = kwargs['technique_instruction_id']

	def is_valid_custom(self):
		try:
			serial_number = int(self.data['serial_number'])
			if serial_number <= 0:
				# 工序号不能为0或负值
				self.error_messages = '工序号不能为0或负值'
				return False
			_tech_serial_list = LAM_TechInst_Serial.objects.filter(
				technique_instruction=self.data['technique_instruction'], serial_number=self.data['serial_number'],
				available=True)
			if len(_tech_serial_list) > 0:
				# 工序号已存在
				self.error_messages = '工序号已存在'
				return False
		except:
			self.error_messages = '未知错误'
			return False

		return self.is_valid()


# 基础工序实例 编辑
class LAMTechInstSerialForm_Edit(ModelForm):
	title = '工序实例'
	modelname = 'LAM_TechInst_Serial'

	# showPreviewTable = True
	class Meta:
		model = LAM_TechInst_Serial
		fields = ['technique_instruction', 'serial_number', 'serial_worktype', 'serial_note', 'serial_content', 'process_parameter']

		# fields = "__all__"
		labels = {
			'technique_instruction': _('工艺文件'),
			'serial_number': _('工序号'),
			'serial_worktype': _('工序名称'),
			'serial_note': _('工序概述'),
			'serial_content': _('工序内容'),
			'process_parameter':_('激光成形参数包'),
			# 'available': _('是否激活'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['technique_instruction'].disabled = True
		self.fields['serial_number'].disabled = True
		self.fields['serial_worktype'].disabled = True

		self.field_order = ['id', 'filter_techinst', 'technique_instruction', 'serial_number', 'serial_worktype',
		                    'serial_note', 'serial_content', 'available']
		# self.fields['technique_instruction'] = forms.CharField(max_length=50)
		# self.fields['technique_instruction'].widget.attrs.update({'list':'techinst_list'})

		# self.fields['datalist_techinst'] = forms.CharField()
		# self.fields['datalist_techinst'].widget.attrs.update({'type': 'datalist', 'id':'list'})
		# self.fields['datalist_techinst'].queryset =LAMTechniqueInstruction.objects.filter(available=True)

		# self.fields['datalist_techinst'] = forms.ModelChoiceField(queryset=LAMTechniqueInstruction.objects.filter(available=True))
		# self.fields['datalist_techinst'].widget.attrs.update({'id':'list','type':'datalist'})

		self.fields['technique_instruction'].queryset = LAMTechniqueInstruction.objects.filter(available=True).order_by(
			'instruction_code', '-version_code', '-version_number')
		self.fields['serial_worktype'].queryset = LAMProductionWorkType.objects.filter(available=True)
		self.fields['technique_instruction'].widget.attrs.update({'type': 'text'})
		self.fields['process_parameter'].queryset = LAMProcessParameters.objects.filter(available=True).order_by('name')

		# self.fields['available'].disabled = True
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


# 基础工序实例 浏览
class LAMTechInstSerialForm_Browse(ModelForm):
	title = '工序实例'
	modelname = 'LAM_TechInst_Serial'

	class Meta:
		model = LAM_TechInst_Serial
		# fields = ['technique_instruction','serial_number','serial_worktype','serial_note','serial_content']
		fields = "__all__"
		labels = {
			# 'filter_techinst': _('辅助筛选工艺文件'),
			'technique_instruction': _('工艺文件'),
			'serial_number': _('工序号'),
			'serial_worktype': _('工序名称'),
			'serial_note': _('工序概述'),
			'serial_content': _('工序内容'),
			'available': _('是否激活'),
			'process_parameter': _('参数包'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.fields['technique_instruction'].queryset = LAMTechniqueInstruction.objects.filter(available=True)
		self.fields['serial_worktype'].queryset = LAMProductionWorkType.objects.filter(available=True)
		self.fields['technique_instruction'].widget.attrs.update({'type': 'text'})

		# self.fields['available'].disabled = True
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})

class LAMProcessParameters_Browse(ModelForm):
# 	''' edit on 20200122 编辑中，未完成'''
# 	edit 20200122
	title = '激光成形参数包设定'
	modelname = 'LAMProcessParameters'
	previewtableTitle = '条件单元'
	previewtablefields = {'level': _('优先级别'), 'precondition': _('先决条件'),'expression': _('工艺范围描述'),
	                      'comment': _('简述'),'instead_Cond_Cell':_('替换条件单元')}
	previewtable2_Title = '适用工序'
	previewtable2_fields = {'technique_instruction': _('工艺文件'),
	                        'serial_number': _('编号'),
	                        'serial_worktype': _('名称'),
	                        'serial_note': _('概述'),
	                        'process_parameter':_('参数包'),
	                        }
	class Meta:
		model = LAMProcessParameters
		fields = ['name', 'comment']
		# fields = "__all__"

		labels = {
			'name': _('参数包名称'),
			'comment': _('参数包简述'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# 原始field
		self.OriginalFields = ('name', 'comment')

		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


class LAMProcessParameters_Edit(ModelForm):
	title = '激光成形参数包实例'
	modelname = 'LAMProcessParameters'
	class Meta:
		model = LAMProcessParameters
		fields = ['name', 'comment', 'available']

		# fields = "__all__"
		labels = {
			'name': _('参数包名称'),
			'comment': _('参数包简述'),
			'available': _('是否激活'),
		}
		error_messages = ''
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['available'].disabled = True
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})

class LAMProcessConditionalCell_Edit(ModelForm):
	title = '激光成形参数条件单元实例'
	modelname = 'LAMProcessParameterConditionalCell'
	class Meta:
		model = LAMProcessParameterConditionalCell
		fields = ['level', 'precondition', 'expression','comment','instead_Cond_Cell']

		# fields = "__all__"
		widgets = {
			'level': widgets.TextInput(
				attrs={'type': 'number', 'placeholder': '级别数值越小，表明条件越基础；级别数值越大，表明条件越特殊；'}),
			'precondition': widgets.Textarea(
				attrs={'type': 'text', 'placeholder': '本条件单元触发的先决条件'}),
			'expression': widgets.Textarea(
				attrs={'type': 'text', 'placeholder': '触发本条件单元后的工艺范围描述'}),
		}
		labels = {
			'level': _('优先级别'),
			'instead_Cond_Cell': _('替代条件单元'),
			'precondition': _('先决条件'),
			'expression': _('工艺范围描述'),
			'comment': _('简述'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		if 'ProcessParameterID' in kwargs:
			# 新建
			super().__init__(*args, {})
		else:
			# 编辑
			super().__init__(*args, **kwargs)

		self.taglist = [
			'and',
			'or',
			'not',
			'{P_programname}',
			'{P_laser}',
			'{P_oxy}',
			'{P_x}',
			'{P_y}',
			'{P_z}',
			'{P_feed}',
			'{P_scanspd}',
			'{P_TimeStamp}',
			'{Sigma} A {Until CertainTime WHILE} B {/Sigma}',
			# '{NOW_TimeStamp}',
			'{Last_PowerOFF_TimeStamp}',
			# '{DeltaTime_To_Now}',
			'{Last_HeatTreatment_TimeStamp}']
		self.taglist_with_label = [
			('and','且'),
			('or','或'),
			('not','非'),
			('{P_programname}', '程序文件名'),
			('{P_laser}','激光功率(W)'),
			('{P_oxy}','气氛氧含量(ppm)'),
			('{P_x}','工件坐标X(mm)'),
			('{P_y}','工件坐标Y(mm)'),
			('{P_z}','工件坐标Z(mm)'),
			('{P_feed}','机床进给率(%)'),
			('{P_scanspd}','移动扫描速率(mm/min)'),
			('{P_TimeStamp}','数据点时间戳(second)'),
			('{Sigma} A {Until CertainTime WHILE} B {/Sigma}','计算至当前时刻，当B为真时A叠加值'),
			# ('{NOW_TimeStamp}','当前时间戳(second)'),
			('{Last_PowerOFF_TimeStamp}','数据点以前最近一次激光停光时间戳(second)'),
			# ('{DeltaTime_To_Now}','数据点距今时间(second)'),
			('{Last_HeatTreatment_TimeStamp}','数据点以前最近一次无应力状态时间戳(second)')]
		if 'ProcessParameterID' in kwargs:
			_parameter = LAMProcessParameters.objects.get(id=kwargs['ProcessParameterID'])
		else:
			# pass CondCell_Parameter
			_parameter=kwargs['instance'].CondCell_Parameter.all()[0]
		# qset = (
		# 		Q(id__gte=Current_i * num_per_page) &
		# 		Q(id__lt=(Current_i + 1) * num_per_page) &
		# 		Q(acquisition_timestamp__isnull=True)
		# )
		self.fields['instead_Cond_Cell'].queryset = _parameter.conditional_cell.all()
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})

	def is_valid_custom(self):
		try:
			if not self.data['instead_Cond_Cell']=='':
				_instead_Cond_Cell_level = LAMProcessParameterConditionalCell.objects.get(id=self.data['instead_Cond_Cell']).level
				_level = int(self.data['level'])
				if _level <= _instead_Cond_Cell_level:
					self.error_messages = '只可替换比其级别低的条件单元'
					return False

		except:
			self.error_messages = '未知错误'
			return False

		return self.is_valid()

class LAMProcessParameterTechInshSerial_Edit(forms.Form):

	TechInshSerialList = forms.fields.MultipleChoiceField(
		# choices=((_serial.id, str(_serial)) for _serial in all_techinst_serial_datalist),
		# choices=((1, "篮球"), (2, "足球"), (3, "双色球"),),
		label="适用工序",
		initial=[],
		widget=forms.widgets.SelectMultiple()
	)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		all_techinst_serial_datalist = LAM_TechInst_Serial.objects.filter(available=True)
		self.fields['TechInshSerialList'].choices = ((_serial.id, str(_serial)) for _serial in all_techinst_serial_datalist)
		# 或
		# self.fields['TechInshSerialList'].choices = LAM_TechInst_Serial.Classes.objects.all().values_list('id', 'caption')
	def selectchoices(self, choiceIDList):
		self.fields['TechInshSerialList'].initial=choiceIDList

# 取样部位
class SamplingPositionForm(ModelForm):
	title = '取样部位'
	modelname = 'SamplingPosition'

	class Meta:
		model = SamplingPosition
		fields = "__all__"
		labels = {
			'PositionName': _('部位名称'),
			'PositionCode': _('代码'),
			'available': _('是否激活'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['available'].disabled = True
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


# 取样方向
class SamplingDirectionForm(ModelForm):
	title = '取样方向'
	modelname = 'SamplingDirection'

	class Meta:
		model = SamplingDirection
		fields = "__all__"
		labels = {
			'DirectionName': _('方向名称'),
			'DirectionCode': _('代码'),
			'available': _('是否激活'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['available'].disabled = True
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


# 热处理状态
class HeatTreatmentStateForm(ModelForm):
	title = '热处理状态'
	modelname = 'HeatTreatmentState'

	class Meta:
		model = HeatTreatmentState
		fields = "__all__"
		labels = {
			'heattreatmentstate_name': _('热处理状态'),
			'available': _('是否激活'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['available'].disabled = True
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


# # 激光成形产品
# class LAMProductForm(forms.Form):
#     # 产品类型
#     product_category = forms.ModelChoiceField(label='产品名称', queryset=LAMProductCategory.objects.all())
#     # 零件编号
#     product_code = forms.CharField(max_length=50)

# 产品类别
class LAMProductForm(ModelForm):
	title = '产品实例'
	modelname = 'LAMProduct'

	class Meta:
		model = LAMProduct
		fields = "__all__"
		labels = {
			'product_category': _('产品类别'),
			'product_code': _('产品编号'),
			'available': _('是否激活'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['available'].disabled = True
		self.fields['product_category'].queryset = LAMProductCategory.objects.filter(available=True)
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


# 产品类别与工艺文件的关联
# class LAMProdCate_TechInstForm(ModelForm):
#     title = '产品类别与工艺文件的关联'
#     modelname = 'LAMProdCate_TechInst'
#     class Meta:
#         model = LAMProdCate_TechInst
#         fields = "__all__"
#         labels = {
#             'lamproductcategory': _('产品类别'),
#             'lamtechniqueinstruction': _('工艺文件'),
#             'available': _('是否激活'),
#         }
#         error_messages = ''
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['available'].disabled = True
#         self.fields['lamproductcategory'].queryset = LAMProductCategory.objects.filter(available=True)
#         self.fields['lamtechniqueinstruction'].queryset = LAMTechniqueInstruction.objects.filter(available=True)
#         for field in self.fields.values():
#             field.widget.attrs.update({'class':'form-control'})


# 激光成形生产任务_编辑
class LAMProcessMissionForm_Edit(ModelForm):
	title = '生产任务实例'
	modelname = 'LAMProcessMission'
	previewtableTitle = '产品任务'
	previewtablefields = {'LAM_techinst_serial': _('下达任务工序'), 'arrangement_date': _('下达任务日期'),
	                      'completion_date': _('完成任务日期')}

	class Meta:
		model = LAMProcessMission
		fields = ['LAM_product', 'LAM_techinst_serial', 'work_section', 'arrangement_date']
		# fields = "__all__"
		widgets = {
			'arrangement_date': widgets.TextInput(
				attrs={'type': 'date', 'value': str(datetime.date.today()), 'placeholder': '请选择任务下达日期'}),
			'completion_date': widgets.TextInput(attrs={'type': 'date', 'placeholder': '请选择任务完成日期'}),

		}
		labels = {
			'LAM_product': _('零件实例'),
			'LAM_techinst_serial': _('下达任务工序'),
			'work_section': _('工段'),
			'arrangement_date': _('下达任务日期'),
			'completion_date': _('完成任务日期'),
			'available': _('是否激活'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['LAM_product'].widget.attrs.update(
			{'onchange': 'loadTableData_ProductMission(this.value)'})

		# 辅助选择数据集
		self.techinst_datalist = LAMTechniqueInstruction.objects.filter(Q(available=True) & Q(filed=False)).order_by(
			'instruction_code', '-version_code', '-version_number')
		# print(self.techinst_datalist)
		self.worktype_datalist = LAMProductionWorkType.objects.filter(available=True)
		self.productcode_datalist = LAMProduct.objects.filter(available=True)

		self.fields['LAM_product'].queryset = LAMProduct.objects.filter(available=True)

		NotFiledTechInst = LAMTechniqueInstruction.objects.filter(Q(filed=False) & Q(available=True))
		self.fields['LAM_techinst_serial'].queryset = LAM_TechInst_Serial.objects.filter(
			Q(available=True) & Q(technique_instruction__filed=False))
		self.fields['work_section'].queryset = Worksection.objects.filter(available=True)
		# self.fields['completion_date'].disabled = True
		# self.fields['available'].disabled = True

		# 辅助选择下拉菜单及文本框
		# self.fields['product_category'] = forms.ModelChoiceField(label='产品类别',
		#                                                          queryset=LAMProductCategory.objects.filter(
		#                                                              available=True),
		#                                                          empty_label='请选择产品类别',
		#                                                          required=False)
		self.fields['product_code'] = forms.CharField(label='零件编号',
		                                              max_length=50,
		                                              required=False)
		self.fields['technique_instruction'] = forms.ModelChoiceField(label='工艺文件',
		                                                              queryset=self.techinst_datalist,
		                                                              empty_label='请选择工艺文件',
		                                                              required=False)
		self.fields['work_type'] = forms.ModelChoiceField(label='工序',
		                                                  queryset=self.worktype_datalist,
		                                                  empty_label='请选择工序',
		                                                  required=False)

		# 更新属性
		# 产品类别
		# self.fields['product_category'].widget.attrs.update(
		#     {'onchange': 'load_LAMTechInstandProduct_By_ProductCategory(this.value);'})
		# 工艺文件
		self.fields['technique_instruction'].widget.attrs.update(
			{'onchange': 'load_WorkType_By_LAMTechInst(this.value);'})
		# 工序
		self.fields['work_type'].widget.attrs.update(
			{'onchange': 'refresh_techinst_serial();'})

		self.fields['product_code'].widget.attrs.update(
			{'list': 'product_code_list', 'onblur': 'refresh_product();'})

		# 辅助选择field
		self.AuxiliarySelection = ('product_category',
		                           'technique_instruction',
		                           'work_type',
		                           'product_code')
		# 原始field
		self.OriginalFields = ('LAM_product', 'LAM_techinst_serial', 'work_section', 'arrangement_date')

		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})

	def is_valid_custom(self):

		try:
			_Product = LAMProduct.objects.get(id=self.data['LAM_product'])
			_ProdCate = _Product.product_category
			_TechInst = LAM_TechInst_Serial.objects.get(id=self.data['LAM_techinst_serial']).technique_instruction

			if not (_Product in _TechInst.product.all() or _ProdCate in _TechInst.product_category.all()):
				self.error_messages = '该产品与选中工艺文件未关联'
				return False
		# LAMTechniqueInstruction.objects.filter(Q(product_category=_ProdCate) | Q(product=_Product))

		# all_datadict = LAMTechniqueInstruction.objects.filter(
		#     Q(product_category=filtecondition_ProdCate) | Q(product=filtecondition_Product)).order_by(
		#     'instruction_code')
		#
		#
		# # _ProdCate_id = LAMProduct.objects.get(id=self.data['LAM_product']).product_category
		# _TechInst_id = LAM_TechInst_Serial.objects.get(id=self.data['LAM_techinst_serial']).technique_instruction.id
		#
		# _filter_list = LAMProdCate_TechInst.objects.filter(lamproductcategory = _ProdCate_id,
		#                                     lamtechniqueinstruction = _TechInst_id)
		# if len(_filter_list)==0:
		#     self.error_messages = '该产品与选中工艺文件未关联'
		#     return False
		except:
			self.error_messages = '未知错误'
			return False

		return self.is_valid()


# 激光成形生产任务_完成任务
class LAMProcessMissionForm_Finish(ModelForm):
	title = '生产任务实例'
	modelname = 'LAMProcessMission'

	class Meta:
		model = LAMProcessMission
		# fields = ['LAM_product','LAM_techinst_serial','work_section','arrangement_date']
		fields = "__all__"
		widgets = {
			'arrangement_date': widgets.TextInput(
				attrs={'type': 'date', 'value': str(datetime.date.today()), 'placeholder': '请选择任务下达日期'}),
			'completion_date': widgets.TextInput(
				attrs={'type': 'date', 'value': str(datetime.date.today()), 'placeholder': '请选择任务完成日期'}),
		}
		labels = {
			'LAM_product': _('零件实例'),
			'LAM_techinst_serial': _('下达任务工序'),
			'work_section': _('工段'),
			'arrangement_date': _('下达任务日期'),
			'completion_date': _('完成任务日期'),
			'available': _('是否激活'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# 辅助选择数据集
		self.techinst_datalist = LAMTechniqueInstruction.objects.filter(available=True).order_by('instruction_code',
		                                                                                         '-version_code',
		                                                                                         '-version_number')
		self.worktype_datalist = LAMProductionWorkType.objects.filter(available=True)
		self.productcode_datalist = LAMProduct.objects.filter(available=True)

		self.fields['if_techinst_filed'] = forms.BooleanField(label='工艺文件归档',
		                                                      required=False)
		self.fields['LAM_product'].disabled = True
		self.fields['LAM_techinst_serial'].disabled = True
		self.fields['work_section'].disabled = True
		self.fields['arrangement_date'].disabled = True
		self.fields['available'].disabled = True
		_TechInst = LAM_TechInst_Serial.objects.get(id=self.initial['LAM_techinst_serial']).technique_instruction
		if _TechInst.temporary == 0:
			self.fields['if_techinst_filed'].disabled = True

		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})

	def save_custom(self):
		self.save()
		_TechInst = LAM_TechInst_Serial.objects.get(id=self.initial['LAM_techinst_serial']).technique_instruction
		if _TechInst.temporary == 1:
			if 'if_techinst_filed' in self.data and self.data['if_techinst_filed'] == 'on':
				_TechInst.filed = 1
			else:
				_TechInst.filed = 0
			# _TechInst.filed = [0, 1][self.data['if_techinst_filed']=='on']
			_TechInst.save()
	# print('_TechInst.temporary == 1')


# 激光成形生产任务_浏览
class LAMProcessMissionForm_Browse(ModelForm):
	title = '生产任务实例'
	modelname = 'LAMProcessMission'

	class Meta:
		model = LAMProcessMission
		# fields = ['technique_instruction','serial_number','serial_worktype','serial_note','serial_content']
		fields = "__all__"
		widgets = {
			'arrangement_date': widgets.TextInput(
				attrs={'type': 'date', 'value': str(datetime.date.today()), 'placeholder': '请选择任务下达日期'}),
			'completion_date': widgets.TextInput(attrs={'type': 'date', 'placeholder': '请选择任务完成日期'}),

		}
		labels = {
			'LAM_product': _('零件编号'),
			'LAM_techinst_serial': _('下达任务工序'),
			'work_section': _('工段'),
			'arrangement_date': _('下达任务日期'),
			'completion_date': _('完成任务日期'),
			'available': _('是否激活'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.fields['LAM_product'].queryset = LAMProduct.objects.filter(available=True)
		self.fields['LAM_techinst_serial'].queryset = LAM_TechInst_Serial.objects.filter(available=True)
		self.fields['work_section'].queryset = Worksection.objects.filter(available=True)
		self.fields['completion_date'].disabled = True
		self.fields['available'].disabled = True
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


'''edit 20191119'''


class LAMProcessMission_TimeCutRecordsForm(ModelForm):
	title = '划分成形任务的过程数据'
	modelname = 'Process_Mission_timecut'

	class Meta:
		model = Process_Mission_timecut
		fields = ['id', 'process_mission',
		          'process_start_time',
		          'process_finish_time',
		          # 'laserdata_start_id',
		          # 'laserdata_finish_id',
		          # 'oxygendata_start_id',
		          # 'oxygendata_finish_id',
		          # 'cncstatusdata_start_id',
		          # 'cncstatusdata_finish_id'
		          ]

		# fields = "__all__"
		labels = {
			'process_mission': _('生产任务'),
			# 'process_start_date': _('激光成形过程开始日期'),
			# 'process_finish_date': _('激光成形过程结束日期'),
			'process_start_time': _('激光成形过程开始时间'),
			'process_finish_time': _('激光成形过程结束时间'),
			# 'laserdata_start_id': _('激光器采集数据起始id'),
			# 'laserdata_finish_id': _('激光器采集数据结束id'),
			# 'oxygendata_start_id': _('氧分析仪采集数据起始id'),
			# 'oxygendata_finish_id': _('氧分析仪采集数据结束id'),
			# 'cncstatusdata_start_id': _('数控机床采集数据起始id'),
			# 'cncstatusdata_finish_id': _('数控机床采集数据结束id'),
		}
		widgets = {
			'process_start_time': widgets.TextInput(
				attrs={'type': 'datetime-local','step':1, 'value': str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")),
				       'placeholder': '请选择激光成形过程开始时间'}),
			'process_finish_time': widgets.TextInput(
				attrs={'type': 'datetime-local','step':1, 'value': str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")),
				       'placeholder': '请选择激光成形过程结束时间'}),
			# 'temp_process_start_date': widgets.TextInput(
			# 	attrs={'type': 'date', 'value': str(datetime.datetime.now().strftime("%Y-%m-%d")),
			# 	       'placeholder': '请选择右图曲线的起始日期'}),
			# 'temp_process_finish_date': widgets.TextInput(
			# 	attrs={'type': 'date', 'value': str(datetime.datetime.now().strftime("%Y-%m-%d")),
			# 	       'placeholder': '请选择右图曲线的结束日期'}),
			# 'process_start_time': widgets.TextInput(
			# 	attrs={'type': 'time', 'value': '00:00',
			# 	       'placeholder': '请选择激光成形过程开始时间'}),
			# 'process_finish_time': widgets.TextInput(
			# 	attrs={'type': 'time', 'value': '23:59',
			# 	       'placeholder': '请选择激光成形过程结束时间'})
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# 辅助选择数据集
		# self.techinst_datalist = LAMTechniqueInstruction.objects.filter(Q(available=True) & Q(filed=False)).order_by(
		# 	'instruction_code', '-version_code', '-version_number')
		# # print(self.techinst_datalist)
		# self.worktype_datalist = LAMProductionWorkType.objects.filter(available=True)
		# self.productcode_datalist = LAMProduct.objects.filter(available=True)
		#
		# self.fields['LAM_product'].queryset = LAMProduct.objects.filter(available=True)
		#
		# NotFiledTechInst = LAMTechniqueInstruction.objects.filter(Q(filed=False) & Q(available=True))
		# self.fields['LAM_techinst_serial'].queryset = LAM_TechInst_Serial.objects.filter(
		# 	Q(available=True) & Q(technique_instruction__filed=False))
		# self.fields['work_section'].queryset = Worksection.objects.filter(available=True)
		self.productcode_datalist = LAMProduct.objects.filter(available=True)

		self.fields['product_category'] = forms.ModelChoiceField(label='产品类别',
		                                                         queryset=LAMProductCategory.objects.filter(
			                                                         available=True),
		                                                         empty_label='请选择产品类别',
		                                                         required=False)
		self.fields['worksection'] = forms.ModelChoiceField(label='激光成形工段',
		                                                    queryset=Worksection.objects.filter(available=True),
		                                                    empty_label='请选择激光成形工段',
		                                                    required=False)
		self.fields['product_code'] = forms.CharField(label='零件编号',
		                                              max_length=50,
		                                              required=False)

		self.fields['temp_process_start_date'] = forms.DateField(label='从',
		                                                         widget=widgets.TextInput(
			                                                         attrs={'type': 'date',
			                                                                'value': str((
					                                                                datetime.datetime.now() - datetime.timedelta(
				                                                                days=1)).strftime(
				                                                                "%Y-%m-%d")),
			                                                                'placeholder': '请选择右图曲线的起始日期'}),
		                                                         required=False)
		self.fields['temp_process_finish_date'] = forms.DateField(label='到',
		                                                          widget=widgets.TextInput(
			                                                          attrs={'type': 'date', 'value': str(
				                                                          datetime.datetime.now().strftime("%Y-%m-%d")),
			                                                                 'placeholder': '请选择右图曲线的结束日期'}),
		                                                          required=False)
		self.fields['product_category'].name = 'product_category'
		self.fields['worksection'].name = 'worksection'
		self.fields['product_code'].name = 'product_code'
		self.fields['temp_process_start_date'].name = 'temp_process_start_date'
		self.fields['temp_process_finish_date'].name = 'temp_process_finish_date'
		# 辅助选择field
		self.AuxiliarySelection = ('temp_process_start_date',
		                           'temp_process_finish_date',
		                           'product_category',
		                           'worksection',
		                           'product_code'
		                           )
		self.AuxiliarySelection_with_row = (
			('temp_process_start_date', 'temp_process_finish_date'), ('product_category', 'worksection'),
			('product_code'))

		# 原始field
		self.OriginalFields = ('process_mission',
		                       'process_start_time',
		                       'process_finish_time',
		                       'laserdata_start_id',
		                       'laserdata_finish_id',
		                       'oxygendata_start_id',
		                       'oxygendata_finish_id',
		                       'cncstatusdata_start_id',
		                       'cncstatusdata_finish_id')

		# self.fields['process_start_time'].disabled = True
		# self.fields['process_finish_time'].disabled = True

		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})

		self.fields['product_code'].widget.attrs.update(
			{'list': 'product_code_list', 'onblur': 'refresh_missionlist();'})
		self.fields['product_category'].widget.attrs.update(
			{'onblur': 'refresh_productlist();'})
		self.fields['process_mission'].widget.attrs.update(
			{'onchange': 'refresh_worksection_selection(this.value);refresh_start_finsh_datetime(this.value);'})

		# self.fields['laserdata_start_id'].widget.attrs.update({'type': 'hidden'})
		# self.fields['laserdata_finish_id'].widget.attrs.update({'type': 'hidden'})
		# self.fields['oxygendata_start_id'].widget.attrs.update({'type': 'hidden'})
		# self.fields['oxygendata_finish_id'].widget.attrs.update({'type': 'hidden'})
		# self.fields['cncstatusdata_start_id'].widget.attrs.update({'type': 'hidden'})
		# self.fields['cncstatusdata_start_id'].widget.attrs.update({'type': 'hidden'})

		self.AuxiliarySelectionField_with_row = (
			(self.fields['product_category'], self.fields['product_code']),
		)
		self.GraphOperatorField_with_row = (
			(self.fields['temp_process_start_date'], self.fields['temp_process_finish_date'],self.fields['worksection']),
		)
		self.ChangeableFieldname = 'process_mission'


'''edit 20191220'''
class LAMProcess_Worksection_OperateForm(ModelForm):
	title = '激光成形现场操作'
	modelname = 'Process_Mission_timecut'

	class Meta:
		model = Process_Mission_timecut
		fields = ['id', 'process_mission',
		          'process_start_time',
		          'process_finish_time',
		          ]

		# fields = "__all__"
		labels = {
			'process_mission': _('生产任务'),
			'process_start_time': _('激光成形过程开始时间'),
			'process_finish_time': _('激光成形过程结束时间'),
		}
		widgets = {
			'process_start_time': widgets.TextInput(
				attrs={'type': 'datetime-local', 'step': 1,
				       # 'value': str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")),
				       'placeholder': '激光成形过程开始时间'}),
			'process_finish_time': widgets.TextInput(
				attrs={'type': 'datetime-local', 'step': 1,
				       # 'value': str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")),
				       'placeholder': '激光成形过程结束时间'}),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# super().__init__((), {})
		# 辅助选择数据集
		# work_section
		# arrangement_date
		# completion_date
		# available
		self.fields['process_start_time'].disabled = True
		self.fields['process_finish_time'].disabled = True
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})

	def setMissionQueryset(self, worksection_id):
		self.fields['process_mission'].queryset = LAMProcessMission.objects.filter(Q(available=True)&Q(work_section=worksection_id)&Q(completion_date=None))

	def refresh_by_currentmission(self, worksection_id):
		crtmission_obj = Worksection_Current_LAMProcessMission.objects.get(work_section = worksection_id)
		if crtmission_obj.if_onwork:
			# 正在执行
			self.initial['process_mission'] = [crtmission_obj.process_mission.id]
			# self.fields['process_mission'].widget.attrs.update({'selected':crtmission_obj.process_mission.id})
			# self.fields['process_mission'].widget._empty_value=[crtmission_obj.process_mission.id]
			# self.inital['process_mission']=crtmission_obj.process_mission.id
			# self.fields['process_mission'].value=crtmission_obj.process_mission.id
			self.fields['process_mission'].disabled = True
			_mission_attr_obj = Process_Mission_timecut.objects.get(process_mission = crtmission_obj.process_mission)

			self.fields['process_start_time'].widget.attrs.update({'value': _mission_attr_obj.process_start_time.strftime("%Y-%m-%dT%H:%M:%S")})
			self.fields['process_finish_time'].widget.attrs.update({'value': _mission_attr_obj.process_finish_time.strftime("%Y-%m-%dT%H:%M:%S")})
			# print(_mission_attr_obj.process_start_time)
			# print(_mission_attr_obj.process_finish_time)
		return crtmission_obj.if_onwork

		# self.fields['product_category'] = forms.ModelChoiceField(label='产品类别',
		#                                                          queryset=LAMProductCategory.objects.filter(
		# 	                                                         available=True),
		#                                                          empty_label='请选择产品类别',
		#                                                          required=False)
		# self.fields['worksection'] = forms.ModelChoiceField(label='激光成形工段',
		#                                                     queryset=Worksection.objects.filter(available=True),
		#                                                     empty_label='请选择激光成形工段',
		#                                                     required=False)
		# self.fields['product_code'] = forms.CharField(label='零件编号',
		#                                               max_length=50,
		#                                               required=False)
		#
		# self.fields['temp_process_start_date'] = forms.DateField(label='从',
		#                                                          widget=widgets.TextInput(
		# 	                                                         attrs={'type': 'date',
		# 	                                                                'value': str((
		# 			                                                                datetime.datetime.now() - datetime.timedelta(
		# 		                                                                days=1)).strftime(
		# 		                                                                "%Y-%m-%d")),
		# 	                                                                'placeholder': '请选择右图曲线的起始日期'}),
		#                                                          required=False)
		# self.fields['temp_process_finish_date'] = forms.DateField(label='到',
		#                                                           widget=widgets.TextInput(
		# 	                                                          attrs={'type': 'date', 'value': str(
		# 		                                                          datetime.datetime.now().strftime("%Y-%m-%d")),
		# 	                                                                 'placeholder': '请选择右图曲线的结束日期'}),
		#                                                           required=False)
		# self.fields['product_category'].name = 'product_category'
		# self.fields['worksection'].name = 'worksection'
		# self.fields['product_code'].name = 'product_code'
		# self.fields['temp_process_start_date'].name = 'temp_process_start_date'
		# self.fields['temp_process_finish_date'].name = 'temp_process_finish_date'
		# # 辅助选择field
		# self.AuxiliarySelection = ('temp_process_start_date',
		#                            'temp_process_finish_date',
		#                            'product_category',
		#                            'worksection',
		#                            'product_code'
		#                            )
		# self.AuxiliarySelection_with_row = (
		# 	('temp_process_start_date', 'temp_process_finish_date'), ('product_category', 'worksection'),
		# 	('product_code'))
		#
		# # 原始field
		# self.OriginalFields = ('process_mission',
		#                        'process_start_time',
		#                        'process_finish_time',
		#                        'laserdata_start_id',
		#                        'laserdata_finish_id',
		#                        'oxygendata_start_id',
		#                        'oxygendata_finish_id',
		#                        'cncstatusdata_start_id',
		#                        'cncstatusdata_finish_id')
		#
		# # self.fields['process_start_time'].disabled = True
		# # self.fields['process_finish_time'].disabled = True
		#
		# for field in self.fields.values():
		# 	field.widget.attrs.update({'class': 'form-control'})
		#
		# self.fields['product_code'].widget.attrs.update(
		# 	{'list': 'product_code_list', 'onblur': 'refresh_missionlist();'})
		# self.fields['product_category'].widget.attrs.update(
		# 	{'onblur': 'refresh_productlist();'})
		# self.fields['process_mission'].widget.attrs.update(
		# 	{'onchange': 'refresh_worksection_selection(this.value);refresh_start_finsh_datetime(this.value);'})
		#
		# # self.fields['laserdata_start_id'].widget.attrs.update({'type': 'hidden'})
		# # self.fields['laserdata_finish_id'].widget.attrs.update({'type': 'hidden'})
		# # self.fields['oxygendata_start_id'].widget.attrs.update({'type': 'hidden'})
		# # self.fields['oxygendata_finish_id'].widget.attrs.update({'type': 'hidden'})
		# # self.fields['cncstatusdata_start_id'].widget.attrs.update({'type': 'hidden'})
		# # self.fields['cncstatusdata_start_id'].widget.attrs.update({'type': 'hidden'})
		#
		# self.AuxiliarySelectionField_with_row = (
		# 	(self.fields['product_category'], self.fields['product_code']),
		# )
		# self.GraphOperatorField_with_row = (
		# 	(self.fields['temp_process_start_date'], self.fields['temp_process_finish_date'],self.fields['worksection']),
		# )
		# self.ChangeableFieldname = 'process_mission'



# 生产过程开始时间
# self.fields['process_start_time'].widget.attrs.update(
# 	{'onchange': 'load_StartDateData_By_Process();'})
# # 生产过程结束时间
# self.fields['process_finish_time'].widget.attrs.update(
# 	{'onchange': 'load_FinishDateData_By_Process();'})
#
#
#
# title = '划分成形任务的过程数据'
# modelname = 'Process_Mission_timecut'
# class Meta:
#     model = Process_Mission_timecut
#     # fields = ['LAM_product','LAM_techinst_serial','work_section','arrangement_date']
#     fields = "__all__"
#     widgets = {
#         'arrangement_date': widgets.TextInput(attrs={'type': 'date','value':str(datetime.date.today()), 'placeholder': '请选择任务下达日期'}),
#         'completion_date': widgets.TextInput(attrs={'type': 'date', 'placeholder': '请选择任务完成日期'}),
#
#     }
#     labels = {
#         'LAM_product': _('零件实例'),
#         'LAM_techinst_serial': _('下达任务工序'),
#         'work_section': _('工段'),
#         'arrangement_date': _('下达任务日期'),
#         'completion_date': _('完成任务日期'),
#         'available': _('是否激活'),
#     }
#     error_messages = ''
#
# def __init__(self, *args, **kwargs):
#     super().__init__(*args, **kwargs)
#     self.fields['LAM_product'].widget.attrs.update(
#         {'onchange': 'loadTableData_ProductMission(this.value)'})
#
#     # 辅助选择数据集
#     self.techinst_datalist = LAMTechniqueInstruction.objects.filter(Q(available=True)&Q(filed=False)).order_by('instruction_code', '-version_code', '-version_number')
#     # print(self.techinst_datalist)
#     self.worktype_datalist = LAMProductionWorkType.objects.filter(available=True)
#     self.productcode_datalist = LAMProduct.objects.filter(available=True)
#
#
#     self.fields['LAM_product'].queryset = LAMProduct.objects.filter(available=True)
#
#     NotFiledTechInst = LAMTechniqueInstruction.objects.filter(Q(filed=False)&Q(available=True))
#     self.fields['LAM_techinst_serial'].queryset = LAM_TechInst_Serial.objects.filter(Q(available=True)&Q(technique_instruction__filed=False))
#     self.fields['work_section'].queryset = Worksection.objects.filter(available=True)
#     # self.fields['completion_date'].disabled = True
#     # self.fields['available'].disabled = True
#
#     # 辅助选择下拉菜单及文本框
#     # self.fields['product_category'] = forms.ModelChoiceField(label='产品类别',
#     #                                                          queryset=LAMProductCategory.objects.filter(
#     #                                                              available=True),
#     #                                                          empty_label='请选择产品类别',
#     #                                                          required=False)
#     self.fields['product_code'] = forms.CharField(label='零件编号',
#                                                   max_length=50,
#                                                   required=False)
#     self.fields['technique_instruction'] = forms.ModelChoiceField(label='工艺文件',
#                                                                   queryset=self.techinst_datalist,
#                                                              empty_label='请选择工艺文件',
#                                                              required=False)
#     self.fields['work_type'] = forms.ModelChoiceField(label='工序',
#                                                       queryset=self.worktype_datalist,
#                                                              empty_label='请选择工序',
#                                                              required=False)
#
#     # 更新属性
#     # 产品类别
#     # self.fields['product_category'].widget.attrs.update(
#     #     {'onchange': 'load_LAMTechInstandProduct_By_ProductCategory(this.value);'})
#     # 工艺文件
#     self.fields['technique_instruction'].widget.attrs.update(
#         {'onchange': 'load_WorkType_By_LAMTechInst(this.value);'})
#     # 工序
#     self.fields['work_type'].widget.attrs.update(
#         {'onchange': 'refresh_techinst_serial();'})
#
#     self.fields['product_code'].widget.attrs.update(
#         {'list': 'product_code_list', 'onblur': 'refresh_product();'})
#
#     # 辅助选择field
#     self.AuxiliarySelection = ('product_category',
#                                'technique_instruction',
#                                'work_type',
#                                'product_code')
#     # 原始field
#     self.OriginalFields = ('LAM_product','LAM_techinst_serial','work_section','arrangement_date')
#
#     for field in self.fields.values():
#         field.widget.attrs.update({'class':'form-control'})
# def is_valid_custom(self):
#
#     try:
#         _Product = LAMProduct.objects.get(id = self.data['LAM_product'])
#         _ProdCate = _Product.product_category
#         _TechInst = LAM_TechInst_Serial.objects.get(id = self.data['LAM_techinst_serial']).technique_instruction
#
#         if not (_Product in _TechInst.product.all() or _ProdCate in _TechInst.product_category.all()):
#             self.error_messages = '该产品与选中工艺文件未关联'
#             return False
#
#     except:
#         self.error_messages = '未知错误'
#         return False
#
#     return self.is_valid()


# 拉伸测试数据
class MechanicalTest_TensileForm(ModelForm):
	title = '拉伸性能测试'
	modelname = 'MechanicalTest_Tensile'

	# previewtablefields = {
	#         'sample_number': _('试样编号'),
	#         'sampling_position': _('取样部位'),
	#         'sampling_direction': _('取样方向'),
	#         'test_temperature': _('测试温度'),
	#         'tensile_strength': _('抗拉强度/MPa'),
	#         'yield_strength': _('屈服强度/MPa'),
	#         'elongation': _('断后延伸率/%'),
	#         'areareduction': _('断面收缩率/%'),
	#         'modulus': _('弹性模量/GPa'),
	#     }

	class Meta:
		model = MechanicalTest_Tensile
		# fields = ['id','sample_number',
		#     'sampling_position',
		#     'sampling_direction',
		#     'test_temperature',
		#     'tensile_strength',
		#     'yield_strength',
		#     'elongation',
		#     'areareduction',
		#     'modulus','available','preWTestItemID']

		fields = "__all__"
		labels = {
			'sample_number': _('试样编号'),
			'sampling_position': _('取样部位'),
			'sampling_direction': _('取样方向'),
			'test_temperature': _('测试温度/℃'),
			'tensile_strength': _('抗拉强度/MPa'),
			'yield_strength': _('屈服强度/MPa'),
			'elongation': _('断后延伸率/%'),
			'areareduction': _('断面收缩率/%'),
			'modulus': _('弹性模量/GPa'),
			'available': _('是否有效'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


# 冲击测试数据
class MechanicalTest_ToughnessForm(ModelForm):
	title = '冲击性能测试'
	modelname = 'MechanicalTest_Toughness'

	# previewtablefields = {
	#         'sample_number': _('试样编号'),
	#         'sampling_position': _('取样部位'),
	#         'sampling_direction': _('取样方向'),
	#         'test_temperature': _('测试温度'),
	#         'tensile_strength': _('抗拉强度/MPa'),
	#         'yield_strength': _('屈服强度/MPa'),
	#         'elongation': _('断后延伸率/%'),
	#         'areareduction': _('断面收缩率/%'),
	#         'modulus': _('弹性模量/GPa'),
	#     }

	class Meta:
		model = MechanicalTest_Toughness
		# fields = ['id','sample_number',
		#     'sampling_position',
		#     'sampling_direction',
		#     'test_temperature',
		#     'tensile_strength',
		#     'yield_strength',
		#     'elongation',
		#     'areareduction',
		#     'modulus','available','preWTestItemID']

		fields = "__all__"
		labels = {
			'sample_number': _('试样编号'),
			'sampling_position': _('取样部位'),
			'sampling_direction': _('取样方向'),
			'test_temperature': _('测试温度/℃'),
			'toughness': _('冲击韧性 / J/cm<sup>2</sup>'),
			'available': _('是否有效'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


# 化学成分测试数据
class MechanicalTest_ChemicalForm(ModelForm):
	title = '化学成分测试'
	modelname = 'ChemicalTest'

	class Meta:
		model = ChemicalTest
		fields = ['sample_number', 'sampling_position']
		labels = {
			'sample_number': _('试样编号'),
			'sampling_position': _('取样部位'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})

	def addElementFields(self, chemical_items):
		# 根据ChemicalElement列表生成field
		for element in chemical_items:
			self.fields[element.element_code] = forms.FloatField(required=False)
			self.fields[element.element_code].widget.attrs.update({'class': 'form-control', 'min_value': 0.0})

	def refreshValue(self, chemicaltest_element_list):
		for element in chemicaltest_element_list:
			self.fields[element.element.element_code].widget.attrs.update({'value': element.value})
		# self.fields[element.element.element_code].value = element.value
		pass


# 产品理化检测
class ProductPhyChemTestForm_New(ModelForm):
	title = '产品理化检测'
	modelname = 'PhysicochemicalTest_Mission'

	class Meta:
		model = PhysicochemicalTest_Mission
		fields = ['LAM_product',
		          'LAM_techinst_serial',
		          'commission_date',
		          'heat_treatment_state',
		          ]
		widgets = {
			'commission_date': widgets.TextInput(
				attrs={'type': 'date', 'value': str(datetime.date.today()), 'placeholder': '请选择开始日期'}),
		}
		labels = {
			'LAM_product': _('产品实例'),
			'RawStock': _('原材料实例'),
			'LAM_techinst_serial': _('工序'),
			'commission_date': _('开始日期'),
			'heat_treatment_state': _('热处理状态'),
			'mechanicaltest_tensile': _('拉伸测试'),
			'mechanicaltest_toughness': _('冲击测试'),
			'chemicaltest': _('化学成分测试'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.fields['LAM_product'].disabled = True
		# self.fields['LAM_techinst_serial'].disabled = True
		# self.fields['commission_date'].disabled = True
		# self.fields['heat_treatment_state'].disabled = True

		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


# 产品理化检测
class ProductPhyChemTestForm_Edit(ModelForm):
	title = '产品理化检测'
	modelname = 'PhysicochemicalTest_Mission'
	# previewtablefields = {'LAM_techinst_serial': _('下达任务工序'), 'arrangement_date': _('下达任务日期'),
	#                       'completion_date': _('完成任务日期')}
	tensile_fields = [
		'试样编号',
		'取样部位',
		'取样方向',
		'测试温度/℃',
		'抗拉强度/MPa',
		'屈服强度/MPa',
		'断后延伸率/%',
		'断面收缩率/%',
		'弹性模量/GPa',
		'是否有效',
	]
	toughness_fields = [
		'试样编号',
		'取样部位',
		'取样方向',
		'测试温度/℃',
		'冲击韧性 / J/cm<sup>2</sup>',
		'是否有效',
	]

	class Meta:
		model = PhysicochemicalTest_Mission
		# fields='__all__'
		fields = ['LAM_product',
		          'LAM_techinst_serial',
		          'commission_date',
		          'heat_treatment_state',
		          # 'mechanicaltest_tensile',
		          # 'mechanicaltest_toughness',
		          # 'chemicaltest',
		          ]
		widgets = {
			'commission_date': widgets.TextInput(
				attrs={'type': 'date', 'value': str(datetime.date.today()), 'placeholder': '请选择开始日期'}),
		}
		labels = {
			'LAM_product': _('产品实例'),
			'RawStock': _('原材料实例'),
			'LAM_techinst_serial': _('工序'),
			'commission_date': _('开始日期'),
			'heat_treatment_state': _('热处理状态'),
			'mechanicaltest_tensile': _('拉伸测试'),
			'mechanicaltest_toughness': _('冲击测试'),
			'chemicaltest': _('化学成分测试'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['LAM_product'].disabled = True
		self.fields['LAM_techinst_serial'].disabled = True
		# self.fields['commission_date'].disabled = True
		self.fields['heat_treatment_state'].disabled = True

		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


# 产品理化检测
class ProductPhyChemTestForm_Browse(ModelForm):
	title = '产品理化检测'
	modelname = 'PhysicochemicalTest_Mission'

	class Meta:
		model = PhysicochemicalTest_Mission
		fields = ['LAM_product',
		          'LAM_techinst_serial',
		          'commission_date',
		          'heat_treatment_state',
		          'mechanicaltest_tensile',
		          'mechanicaltest_toughness',
		          'chemicaltest']
		widgets = {
			'commission_date': widgets.TextInput(
				attrs={'type': 'date', 'value': str(datetime.date.today()), 'placeholder': '请选择开始日期'}),
		}
		labels = {
			'LAM_product': _('产品实例'),
			'RawStock': _('原材料实例'),
			'LAM_techinst_serial': _('工序'),
			'commission_date': _('开始日期'),
			'heat_treatment_state': _('热处理状态'),
			'mechanicaltest_tensile': _('拉伸测试'),
			'mechanicaltest_toughness': _('冲击测试'),
			'chemicaltest': _('化学成分测试'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.fields['available'].disabled = True

		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


# 原材料理化检测
class RawStockPhyChemTestForm_New(ModelForm):
	title = '原材料理化检测'
	modelname = 'PhysicochemicalTest_Mission'

	class Meta:
		model = PhysicochemicalTest_Mission
		fields = ['RawStock',
		          'LAM_techinst_serial',
		          'commission_date',
		          'heat_treatment_state',
		          ]
		widgets = {
			'commission_date': widgets.TextInput(
				attrs={'type': 'date', 'value': str(datetime.date.today()), 'placeholder': '请选择开始日期'}),
		}
		labels = {
			'LAM_product': _('产品实例'),
			'RawStock': _('原材料实例'),
			'LAM_techinst_serial': _('工序'),
			'commission_date': _('开始日期'),
			'heat_treatment_state': _('热处理状态'),
			'mechanicaltest_tensile': _('拉伸测试'),
			'mechanicaltest_toughness': _('冲击测试'),
			'chemicaltest': _('化学成分测试'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


# 原材料理化检测
class RawStockPhyChemTestForm_Edit(ModelForm):
	title = '原材料理化检测'
	modelname = 'PhysicochemicalTest_Mission'
	# previewtablefields = {'LAM_techinst_serial': _('下达任务工序'), 'arrangement_date': _('下达任务日期'),
	#                       'completion_date': _('完成任务日期')}
	tensile_fields = [
		'试样编号',
		'取样部位',
		'取样方向',
		'测试温度/℃',
		'抗拉强度/MPa',
		'屈服强度/MPa',
		'断后延伸率/%',
		'断面收缩率/%',
		'弹性模量/GPa',
		'是否有效',
	]
	toughness_fields = [
		'试样编号',
		'取样部位',
		'取样方向',
		'测试温度/℃',
		'冲击韧性 / J/cm<sup>2</sup>',
		'是否有效',
	]

	class Meta:
		model = PhysicochemicalTest_Mission
		# fields='__all__'
		fields = ['RawStock',
		          'LAM_techinst_serial',
		          'commission_date',
		          'heat_treatment_state',
		          # 'mechanicaltest_tensile',
		          # 'mechanicaltest_toughness',
		          # 'chemicaltest',
		          ]
		widgets = {
			'commission_date': widgets.TextInput(
				attrs={'type': 'date', 'value': str(datetime.date.today()), 'placeholder': '请选择开始日期'}),
		}
		labels = {
			'LAM_product': _('产品实例'),
			'RawStock': _('原材料实例'),
			'LAM_techinst_serial': _('工序'),
			'commission_date': _('开始日期'),
			'heat_treatment_state': _('热处理状态'),
			'mechanicaltest_tensile': _('拉伸测试'),
			'mechanicaltest_toughness': _('冲击测试'),
			'chemicaltest': _('化学成分测试'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['RawStock'].disabled = True
		self.fields['LAM_techinst_serial'].disabled = True
		# self.fields['commission_date'].disabled = True
		self.fields['heat_treatment_state'].disabled = True

		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


# 原材料理化检测
class RawStockPhyChemTestForm_Browse(ModelForm):
	title = '原材料理化检测'
	modelname = 'PhysicochemicalTest_Mission'

	class Meta:
		model = PhysicochemicalTest_Mission
		fields = ['RawStock',
		          'LAM_techinst_serial',
		          'commission_date',
		          'heat_treatment_state',
		          'mechanicaltest_tensile',
		          'mechanicaltest_toughness',
		          'chemicaltest']
		widgets = {
			'commission_date': widgets.TextInput(
				attrs={'type': 'date', 'value': str(datetime.date.today()), 'placeholder': '请选择开始日期'}),
		}
		labels = {
			'LAM_product': _('产品实例'),
			'RawStock': _('原材料实例'),
			'LAM_techinst_serial': _('工序'),
			'commission_date': _('开始日期'),
			'heat_treatment_state': _('热处理状态'),
			'mechanicaltest_tensile': _('拉伸测试'),
			'mechanicaltest_toughness': _('冲击测试'),
			'chemicaltest': _('化学成分测试'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.fields['available'].disabled = True

		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})
