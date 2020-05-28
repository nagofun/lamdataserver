# coding=utf-8
from LAMProcessData.models import *
from django import forms
from django.forms import ModelForm, widgets
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
import datetime
from django.db import connection
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
		self.fields['workshop'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择厂房..."})
		self.fields['desktop_computer'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择桌面计算机..."})
		self.fields['cnc_computer'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择数控计算机..."})


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
		self.fields['chemicalelements'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择元素..."})


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
			'use_up': _('是否已用尽'),
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
		self.fields['material'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择材料..."})
		self.fields['rawstock_category'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择原材料类别..."})


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
			# 'use_up': _('是否已用尽'),
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
		self.fields['material'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择材料..."})
		self.fields['rawstock_category'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择原材料类别..."})


# 原材料发放回收台账-浏览
class RawStockSendRetrieveForm(ModelForm):
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
			'raw_stock_sent_amount': _('发放数量'),
			'retrieve_time': _('回收日期'),
			'send_addition': _('追加发放'),
			'raw_stock_unused_amount': _('未用粉末数量'),
			# 'raw_stock_primaryretrieve':_('一级回收粉实例'),
			'raw_stock_primaryretrieve_amount': _('一级回收粉数量'),
			# 'raw_stock_secondaryretrieve':_('二级回收粉实例'),
			'raw_stock_secondaryretrieve_amount': _('二级回收粉数量'),
		}
		error_messages = ''
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		

# 原材料发放台账
class RawStockSendForm(ModelForm):
	title = '原材料发放记录'
	modelname = 'RawStockSendRetrieve'
	sendaddition_fields = [
		'补发日期',
		'原材料实例',
		'数量（kg）',
	]
	class Meta:
		model = RawStockSendRetrieve
		# fields = "__all__"
		fields = ['send_time',
		          'LAM_mission',
		          'raw_stock',
		          'raw_stock_sent_amount',
		          ]
		widgets = {
			'send_time': widgets.TextInput(
				attrs={'type': 'date', 'value': str(datetime.date.today()), 'placeholder': '请选择发料日期'}),
			'retrieve_time': widgets.TextInput(attrs={'type': 'date', 'placeholder': '请选择收料日期'}),

		}
		labels = {
			'send_time': _('发料日期'),
			'LAM_mission': _('生产任务实例'),
			'raw_stock': _('原材料实例'),
			'raw_stock_sent_amount': _('发放数量'),
			'retrieve_time': _('回收日期'),
			'send_addition':_('追加发放'),
			'raw_stock_unused_amount': _('未用粉末数量'),
			# 'raw_stock_primaryretrieve':_('一级回收粉实例'),
			'raw_stock_primaryretrieve_amount': _('一级回收粉数量'),
			# 'raw_stock_secondaryretrieve':_('二级回收粉实例'),
			'raw_stock_secondaryretrieve_amount': _('二级回收粉数量'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		'''找出所有任务中产品类型的组合'''
		mission_product_category_typedict = {}
		with connection.cursor() as cursor:
			# cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
			cursor.execute(
				"SELECT lamdataserver.lamprocessdata_lamprocessmission_lam_product.lamprocessmission_id, group_concat(distinct lamdataserver.lamprocessdata_lamproduct.product_category_id) as categorylist FROM lamdataserver.lamprocessdata_lamprocessmission_lam_product inner join lamdataserver.lamprocessdata_lamproduct on lamdataserver.lamprocessdata_lamproduct.id=lamdataserver.lamprocessdata_lamprocessmission_lam_product.lamproduct_id group by  lamdataserver.lamprocessdata_lamprocessmission_lam_product.lamprocessmission_id ;")
			row = cursor.fetchall()
			for _record in row:
				_mission_id = _record[0]
				# _product_list = _record[1]
				_category_list = _record[1]
				if _category_list not in mission_product_category_typedict:
					mission_product_category_typedict[_category_list] = [_mission_id]
				else:
					mission_product_category_typedict[_category_list].append(_mission_id)
		mission_data = []
		for _category_list_str, _mission_list in mission_product_category_typedict.items():
			_category_list = _category_list_str.split(',')
			mission_data.append([
				','.join([str(LAMProductCategory.objects.get(id=category_id)) for category_id in _category_list]),
				[
					(mission_id, str(LAMProcessMission.objects.get(id=mission_id))) for mission_id in _mission_list if LAMProcessMission.objects.get(id=mission_id).LAM_techinst_serial.selectable_RawStockSendRetrieve
				]
			])
		self.fields['LAM_mission'].choices = mission_data
		
		'''原材料按类型分组显示'''
		# rawstock_category_set = set(['%s-%s'%(str(i.material), str(i.rawstock_category)) for i in RawStock.objects.filter(available=True)])
		rawstock_list = RawStock.objects.filter(available=True)
		rawstock_display_dict = {}
		for stock in rawstock_list:
			key = '%s-%s'%(str(stock.material), str(stock.rawstock_category))
			if key not in rawstock_display_dict:
				rawstock_display_dict[key] = [(stock.id, stock)]
			else:
				rawstock_display_dict[key].append((stock.id,stock))
		rawstock_data = [[key,values] for key,values in rawstock_display_dict.items()]
		self.fields['raw_stock'].choices = rawstock_data
			# # 原材料类别列表
		# rawstock_category_list = RawStockCategory.objects.filter(available=True)
		# # 原材料按类别分类
		# rawstock_choice = [[_category.Category_name, [(_product.id, _product.product_code) for _product in
		#                                             LAMProduct.objects.filter(
		# 	                                            (Q(product_category=_category) & Q(available=True)))]] for
		#                   _category in rawstock_category_list]
		
		# self.fields['LAM_mission'].queryset = LAMProcessMission.objects.filter(available=True)
		self.fields['raw_stock'].queryset = RawStock.objects.filter(available=True)
		# self.fields['retrieve_time'].disabled = True
		# self.fields['raw_stock_unused_amount'].disabled = True
		# self.fields['raw_stock_primaryretrieve_amount'].disabled = True
		# self.fields['raw_stock_secondaryretrieve_amount'].disabled = True
		
		# self.fields['raw_stock_primaryretrieve'].disabled = True
		# self.fields['raw_stock_secondaryretrieve'].disabled = True
		# self.fields['available'].disabled = True

		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})
		self.fields['raw_stock'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择原材料实例..."})
		self.fields['LAM_mission'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择任务..."})
		

# 原材料追加发放台账
class RawStockSendAdditionForm(ModelForm):
	title = '原材料追加发放记录'
	modelname = 'RawStockSendAddition'
	class Meta:
		model = RawStockSendAddition
		fields = "__all__"
		
		widgets = {
			'send_time': widgets.TextInput(
				attrs={'type': 'date', 'value': str(datetime.date.today()), 'placeholder': '请选择发料日期'}),
		}
		labels = {
			'send_time': _('发料日期'),
			'RawStockSendRetrieve': _('发料实例'),
			'raw_stock': _('原材料实例'),
			'raw_stock_sent_amount': _('发放数量'),
		}
		error_messages = ''
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# '''找出所有任务中产品类型的组合'''
		# mission_product_category_typedict = {}
		# with connection.cursor() as cursor:
		# 	# cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
		# 	cursor.execute(
		# 		"SELECT lamdataserver.lamprocessdata_lamprocessmission_lam_product.lamprocessmission_id, group_concat(distinct lamdataserver.lamprocessdata_lamproduct.product_category_id) as categorylist FROM lamdataserver.lamprocessdata_lamprocessmission_lam_product inner join lamdataserver.lamprocessdata_lamproduct on lamdataserver.lamprocessdata_lamproduct.id=lamdataserver.lamprocessdata_lamprocessmission_lam_product.lamproduct_id group by  lamdataserver.lamprocessdata_lamprocessmission_lam_product.lamprocessmission_id ;")
		# 	row = cursor.fetchall()
		# 	for _record in row:
		# 		_mission_id = _record[0]
		# 		# _product_list = _record[1]
		# 		_category_list = _record[1]
		# 		if _category_list not in mission_product_category_typedict:
		# 			mission_product_category_typedict[_category_list] = [_mission_id]
		# 		else:
		# 			mission_product_category_typedict[_category_list].append(_mission_id)
		# mission_data = []
		# for _category_list_str, _mission_list in mission_product_category_typedict.items():
		# 	_category_list = _category_list_str.split(',')
		# 	mission_data.append([
		# 		','.join([str(LAMProductCategory.objects.get(id=category_id)) for category_id in _category_list]),
		# 		[
		# 			(mission_id, str(LAMProcessMission.objects.get(id=mission_id))) for mission_id in _mission_list if
		# 			LAMProcessMission.objects.get(id=mission_id).LAM_techinst_serial.selectable_RawStockSendRetrieve
		# 		]
		# 	])
		# self.fields['LAM_mission'].choices = mission_data
		# self.fields['RawStockSendRetrieve'] = forms.CharField(label='发料实例ID(悬停查看详情)')
		# self.fields['RawStockSendRetrieve']= forms.ModelChoiceField(queryset=RawStockSendRetrieve.objects.all())
		# self.fields['RawStockSendRetrieve'] = forms.ModelChoiceField(queryset=RawStockSendRetrieve.objects.filter(id=args[0]))
		# self.fields['RawStockSendRetrieve'] = forms.ModelChoiceField(queryset=RawStockSendRetrieve.objects.filter(id=kwargs['item_id']))
		# self.fields['RawStockSendRetrieve'] = forms.ModelChoiceField(queryset=RawStockSendRetrieve.objects.all())
		'''原材料按类型分组显示'''
		# rawstock_category_set = set(['%s-%s'%(str(i.material), str(i.rawstock_category)) for i in RawStock.objects.filter(available=True)])
		rawstock_list = RawStock.objects.filter(available=True)
		rawstock_display_dict = {}
		for stock in rawstock_list:
			key = '%s-%s' % (str(stock.material), str(stock.rawstock_category))
			if key not in rawstock_display_dict:
				rawstock_display_dict[key] = [(stock.id, stock)]
			else:
				rawstock_display_dict[key].append((stock.id, stock))
		rawstock_data = [[key, values] for key, values in rawstock_display_dict.items()]
		self.fields['raw_stock'].choices = rawstock_data
		# # 原材料类别列表
		# rawstock_category_list = RawStockCategory.objects.filter(available=True)
		# # 原材料按类别分类
		# rawstock_choice = [[_category.Category_name, [(_product.id, _product.product_code) for _product in
		#                                             LAMProduct.objects.filter(
		# 	                                            (Q(product_category=_category) & Q(available=True)))]] for
		#                   _category in rawstock_category_list]
		
		# self.fields['LAM_mission'].queryset = LAMProcessMission.objects.filter(available=True)
		self.fields['raw_stock'].queryset = RawStock.objects.filter(available=True)
		# self.fields['retrieve_time'].disabled = True
		# self.fields['raw_stock_unused_amount'].disabled = True
		# self.fields['raw_stock_primaryretrieve_amount'].disabled = True
		# self.fields['raw_stock_secondaryretrieve_amount'].disabled = True
		
		# self.fields['raw_stock_primaryretrieve'].disabled = True
		# self.fields['raw_stock_secondaryretrieve'].disabled = True
		# self.fields['available'].disabled = True
		# self.fields['RawStockSendRetrieve'].disabled = True
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})
		self.fields['raw_stock'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择原材料实例..."})
		# self.fields['raw_stock'].widget.attrs.update(
		# 	{'class': 'form-control chosen-select', 'data-placeholder': "选择原材料实例..."})
		# self.fields['LAM_mission'].widget.attrs.update(
		# 	{'class': 'form-control chosen-select', 'data-placeholder': "选择任务..."})

# 原材料回收台账
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
			'raw_stock_sent_amount': _('发放数量'),
			'send_addition': _('补发粉末'),
			'retrieve_time': _('回收日期'),
			'raw_stock_unused_amount': _('未用粉末数量'),
			'raw_stock_primaryretrieve':_('一级回收粉实例'),
			'raw_stock_primaryretrieve_amount': _('一级回收粉数量'),
			'raw_stock_secondaryretrieve': _('二级回收粉实例'),
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
		self.fields['send_addition'].disabled = True

		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})
		self.fields['send_addition'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "补发粉末..."})




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
		self.fields['material'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择材料..."})


# 零件分区
class LAMProductSubareaForm(ModelForm):
	title = '零件分区'
	modelname = 'LAMProductSubarea'

	class Meta:
		model = LAMProductSubarea
		fields = "__all__"
		
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['available'].disabled = True
		self.fields['product_category'].queryset = LAMProductCategory.objects.filter(available=True)
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})
		self.fields['product_category'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择产品类别..."})



# 基础工序类别
class LAMProductionWorkTypeForm(ModelForm):
	title = '基础工序类别'
	modelname = 'LAMProductionWorkType'

	class Meta:
		model = LAMProductionWorkType
		fields = "__all__"
		labels = {
			'worktype_name': _('工序名称'),
			# 'selectable_Scheduling': _('是否可被调度模块选择'),
			# 'selectable_LAM': _('是否可被激光成形模块选择'),
			# 'selectable_HeatTreatment': _('是否可被热处理模块选择'),
			# 'selectable_PhyChemNonDestructiveTest': _('是否可被检验模块选择'),
			# 'selectable_RawStockSendRetrieve': _('是否可被库房模块选择'),
			# 'selectable_Weighing': _('是否可被称重模块选择'),
			'available': _('是否激活'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['available'].disabled = True
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})

# 图片识别码
class PDFImageCodeForm(ModelForm):
	title = '文字识别记忆'
	modelname = 'PDFImageCode'
	class Meta:
		model = PDFImageCode
		fields = ['text', 'OriginalImage']
		labels = {
			'text': _('文字'),
			'OriginalImage': _('图片'),
		}
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
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
		#     'product': widgets.TextInput(
		#         attrs={'class': 'product_select'}),
		# }
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.fields['LAMProcess_serial_number'].disabled = True
		# self.fields['LAMProcess_serial_note'].disabled = True
		# product_choice =
		product_category_list = LAMProductCategory.objects.filter(available=True)
		product_choice = [[_category.product_name, [(_product.id, _product.product_code) for _product in LAMProduct.objects.filter((Q(product_category=_category)&Q(available=True)))]] for _category in product_category_list]
		self.fields['available'].disabled = True
		self.fields['product'].choices = product_choice
		# self.fields['product']=forms.MultipleChoiceField(choices=product_choice, label='产品有效范围')
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})
		self.fields['product'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder':"选择产品..."})
		self.fields['product_category'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择产品类别..."})


# 基础工序实例
class LAMTechInstSerialForm(ModelForm):
	title = '基础工序实例'
	modelname = 'LAM_TechInst_Serial'

	previewtableTitle = '工艺文件工序'
	# showPreviewTable = True
	previewtablefields = {'serial_number': _('工序号'), 'serial_worktype': _('工序名称'), 'serial_note': _('工序概述')}

	class Meta:
		model = LAM_TechInst_Serial
		fields = ['technique_instruction',
		          'serial_number',
		          'serial_worktype',
		          'serial_note',
		          'serial_content',
		          'process_parameter',
		          'selectable_Scheduling',
		          'selectable_LAM',
		          'selectable_HeatTreatment',
		          'selectable_PhyChemNonDestructiveTest',
		          'selectable_RawStockSendRetrieve',
		          'selectable_Weighing',
		          ]
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
			'selectable_Scheduling': _('是否可被调度模块选择'),
			'selectable_LAM': _('是否可被激光成形模块选择'),
			'selectable_HeatTreatment': _('是否可被热处理模块选择'),
			'selectable_PhyChemNonDestructiveTest': _('是否可被检验模块选择'),
			'selectable_RawStockSendRetrieve': _('是否可被库房模块选择'),
			'selectable_Weighing': _('是否可被称重模块选择'),
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

		# self.fields['filter_techinst'] = forms.CharField(max_length=50, required=False)
		# self.fields['filter_techinst'].widget.attrs.update(
		# 	# {'list': 'techinst_list', 'onchange': 'check_FilterTechinstField(this.value)'})
		# 	{'list': 'techinst_list', 'onchange': 'check_FilterTechinstField(getValue_from_datalist(this.id, "techinst_list"))'})
		# self.fields['filter_techinst'].label = '辅助筛选工艺文件'
		#
		# self.fields['filter_worktype'] = forms.CharField(max_length=50, required=False)
		# self.fields['filter_worktype'].widget.attrs.update(
		# 	# {'list': 'worktype_list', 'onchange': 'check_FilterWorktypeField(this.value)'})
		# 	{'list': 'worktype_list', 'onchange': 'check_FilterWorktypeField(getValue_from_datalist(this.id, "worktype_list"))'})
		# self.fields['filter_worktype'].label = '辅助筛选工序'

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
		# self.fields['technique_instruction'].widget.attrs.update({'type': 'text'})
		self.fields['process_parameter'].queryset = LAMProcessParameters.objects.filter(available=True).order_by('name')

		# self.fields['available'].disabled = True
		self.AuxiliarySelection = ('filter_techinst',
		                           'filter_worktype')
		self.OriginalFields = (
			'technique_instruction',
			'serial_number',
			'serial_worktype',
			'serial_note',
			'serial_content',
			'process_parameter',
			'selectable_Scheduling',
			'selectable_LAM',
			'selectable_HeatTreatment',
			'selectable_PhyChemNonDestructiveTest',
			'selectable_RawStockSendRetrieve',
			'selectable_Weighing',
		)
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})
		self.fields['technique_instruction'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择技术文件..."})
		self.fields['serial_worktype'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择工序..."})
		self.fields['process_parameter'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择工艺参数包..."})

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
		fields = [
			'technique_instruction',
		    'serial_number',
		    'serial_worktype',
		    'serial_note',
		    'serial_content',
		    'process_parameter',
			'selectable_Scheduling',
			'selectable_LAM',
			'selectable_HeatTreatment',
			'selectable_PhyChemNonDestructiveTest',
			'selectable_RawStockSendRetrieve',
			'selectable_Weighing'
		]

		# fields = "__all__"
		labels = {
			'technique_instruction': _('工艺文件'),
			'serial_number': _('工序号'),
			'serial_worktype': _('工序名称'),
			'serial_note': _('工序概述'),
			'serial_content': _('工序内容'),
			'process_parameter':_('激光成形参数包'),
			'selectable_Scheduling': _('是否可被调度模块选择'),
			'selectable_LAM': _('是否可被激光成形模块选择'),
			'selectable_HeatTreatment': _('是否可被热处理模块选择'),
			'selectable_PhyChemNonDestructiveTest': _('是否可被检验模块选择'),
			'selectable_RawStockSendRetrieve': _('是否可被库房模块选择'),
			'selectable_Weighing': _('是否可被称重模块选择'),
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
		self.fields['technique_instruction'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择技术文件..."})
		self.fields['serial_worktype'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择工序..."})
		self.fields['process_parameter'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择工艺参数包..."})


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
			'selectable_Scheduling': _('调度可选'),
			'selectable_LAM': _('成形可择'),
			'selectable_HeatTreatment': _('热处理可选'),
			'selectable_PhyChemNonDestructiveTest': _('检验可选'),
			'selectable_RawStockSendRetrieve': _('库房可选'),
			'selectable_Weighing': _('称重可选'),
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

	previewtable3_Title = '累加单元'
	previewtable3_fields = {'active':_('是否激活'),
							'M1': _('能量系数M1'),
	                        'M2': _('停光冷却系数M2'),
	                        'l': _('停光冷却-聚集系数l'),
	                        'tm': _('停光权重半衰期tm'),
	                        'alarm_value':_('报警值'),
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

class LAMProcessAccumulateCell_Edit(ModelForm):
	title = '激光成形参数累加单元实例'
	modelname = 'LAMProcessParameterAccumulateCell'
	class Meta:
		model = LAMProcessParameterAccumulateCell
		fields = ['active', 'M1', 'M2', 'l','tm','alarm_value']
		# fields = "__all__"
		# widgets = {
		# 	'level': widgets.TextInput(
		# 		attrs={'type': 'number', 'placeholder': '级别数值越小，表明条件越基础；级别数值越大，表明条件越特殊；'}),
		# 	'precondition': widgets.Textarea(
		# 		attrs={'type': 'text', 'placeholder': '本条件单元触发的先决条件'}),
		# 	'expression': widgets.Textarea(
		# 		attrs={'type': 'text', 'placeholder': '触发本条件单元后的工艺范围描述'}),
		# }
		labels = {
			'active':_('是否启动累加单元'),
			'M1': _('能量系数M1'),
			'M2': _('停光冷却系数M2'),
			'l': _('停光冷却-聚集系数l'),
			'tm': _('停光冷却-权重半衰期tm'),
			'alarm_value': _('报警值'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		if 'ProcessParameterID' in kwargs:
			# 新建
			super().__init__(*args, {})
		else:
			# 编辑
			super().__init__(*args, **kwargs)

		if 'ProcessParameterID' in kwargs:
			_parameter = LAMProcessParameters.objects.get(id=kwargs['ProcessParameterID'])
		else:
			# pass AccuCell_Parameter
			_parameter=kwargs['instance'].AccuCell_Parameter.all()[0]
		# qset = (
		# 		Q(id__gte=Current_i * num_per_page) &
		# 		Q(id__lt=(Current_i + 1) * num_per_page) &
		# 		Q(acquisition_timestamp__isnull=True)
		# )
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})

	def is_valid_custom(self):
		try:
			if 'active' in self.data and self.data['active'] and \
				not (self.data['M1'] and \
				 self.data['M2'] and \
				 self.data['l'] and \
				 self.data['tm'] and \
				 self.data['alarm_value']):
				self.error_messages = '累加功能激活时各参数不能为空。'
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


# 机械加工状态
class MachiningStateForm(ModelForm):
	title = '机械加工状态'
	modelname = 'HeatTreatmentState'

	class Meta:
		model = MachiningState
		fields = "__all__"
		labels = {
			'machiningstate_name': _('机械加工状态'),
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
		self.fields['product_category'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择产品类别..."})


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
	# previewtablefields = {'LAM_product': _('零件实例'),'LAM_techinst_serial': _('下达任务工序'), 'arrangement_date': _('下达任务日期'),
	#                       'completion_date': _('完成任务日期')}

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
		# 产品类别列表
		product_category_list = LAMProductCategory.objects.filter(available=True)
		# 产品按类别分类
		product_choice = [[_category.product_name, [(_product.id, _product.product_code) for _product in
		                                            LAMProduct.objects.filter(
			                                            (Q(product_category=_category) & Q(available=True)))]] for
		                  _category in product_category_list]
		# 已有工艺文件
		techinst_list = LAMTechniqueInstruction.objects.filter(Q(available=True) & Q(filed=False)).order_by('instruction_code', '-version_code', '-version_number')
		# 工序按工艺文件分类
		techinst_serial_choice = [[str(_techinst), [(_serial.id, "%d-%s %s"%(_serial.serial_number, _serial.serial_worktype, _serial.serial_note)) for _serial in
		                                            LAM_TechInst_Serial.objects.filter(
			                                            (Q(technique_instruction=_techinst) & Q(available=True)))]] for _techinst in techinst_list]
		
		# 辅助选择数据集
		# self.techinst_datalist = LAMTechniqueInstruction.objects.filter(Q(available=True) & Q(filed=False)).order_by(
		# 	'instruction_code', '-version_code', '-version_number')
		# # print(self.techinst_datalist)
		# self.worktype_datalist = LAMProductionWorkType.objects.filter(available=True)
		# self.productcode_datalist = LAMProduct.objects.filter(available=True)

		# self.fields['LAM_product'].queryset = LAMProduct.objects.filter(available=True)

		# NotFiledTechInst = LAMTechniqueInstruction.objects.filter(Q(filed=False) & Q(available=True))
		# self.fields['LAM_techinst_serial'].queryset = LAM_TechInst_Serial.objects.filter(
		# 	Q(available=True) & Q(technique_instruction__filed=False))
		self.fields['work_section'].queryset = Worksection.objects.filter(available=True)
		# self.fields['completion_date'].disabled = True
		# self.fields['available'].disabled = True

		# 辅助选择下拉菜单及文本框
		# self.fields['product_category'] = forms.ModelChoiceField(label='产品类别',
		#                                                          queryset=LAMProductCategory.objects.filter(
		#                                                              available=True),
		#                                                          empty_label='请选择产品类别',
		#                                                          required=False)
		# self.fields['product_code'] = forms.CharField(label='零件编号',
		#                                               max_length=50,
		#                                               required=False)
		# self.fields['technique_instruction'] = forms.ModelChoiceField(label='工艺文件',
		#                                                               queryset=self.techinst_datalist,
		#                                                               empty_label='请选择工艺文件',
		#                                                               required=False)
		# self.fields['work_type'] = forms.ModelChoiceField(label='工序',
		#                                                   queryset=self.worktype_datalist,
		#                                                   empty_label='请选择工序',
		#                                                   required=False)

		# 更新属性
		# 产品类别
		# self.fields['product_category'].widget.attrs.update(
		#     {'onchange': 'load_LAMTechInstandProduct_By_ProductCategory(this.value);'})
		# 工艺文件
		# self.fields['technique_instruction'].widget.attrs.update(
		# 	{'onchange': 'load_WorkType_By_LAMTechInst(this.value);'})
		# # 工序
		# self.fields['work_type'].widget.attrs.update(
		# 	{'onchange': 'refresh_techinst_serial();'})
		#
		# self.fields['product_code'].widget.attrs.update(
		# 	{'list': 'product_code_list', 'onblur': 'refresh_product();'})

		# 辅助选择field
		# self.AuxiliarySelection = ('product_category',
		#                            'technique_instruction',
		#                            'work_type',
		#                            'product_code')
		# 原始field
		self.OriginalFields = ('LAM_product', 'LAM_techinst_serial', 'work_section', 'arrangement_date')

		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})
		
		self.fields['LAM_product'].choices = product_choice
		self.fields['LAM_product'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择产品..."})
		# self.fields['LAM_product'].widget.attrs.update(
		# 	{'class': 'form-control chosen-select', 'data-placeholder': "选择产品...",
		# 	 'onchange': 'loadTableData_ProductMission(this.value)'})
		self.fields['LAM_techinst_serial'].choices = techinst_serial_choice
		self.fields['LAM_techinst_serial'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择工序..."})
		self.fields['work_section'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择激光成形工段..."})

		
	def is_valid_custom(self):

		# try:
		# 	_Product = LAMProduct.objects.get(id=self.data['LAM_product'])
		# 	_ProdCate = _Product.product_category
		# 	_TechInst = LAM_TechInst_Serial.objects.get(id=self.data['LAM_techinst_serial']).technique_instruction
		#
		# 	if not (_Product in _TechInst.product.all() or _ProdCate in _TechInst.product_category.all()):
		# 		self.error_messages = '该产品与选中工艺文件未关联'
		# 		return False
		# # LAMTechniqueInstruction.objects.filter(Q(product_category=_ProdCate) | Q(product=_Product))
		#
		# # all_datadict = LAMTechniqueInstruction.objects.filter(
		# #     Q(product_category=filtecondition_ProdCate) | Q(product=filtecondition_Product)).order_by(
		# #     'instruction_code')
		# #
		# #
		# # # _ProdCate_id = LAMProduct.objects.get(id=self.data['LAM_product']).product_category
		# # _TechInst_id = LAM_TechInst_Serial.objects.get(id=self.data['LAM_techinst_serial']).technique_instruction.id
		# #
		# # _filter_list = LAMProdCate_TechInst.objects.filter(lamproductcategory = _ProdCate_id,
		# #                                     lamtechniqueinstruction = _TechInst_id)
		# # if len(_filter_list)==0:
		# #     self.error_messages = '该产品与选中工艺文件未关联'
		# #     return False
		# except:
		# 	self.error_messages = '未知错误'
		# 	return False

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

		# 找出所有任务中产品类型的组合
		mission_product_category_typedict = {}
		with connection.cursor() as cursor:
			# cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
			cursor.execute(
				"SELECT lamdataserver.lamprocessdata_lamprocessmission_lam_product.lamprocessmission_id, group_concat(distinct lamdataserver.lamprocessdata_lamproduct.product_category_id) as categorylist FROM lamdataserver.lamprocessdata_lamprocessmission_lam_product inner join lamdataserver.lamprocessdata_lamproduct on lamdataserver.lamprocessdata_lamproduct.id=lamdataserver.lamprocessdata_lamprocessmission_lam_product.lamproduct_id group by  lamdataserver.lamprocessdata_lamprocessmission_lam_product.lamprocessmission_id ;")
			row = cursor.fetchall()
			for _record in row:
				_mission_id = _record[0]
				# _product_list = _record[1]
				_category_list = _record[1]
				if _category_list not in mission_product_category_typedict:
					mission_product_category_typedict[_category_list] = [_mission_id]
				else:
					mission_product_category_typedict[_category_list].append(_mission_id)
		mission_data = []
		for _category_list_str, _mission_list in mission_product_category_typedict.items():
			_category_list = _category_list_str.split(',')
			mission_data.append([
				','.join([ str(LAMProductCategory.objects.get(id = category_id)) for category_id in _category_list]),
				[
					(mission_id,str(LAMProcessMission.objects.get(id = mission_id))) for mission_id in _mission_list
				]
			])
		
		self.fields['process_mission'].choices = mission_data
		# print(mission_data)
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
		# self.productcode_datalist = LAMProduct.objects.filter(available=True)

		# self.fields['product_category'] = forms.ModelChoiceField(label='产品类别',
		#                                                          queryset=LAMProductCategory.objects.filter(
		# 	                                                         available=True),
		#                                                          empty_label='请选择产品类别',
		#                                                          required=False)
		self.fields['worksection'] = forms.ModelChoiceField(label='激光成形工段',
		                                                    queryset=Worksection.objects.filter(available=True),
		                                                    empty_label='请选择激光成形工段',
		                                                    required=False)
		# self.fields['product_code'] = forms.CharField(label='零件编号',
		#                                               max_length=50,
		#                                               required=False)

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
		# self.fields['product_category'].name = 'product_category'
		self.fields['worksection'].name = 'worksection'
		# self.fields['product_code'].name = 'product_code'
		self.fields['temp_process_start_date'].name = 'temp_process_start_date'
		self.fields['temp_process_finish_date'].name = 'temp_process_finish_date'
		# 辅助选择field
		self.AuxiliarySelection = ('temp_process_start_date',
		                           'temp_process_finish_date',
		                           # 'product_category',
		                           'worksection',
		                           # 'product_code'
		                           )
		self.AuxiliarySelection_with_row = (
			('temp_process_start_date', 'temp_process_finish_date'), ('product_category', 'worksection'),
			('product_code'))

		# 原始field
		self.OriginalFields = ('process_mission',
		                       'process_start_time',
		                       'process_finish_time',
		                       # 'laserdata_start_id',
		                       # 'laserdata_finish_id',
		                       # 'oxygendata_start_id',
		                       # 'oxygendata_finish_id',
		                       # 'cncstatusdata_start_id',
		                       # 'cncstatusdata_finish_id'
		                       )

		# self.fields['process_start_time'].disabled = True
		# self.fields['process_finish_time'].disabled = True

		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})

		# self.fields['product_code'].widget.attrs.update(
		# 	{'list': 'product_code_list', 'onblur': 'refresh_missionlist();'})
		# self.fields['product_category'].widget.attrs.update(
		# 	{'onblur': 'refresh_productlist();'})
		self.fields['process_mission'].widget.attrs.update(
			{'class': 'form-control chosen-select','data-placeholder': "选择激光成形任务...",'onchange': 'refresh_worksection_selection(this.value);refresh_start_finsh_datetime(this.value);'})

		# self.fields['laserdata_start_id'].widget.attrs.update({'type': 'hidden'})
		# self.fields['laserdata_finish_id'].widget.attrs.update({'type': 'hidden'})
		# self.fields['oxygendata_start_id'].widget.attrs.update({'type': 'hidden'})
		# self.fields['oxygendata_finish_id'].widget.attrs.update({'type': 'hidden'})
		# self.fields['cncstatusdata_start_id'].widget.attrs.update({'type': 'hidden'})
		# self.fields['cncstatusdata_start_id'].widget.attrs.update({'type': 'hidden'})

		# self.AuxiliarySelectionField_with_row = (
		# 	(self.fields['product_category'], self.fields['product_code']),
		# )
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

			try:
				self.fields['process_start_time'].widget.attrs.update({'value': _mission_attr_obj.process_start_time.strftime("%Y-%m-%dT%H:%M:%S")})
				self.fields['process_finish_time'].widget.attrs.update({'value': _mission_attr_obj.process_finish_time.strftime("%Y-%m-%dT%H:%M:%S")})
			except:
				pass
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
		# self.fields['datalist_techinst'] = forms.CharField()
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})
		self.fields['sampling_position'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择取样部位..."})
		self.fields['sampling_direction'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择取样方向..."})


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
		self.fields['sampling_position'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择取样部位..."})
		self.fields['sampling_direction'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择取样方向..."})

# 断裂韧性测试数据
class MechanicalTest_FracturetoughnessForm(ModelForm):
	title = '断裂韧性性能测试'
	modelname = 'MechanicalTest_FractureToughness'

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
		model = MechanicalTest_FractureToughness
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
			'fracturetoughness_KIC': _('KIC / MPa×m<sup>1/2</sup>'),
			'fracturetoughness_KQ': _('KQ / MPa×m<sup>1/2</sup>'),
			'Effectiveness': _('有效性判定'),
			'toughness': _('冲击韧性 / J/cm<sup>2</sup>'),
			'available': _('是否有效'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})
		self.fields['sampling_position'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择取样部位..."})
		self.fields['sampling_direction'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择取样方向..."})


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
		self.fields['sampling_position'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择取样部位..."})

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
	# title = '产品理化检测'
	# modelname = 'PhysicochemicalTest_Mission'
	#
	# class Meta:
	# 	model = PhysicochemicalTest_Mission
	# 	fields = ['LAM_product',
	# 	          'LAM_techinst_serial',
	# 	          'commission_date',
	# 	          'heat_treatment_state',
	# 	          ]
	# 	widgets = {
	# 		'commission_date': widgets.TextInput(
	# 			attrs={'type': 'date', 'value': str(datetime.date.today()), 'placeholder': '请选择开始日期'}),
	# 	}
	# 	labels = {
	# 		'LAM_product': _('产品实例'),
	# 		'RawStock': _('原材料实例'),
	# 		'LAM_techinst_serial': _('工序'),
	# 		'commission_date': _('开始日期'),
	# 		'heat_treatment_state': _('热处理状态'),
	# 		'mechanicaltest_tensile': _('拉伸测试'),
	# 		'mechanicaltest_toughness': _('冲击测试'),
	# 		'chemicaltest': _('化学成分测试'),
	# 	}
	# 	error_messages = ''
	#
	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)
	# 	# self.fields['LAM_product'].disabled = True
	# 	# self.fields['LAM_techinst_serial'].disabled = True
	# 	# self.fields['commission_date'].disabled = True
	# 	# self.fields['heat_treatment_state'].disabled = True
	#
	# 	for field in self.fields.values():
	# 		field.widget.attrs.update({'class': 'form-control'})
# # 激光成形生产任务_编辑
# class LAMProcessMissionForm_Edit(ModelForm):
	title = '产品理化检测'
	modelname = 'PhysicochemicalTest_Mission'
	previewtableTitle = '产品检测任务'
	previewtablefields = {'LAM_techinst_serial': _('下达任务工序'), 'arrangement_date': _('下达任务日期')}

	class Meta:
		model = PhysicochemicalTest_Mission
		fields = ['LAM_product',
		          'LAM_techinst_serial',
		          'commission_date',
		          'heat_treatment_state',
		          ]
		# fields = "__all__"
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
			'mechanicaltest_fracturetoughness': _('断裂韧性测试'),
			'chemicaltest': _('化学成分测试'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# 产品类别列表
		product_category_list = LAMProductCategory.objects.filter(available=True)
		# 产品按类别分类
		product_choice = [[_category.product_name, [(_product.id, _product.product_code) for _product in
		                                            LAMProduct.objects.filter(
			                                            (Q(product_category=_category) & Q(available=True)))]] for
		                  _category in product_category_list]
		self.fields['LAM_product'].choices = product_choice
		
		self.fields['LAM_product'].widget.attrs.update(
			{'onchange': 'loadTableData_ProductMission(this.value)'})

		# 辅助选择数据集
		# self.techinst_datalist = LAMTechniqueInstruction.objects.filter(Q(available=True) & Q(filed=False)).order_by(
		# 	'instruction_code', '-version_code', '-version_number')
		# # print(self.techinst_datalist)
		# self.worktype_datalist = LAMProductionWorkType.objects.filter(Q(available=True))
		# self.productcode_datalist = LAMProduct.objects.filter(available=True)

		self.fields['LAM_product'].queryset = LAMProduct.objects.filter(available=True)

		# NotFiledTechInst = LAMTechniqueInstruction.objects.filter(Q(filed=False) & Q(available=True))
		self.fields['LAM_techinst_serial'].queryset = LAM_TechInst_Serial.objects.filter(
			Q(available=True) & Q(technique_instruction__filed=False) & Q(selectable_PhyChemNonDestructiveTest=True))
		# self.fields['work_section'].queryset = Worksection.objects.filter(available=True)
		# self.fields['completion_date'].disabled = True
		# self.fields['available'].disabled = True

		# 辅助选择下拉菜单及文本框
		# self.fields['product_category'] = forms.ModelChoiceField(label='产品类别',
		#                                                          queryset=LAMProductCategory.objects.filter(
		#                                                              available=True),
		#                                                          empty_label='请选择产品类别',
		#                                                          required=False)
		# self.fields['product_code'] = forms.CharField(label='零件编号',
		#                                               max_length=50,
		#                                               required=False)
		# self.fields['technique_instruction'] = forms.ModelChoiceField(label='工艺文件',
		#                                                               queryset=self.techinst_datalist,
		#                                                               empty_label='请选择工艺文件',
		#                                                               required=False)
		# self.fields['work_type'] = forms.ModelChoiceField(label='工序',
		#                                                   queryset=self.worktype_datalist,
		#                                                   empty_label='请选择工序',
		#                                                   required=False)

		# 更新属性
		# 产品类别
		# self.fields['product_category'].widget.attrs.update(
		#     {'onchange': 'load_LAMTechInstandProduct_By_ProductCategory(this.value);'})
		# 工艺文件
		# self.fields['technique_instruction'].widget.attrs.update(
		# 	{'onchange': 'load_WorkType_By_LAMTechInst(this.value);'})
		# 工序
		# self.fields['work_type'].widget.attrs.update(
		# 	{'onchange': 'refresh_techinst_serial();'})

		# self.fields['product_code'].widget.attrs.update(
		# 	{'list': 'product_code_list', 'onblur': 'refresh_product();'})

		# 辅助选择field
		# self.AuxiliarySelection = ('product_category',
		#                            'technique_instruction',
		#                            'work_type',
		#                            'product_code')
		# 原始field
		self.OriginalFields = ('LAM_product',
		                       'LAM_techinst_serial',
		                       'commission_date',
		                       'heat_treatment_state',
		                       )

		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})
		'''检验工序'''
		self.fields['LAM_techinst_serial'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择检验工序..."})
		'''产品'''
		self.fields['LAM_product'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择产品..."})
		'''热处理状态'''
		self.fields['heat_treatment_state'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择热处理状态..."})

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
	fracturetoughness_fields = [
		'试样编号',
		'取样部位',
		'取样方向',
		'测试温度/℃',
		'K<sub>IC</sub> / MPa×m<sup>1/2</sup>',
		'K<sub>Q</sub> / MPa×m<sup>1/2</sup>',
		'有效性判定',
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
			'mechanicaltest_fracturetoughness': _('断裂韧性测试'),
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
		self.fields['LAM_product'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择产品实例..."})
		# self.fields['RawStock'].widget.attrs.update(
		# 	{'class': 'form-control chosen-select', 'data-placeholder': "选择原材料实例..."})


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
		          'mechanicaltest_fracturetoughness',
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
			'mechanicaltest_fracturetoughness':_('断裂韧性测试'),
			'chemicaltest': _('化学成分测试'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.fields['available'].disabled = True

		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})



# 超声缺陷
class NonDestructiveTest_UTDefectForm(ModelForm):
	title = '超声波检测'
	modelname = 'UTDefectInformation'
	
	# 是否需要上传照片
	IfUploadPhotos = True

	class Meta:
		model = UTDefectInformation
		fields = [
			# 缺陷编号
			'defect_number',
			# 缺陷类型
			'defect_type',
			# 当量
			'equivalent_hole_diameter',
			# 辐射当量  增益调节的单位
			'radiation_equivalent',
			# 所在分区
			'product_subarea',
			# 半精加工状态统一坐标位置 - x
			'X_coordinate',
			# 半精加工状态统一坐标位置 - y
			'Y_coordinate',
			# 半精加工状态统一坐标位置 - z
			'Z_coordinate',
			# 'photos',
		]
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.fields['datalist_techinst'] = forms.CharField()
		# product_category
		
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})
		self.fields['defect_type'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择缺陷类别..."})
		self.fields['product_subarea'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择所在分区..."})
	def set_Subarea_QuerySet(self, DefectInformationObj=None, MissionObj = None):
		if MissionObj is None:
			NonDestructiveTest_Mission_Obj = DefectInformationObj.UTDefect_NDTMission.all()[0]
			if NonDestructiveTest_Mission_Obj.LAM_product is not None:
				_category = NonDestructiveTest_Mission_Obj.LAM_product.product_category
			else:
				_category = None
		else:
			if MissionObj.LAM_product is not None:
				_category = MissionObj.LAM_product.product_category
			else:
				_category = None
		qset = (
				Q(product_category=_category) &
				Q(available=True)
		)
		self.fields['product_subarea'].queryset = LAMProductSubarea.objects.filter(qset)


# X射线缺陷
class NonDestructiveTest_RTDefectForm(ModelForm):
	title = 'X射线检测'
	modelname = 'RTDefectInformation'
	
	# 是否需要上传照片
	IfUploadPhotos = True
	
	class Meta:
		model = RTDefectInformation
		fields = [
			# 缺陷编号
			'defect_number',
			# 缺陷类型
			'defect_type',
			# 缺陷大小
			'size',
			# 所在分区
			'product_subarea',
			# 半精加工状态统一坐标位置 - x
			'X_coordinate',
			# 半精加工状态统一坐标位置 - y
			'Y_coordinate',
			# 半精加工状态统一坐标位置 - z
			'Z_coordinate',
			# 'photos',
		]
		error_messages = ''
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.fields['datalist_techinst'] = forms.CharField()
		# product_category
		
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})
		self.fields['defect_type'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择缺陷类别..."})
		self.fields['product_subarea'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择所在分区..."})
	
	def set_Subarea_QuerySet(self, DefectInformationObj=None, MissionObj = None):
		if MissionObj is None:
			NonDestructiveTest_Mission_Obj = DefectInformationObj.RTDefect_NDTMission.all()[0]
			if NonDestructiveTest_Mission_Obj.LAM_product is not None:
				_category = NonDestructiveTest_Mission_Obj.LAM_product.product_category
			else:
				_category = None
		else:
			if MissionObj.LAM_product is not None:
				_category = MissionObj.LAM_product.product_category
			else:
				_category = None
		qset = (
				Q(product_category=_category) &
				Q(available=True)
		)
		self.fields['product_subarea'].queryset = LAMProductSubarea.objects.filter(qset)
	


# 渗透缺陷
class NonDestructiveTest_PTDefectForm(ModelForm):
	title = '荧光检测'
	modelname = 'PTDefectInformation'
	
	# 是否需要上传照片
	IfUploadPhotos = True
	
	class Meta:
		model = PTDefectInformation
		fields = [
			# 缺陷编号
			'defect_number',
			# 缺陷类型
			'defect_type',
			# 所在分区
			'product_subarea',
			# 半精加工状态统一坐标位置 - x
			'X_coordinate',
			# 半精加工状态统一坐标位置 - y
			'Y_coordinate',
			# 半精加工状态统一坐标位置 - z
			'Z_coordinate',
			# 'photos',
		]
		error_messages = ''
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.fields['datalist_techinst'] = forms.CharField()
		# product_category
		
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})
		self.fields['defect_type'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择缺陷类别..."})
		self.fields['product_subarea'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择所在分区..."})
	
	def set_Subarea_QuerySet(self, DefectInformationObj=None, MissionObj = None):
		if MissionObj is None:
			NonDestructiveTest_Mission_Obj = DefectInformationObj.PTDefect_NDTMission.all()[0]
			if NonDestructiveTest_Mission_Obj.LAM_product is not None:
				_category = NonDestructiveTest_Mission_Obj.LAM_product.product_category
			else:
				_category = None
		else:
			if MissionObj.LAM_product is not None:
				_category = MissionObj.LAM_product.product_category
			else:
				_category = None
		qset = (
				Q(product_category=_category) &
				Q(available=True)
		)
		self.fields['product_subarea'].queryset = LAMProductSubarea.objects.filter(qset)


# 磁粉检测缺陷
class NonDestructiveTest_MTDefectForm(ModelForm):
	title = '磁粉检测'
	modelname = 'MTDefectInformation'
	
	# 是否需要上传照片
	IfUploadPhotos = True
	
	class Meta:
		model = MTDefectInformation
		fields = [
			# 缺陷编号
			'defect_number',
			# 缺陷类型
			'defect_type',
			# 所在分区
			'product_subarea',
			# 半精加工状态统一坐标位置 - x
			'X_coordinate',
			# 半精加工状态统一坐标位置 - y
			'Y_coordinate',
			# 半精加工状态统一坐标位置 - z
			'Z_coordinate',
			# 'photos',
		]
		error_messages = ''
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.fields['datalist_techinst'] = forms.CharField()
		# product_category
		
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})
		self.fields['defect_type'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择缺陷类别..."})
		self.fields['product_subarea'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择所在分区..."})
	
	def set_Subarea_QuerySet(self, DefectInformationObj=None, MissionObj = None):
		if MissionObj is None:
			NonDestructiveTest_Mission_Obj = DefectInformationObj.MTDefect_NDTMission.all()[0]
			if NonDestructiveTest_Mission_Obj.LAM_product is not None:
				_category = NonDestructiveTest_Mission_Obj.LAM_product.product_category
			else:
				_category = None
		else:
			if MissionObj.LAM_product is not None:
				_category = MissionObj.LAM_product.product_category
			else:
				_category = None
		qset = (
				Q(product_category=_category) &
				Q(available=True)
		)
		self.fields['product_subarea'].queryset = LAMProductSubarea.objects.filter(qset)


# 产品无损检测 新建
class ProductNonDestructiveTestForm_New(ModelForm):

	title = '产品无损检测'
	modelname = 'NonDestructiveTest_Mission'
	previewtableTitle = '产品检测任务'
	previewtablefields = {'LAM_techinst_serial': _('下达任务工序'),
	                      'arrangement_date': _('下达任务日期'),
	                      'machining_state':_('机械加工状态'),
	                      'heat_treatment_state':_('热处理状态'),
	                      }
	
	class Meta:
		model = NonDestructiveTest_Mission
		fields = ['LAM_product',
		          'LAM_techinst_serial',
		          'arrangement_date',
		          'machining_state',
		          'heat_treatment_state',
		          # 'NDT_type',
		          ]
		# fields = "__all__"
		widgets = {
			'arrangement_date': widgets.TextInput(
				attrs={'type': 'date', 'value': str(datetime.date.today()), 'placeholder': '请选择开始日期'}),
		}
		# labels = {
		# 	'LAM_product': _('产品实例'),
		# 	'RawStock': _('原材料实例'),
		# 	'LAM_techinst_serial': _('工序'),
		# 	'commission_date': _('开始日期'),
		# 	'heat_treatment_state': _('热处理状态'),
		# 	'mechanicaltest_tensile': _('拉伸测试'),
		# 	'mechanicaltest_toughness': _('冲击测试'),
		# 	'mechanicaltest_fracturetoughness': _('断裂韧性测试'),
		# 	'chemicaltest': _('化学成分测试'),
		# }
		error_messages = ''
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# 产品类别列表
		product_category_list = LAMProductCategory.objects.filter(available=True)
		# 产品按类别分类
		product_choice = [[_category.product_name, [(_product.id, _product.product_code) for _product in
		                                            LAMProduct.objects.filter(
			                                            (Q(product_category=_category) & Q(available=True)))]] for
		                  _category in product_category_list]
		self.fields['LAM_product'].choices = product_choice
		
		self.fields['LAM_product'].widget.attrs.update(
			{'onchange': 'loadTableData_ProductMission(this.value)'})
	
		
		self.fields['LAM_product'].queryset = LAMProduct.objects.filter(available=True)
		
		# NotFiledTechInst = LAMTechniqueInstruction.objects.filter(Q(filed=False) & Q(available=True))
		self.fields['LAM_techinst_serial'].queryset = LAM_TechInst_Serial.objects.filter(
			Q(available=True) & Q(technique_instruction__filed=False) & Q(selectable_PhyChemNonDestructiveTest=True))
		
		# 原始field
		self.OriginalFields = ('LAM_product',
							'LAM_techinst_serial',
							'arrangement_date',
							'machining_state',
							'heat_treatment_state',
		)
		
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})
		'''检验工序'''
		self.fields['LAM_techinst_serial'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择检验工序..."})
		'''产品'''
		self.fields['LAM_product'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择产品..."})
		'''热处理状态'''
		self.fields['heat_treatment_state'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择热处理状态..."})
		'''加工状态'''
		self.fields['machining_state'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择加工状态..."})
		'''检测类别'''
		# self.fields['NDT_type'].widget.attrs.update(
		# 	{'class': 'form-control chosen-select', 'data-placeholder': "选择检测类别..."})
	
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


# 产品无损检测 编辑
class ProductNonDestructiveTestForm_Edit(ModelForm):
	title = '产品无损检测'
	modelname = 'NonDestructiveTest_Mission'
	# previewtablefields = {'LAM_techinst_serial': _('下达任务工序'), 'arrangement_date': _('下达任务日期'),
	#                       'completion_date': _('完成任务日期')}
	UTDefect_fields = [
		'缺陷编号',
		'缺陷类别',
		'当量平底孔直径(mm)',
		'辐射当量(db)',
		'缺陷所在分区',
		'加工数模内坐标X',
		'加工数模内坐标Y',
		'加工数模内坐标Z',
		# '照片',
	]
	RTDefect_fields = [
		'缺陷编号',
		'缺陷类别',
		'缺陷大小(mm)',
		'缺陷所在分区',
		'加工数模内坐标X',
		'加工数模内坐标Y',
		'加工数模内坐标Z',
		# '照片',
	]
	PTDefect_fields = [
		'缺陷编号',
		'缺陷类别',
		'缺陷所在分区',
		'加工数模内坐标X',
		'加工数模内坐标Y',
		'加工数模内坐标Z',
		# '照片',
	]
	MTDefect_fields = [
		'缺陷编号',
		'缺陷类别',
		# '缺陷大小(mm)',
		'缺陷所在分区',
		'加工数模内坐标X',
		'加工数模内坐标Y',
		'加工数模内坐标Z',
		# '照片',
	]
	
	class Meta:
		model = NonDestructiveTest_Mission
		fields = ['LAM_product',
		          'LAM_techinst_serial',
		          'arrangement_date',
		          'machining_state',
		          'heat_treatment_state',
		          # 'NDT_type',
		          ]
		# fields = "__all__"
		widgets = {
			'arrangement_date': widgets.TextInput(
				attrs={'type': 'date', 'value': str(datetime.date.today()), 'placeholder': '请选择开始日期'}),
		}
		
		error_messages = ''
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['LAM_product'].disabled = True
		self.fields['LAM_techinst_serial'].disabled = True
		# self.fields['commission_date'].disabled = True
		self.fields['machining_state'].disabled = True
		self.fields['heat_treatment_state'].disabled = True
		
		# 产品类别列表
		product_category_list = LAMProductCategory.objects.filter(available=True)
		# 产品按类别分类
		product_choice = [[_category.product_name, [(_product.id, _product.product_code) for _product in
		                                            LAMProduct.objects.filter(
			                                            (Q(product_category=_category) & Q(available=True)))]] for
		                  _category in product_category_list]
		self.fields['LAM_product'].choices = product_choice
		
		self.fields['LAM_product'].widget.attrs.update(
			{'onchange': 'loadTableData_ProductMission(this.value)'})
		
		self.fields['LAM_product'].queryset = LAMProduct.objects.filter(available=True)
		
		# NotFiledTechInst = LAMTechniqueInstruction.objects.filter(Q(filed=False) & Q(available=True))
		self.fields['LAM_techinst_serial'].queryset = LAM_TechInst_Serial.objects.filter(
			Q(available=True) & Q(technique_instruction__filed=False) & Q(selectable_PhyChemNonDestructiveTest=True))
		
		# 原始field
		self.OriginalFields = ('LAM_product',
		                       'LAM_techinst_serial',
		                       'arrangement_date',
		                       'machining_state',
		                       'heat_treatment_state',
		                       )
		
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})
		'''检验工序'''
		self.fields['LAM_techinst_serial'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择检验工序..."})
		'''产品'''
		self.fields['LAM_product'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择产品..."})
		'''热处理状态'''
		self.fields['heat_treatment_state'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择热处理状态..."})
		'''加工状态'''
		self.fields['machining_state'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择加工状态..."})



# 产品无损检测
class ProductNonDestructiveTestForm_Browse(ModelForm):
	title = '产品无损检测'
	modelname = 'NonDestructiveTest_Mission'

	class Meta:
		model = NonDestructiveTest_Mission
		fields = ['LAM_product',
					'LAM_techinst_serial',
					'machining_state',
					'heat_treatment_state',
					'arrangement_date',
					'completion_date',
					# 'NDT_type',
					'UT_defect',
					'RT_defect',
					'PT_defect',
					'MT_defect',
					'rewelding_number',
					'quality_reviewsheet',
		]
		widgets = {
			'arrangement_date': widgets.TextInput(
				attrs={'type': 'date', 'value': str(datetime.date.today()), 'placeholder': '请选择开始日期'}),
			'completion_date': widgets.TextInput(
				attrs={'type': 'date', 'value': str(datetime.date.today()), 'placeholder': '请选择完成日期'}),
		}
		
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.fields['available'].disabled = True

		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})
		self.fields['LAM_techinst_serial'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择检验工序..."})
		self.fields['machining_state'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择加工状态..."})
		self.fields['heat_treatment_state'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择热处理状态..."})


# 产品无损检测
class RawStockNonDestructiveTestForm_Browse(ModelForm):
	title = '原材料无损检测'
	modelname = 'NonDestructiveTest_Mission'
	
	class Meta:
		model = NonDestructiveTest_Mission
		fields = ['RawStock',
		          'LAM_techinst_serial',
		          'machining_state',
		          'heat_treatment_state',
		          'arrangement_date',
		          'completion_date',
		          # 'NDT_type',
		          'UT_defect',
		          'RT_defect',
		          'PT_defect',
		          'MT_defect',
		          'rewelding_number',
		          'quality_reviewsheet',
		          ]
		widgets = {
			'arrangement_date': widgets.TextInput(
				attrs={'type': 'date', 'value': str(datetime.date.today()), 'placeholder': '请选择开始日期'}),
			'completion_date': widgets.TextInput(
				attrs={'type': 'date', 'value': str(datetime.date.today()), 'placeholder': '请选择完成日期'}),
		}
		
		error_messages = ''
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.fields['available'].disabled = True
		
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})
		self.fields['LAM_techinst_serial'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择检验工序..."})
		self.fields['machining_state'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择加工状态..."})
		self.fields['heat_treatment_state'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择热处理状态..."})

# 原材料理化检测
class RawStockPhyChemTestForm_New(ModelForm):
	# title = '原材料理化检测'
	# modelname = 'PhysicochemicalTest_Mission'
	#
	# class Meta:
	# 	model = PhysicochemicalTest_Mission
	# 	fields = ['RawStock',
	# 	          'LAM_techinst_serial',
	# 	          'commission_date',
	# 	          'heat_treatment_state',
	# 	          ]
	# 	widgets = {
	# 		'commission_date': widgets.TextInput(
	# 			attrs={'type': 'date', 'value': str(datetime.date.today()), 'placeholder': '请选择开始日期'}),
	# 	}
	# 	labels = {
	# 		'LAM_product': _('产品实例'),
	# 		'RawStock': _('原材料实例'),
	# 		'LAM_techinst_serial': _('工序'),
	# 		'commission_date': _('开始日期'),
	# 		'heat_treatment_state': _('热处理状态'),
	# 		'mechanicaltest_tensile': _('拉伸测试'),
	# 		'mechanicaltest_toughness': _('冲击测试'),
	# 		'chemicaltest': _('化学成分测试'),
	# 	}
	# 	error_messages = ''
	#
	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)
	#
	# 	for field in self.fields.values():
	# 		field.widget.attrs.update({'class': 'form-control'})
	title = '原材料理化检测'
	modelname = 'PhysicochemicalTest_Mission'
	previewtableTitle = '原材料检测任务'
	previewtablefields = {'LAM_techinst_serial': _('下达任务工序'), 'arrangement_date': _('下达任务日期')}

	class Meta:
		model = PhysicochemicalTest_Mission
		fields = ['RawStock',
		          'LAM_techinst_serial',
		          'commission_date',
		          'heat_treatment_state',
		          ]
		# fields = "__all__"
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
			'mechanicaltest_fracturetoughness': _('断裂韧性测试'),
			'chemicaltest': _('化学成分测试'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		'''原材料按类型分组显示'''
		rawstock_list = RawStock.objects.filter(available=True)
		rawstock_display_dict = {}
		for stock in rawstock_list:
			key = '%s-%s' % (str(stock.material), str(stock.rawstock_category))
			if key not in rawstock_display_dict:
				rawstock_display_dict[key] = [(stock.id, stock)]
			else:
				rawstock_display_dict[key].append((stock.id, stock))
		rawstock_data = [[key, values] for key, values in rawstock_display_dict.items()]
		self.fields['RawStock'].choices = rawstock_data

		self.fields['RawStock'].widget.attrs.update(
			{'onchange': 'loadTableData_RawStockMission(this.value)'})
		
		# 20200405 此处应清理无用的js函数
		# 辅助选择数据集
		self.techinst_datalist = LAMTechniqueInstruction.objects.filter(Q(available=True) & Q(filed=False)).order_by(
			'instruction_code', '-version_code', '-version_number')
		# print(self.techinst_datalist)
		# self.worktype_datalist = LAMProductionWorkType.objects.filter(Q(available=True))
		# self.productcode_datalist = LAMProduct.objects.filter(available=True)
		# self.RawStockBatchNumber_datalist = RawStock.objects.filter(available=True)

		# self.fields['RawStock'].queryset = RawStock.objects.filter(available=True)

		# NotFiledTechInst = LAMTechniqueInstruction.objects.filter(Q(filed=False) & Q(available=True))
		# 检验可选择的工序
		self.fields['LAM_techinst_serial'].queryset = LAM_TechInst_Serial.objects.filter(
			Q(available=True) & Q(technique_instruction__filed=False) & Q(selectable_PhyChemNonDestructiveTest=True))
		# self.fields['work_section'].queryset = Worksection.objects.filter(available=True)
		# self.fields['completion_date'].disabled = True
		# self.fields['available'].disabled = True

		# 辅助选择下拉菜单及文本框
		# self.fields['product_category'] = forms.ModelChoiceField(label='产品类别',
		#                                                          queryset=LAMProductCategory.objects.filter(
		#                                                              available=True),
		#                                                          empty_label='请选择产品类别',
		#                                                          required=False)
		# self.fields['RawStock_batchnumber'] = forms.CharField(label='原材料批号',
		#                                               max_length=50,
		#                                               required=False)
		# self.fields['technique_instruction'] = forms.ModelChoiceField(label='工艺文件',
		#                                                               queryset=self.techinst_datalist,
		#                                                               empty_label='请选择工艺文件',
		#                                                               required=False)
		# self.fields['work_type'] = forms.ModelChoiceField(label='工序',
		#                                                   queryset=self.worktype_datalist,
		#                                                   empty_label='请选择工序',
		#                                                   required=False)

		# 更新属性
		# 产品类别
		# self.fields['product_category'].widget.attrs.update(
		#     {'onchange': 'load_LAMTechInstandProduct_By_ProductCategory(this.value);'})
		# 工艺文件
		# self.fields['technique_instruction'].widget.attrs.update(
		# 	{'onchange': 'load_WorkType_By_LAMTechInst(this.value);'})
		# # 工序
		# self.fields['work_type'].widget.attrs.update(
		# 	{'onchange': 'refresh_techinst_serial();'})

		# self.fields['RawStock_batchnumber'].widget.attrs.update(
		# 	{'list': 'RawStock_BatchNumber_list', 'onblur': 'refresh_rawstock();'})

		# 辅助选择field
		# self.AuxiliarySelection = ('product_category',
		#                            'technique_instruction',
		#                            'work_type',
		#                            'RawStock_batchnumber')
		# 原始field
		self.OriginalFields = ('RawStock',
		                       'LAM_techinst_serial',
		                       'commission_date',
		                       'heat_treatment_state',
		                       )

		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})
		'''原材料'''

		self.fields['RawStock'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择原材料..."})
		'''检验工序'''
		self.fields['LAM_techinst_serial'].widget.attrs.update(
			{'class': 'form-control chosen-select', 'data-placeholder': "选择检验工序..."})

	def is_valid_custom(self):

		# try:
		# 	_Product = LAMProduct.objects.get(id=self.data['LAM_product'])
		# 	_ProdCate = _Product.product_category
		# 	_TechInst = LAM_TechInst_Serial.objects.get(id=self.data['LAM_techinst_serial']).technique_instruction
		#
		# 	if not (_Product in _TechInst.product.all() or _ProdCate in _TechInst.product_category.all()):
		# 		self.error_messages = '该产品与选中工艺文件未关联'
		# 		return False
		# except:
		# 	self.error_messages = '未知错误'
		# 	return False

		return self.is_valid()


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
	fracturetoughness_fields = [
		'试样编号',
		'取样部位',
		'取样方向',
		'测试温度/℃',
		'K<sub>IC</sub> / MPa×m<sup>1/2</sup>',
		'K<sub>Q</sub> / MPa×m<sup>1/2</sup>',
		'有效性判定',
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
		          'mechanicaltest_fracturetoughness',
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
			'mechanicaltest_fracturetoughness': _('断裂韧性测试'),
			'chemicaltest': _('化学成分测试'),
		}
		error_messages = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.fields['available'].disabled = True

		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})


#
class BreakBlockResumptionForm(forms.Form):
	name = 'BreakBlockResumptionForm'
	title='断点分块恢复成形'
	GUID = forms.CharField(max_length=50, label=None, widget=forms.HiddenInput())
	ParamCurrentPPOSX = forms.CharField(max_length=10, label='上一分块停光点X坐标P参数')
	ParamCurrentPPOSY = forms.CharField(max_length=10, label='上一分块停光点Y坐标P参数')
	ParamCurrentPPOSZ = forms.CharField(max_length=10, label='上一分块停光点Z坐标P参数')
	ParamCounter = forms.CharField(max_length=10, label='当前层已成形分块计数P参数')
	File = forms.FileField(required=True, label='待处理的Sub文件(*.nc)')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.fields['available'].disabled = True
		self.defaultParams = ['P196','P197','P198','P199']
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})

class SShapeBreakForm(forms.Form):
	name = 'SShapeBreakForm'
	title = '负搭接弓字步拆分'
	# PowderOnOrder = forms.CharField(max_length=10, label='开粉指令')
	# PowderOffOrder = forms.CharField(max_length=10, label='关粉指令')
	GUID = forms.CharField(max_length=50, label=None, widget=forms.HiddenInput())
	TurningFunction = forms.CharField(max_length=10, label='Track 切换函数')
	SwitchBlockFunction = forms.CharField(max_length=10, label='polygon 切换函数')
	IfPrintTurningFunction = forms.BooleanField(label='是否启用 Track 切换函数', required=False)
	IfPrintSwitchBlockFunction = forms.BooleanField(label='是否启用 polygon 切换函数', required=False)
	File = forms.FileField(required=True, label='待处理的Sub文件(*.nc/*.pim)')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.fields['available'].disabled = True
		# self.defaultParams = ['M12', 'M13', '1400', '1401', 'true', 'true']
		self.defaultParams = ['1400', '1401', 'true', 'true']
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})

class LAMTechInstSerial_PDF_Form(forms.Form):
	title = '工序实例 by PDF'
	# GUID = forms.CharField(max_length=50, label=None, widget=forms.HiddenInput())
	# GUID = forms.CharField(max_length=50, label='GUID')
	File = forms.FileField(required=True, label='待识别的PDF文件(*.pdf)')
	Technique_Instruction = forms.CharField(label='技术文件')
	# upload = forms.CharField(label='上传识别')
	# save = forms.CharField(label='保存')
	Technique_Instruction_ID = forms.CharField(max_length=50, label='', widget=forms.HiddenInput())
	
	
	# technique_instruction = forms.
	# class Meta:
	# 	model = LAM_TechInst_Serial
	# 	# fields = ['technique_instruction','serial_number','serial_worktype','serial_note','serial_content']
	# 	fields = "__all__"
	# 	labels = {
	# 		# 'filter_techinst': _('辅助筛选工艺文件'),
	# 		'technique_instruction': _('工艺文件'),
	# 		'serial_number': _('工序号'),
	# 		'serial_worktype': _('工序名称'),
	# 		'serial_note': _('工序概述'),
	# 		'serial_content': _('工序内容'),
	# 		'available': _('是否激活'),
	# 		'process_parameter': _('参数包'),
	# 		'selectable_Scheduling': _('是否可被调度模块选择'),
	# 		'selectable_LAM': _('是否可被激光成形模块选择'),
	# 		'selectable_HeatTreatment': _('是否可被热处理模块选择'),
	# 		'selectable_PhyChemNonDestructiveTest': _('是否可被检验模块选择'),
	# 		'selectable_RawStockSendRetrieve': _('是否可被库房模块选择'),
	# 		'selectable_Weighing': _('是否可被称重模块选择'),
	# 	}
	# 	error_messages = ''
	class Meta:
		# fields = ['GUID',
		#           'technique_instruction',
		#           ]

		fields = "__all__"
		# widgets = {
		#     # 'technique_instruction': widgets.TextInput(attrs={'class': 'form-control', 'list':"techinst_list"}),
		# }

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.technique_instruction_datalist = LAMTechniqueInstruction.objects.filter(
			Q(available=True) & Q(filed=False)).order_by(
			'instruction_code', '-version_code', '-version_number')
		
		# self.fields['technique_instruction'] = forms.ModelChoiceField(label='技术文件',
		#                                                   queryset=LAMTechniqueInstruction.objects.filter(available=True),
		#                                                   required=False)
		
		# self.fields['Technique_Instruction'].queryset = LAMTechniqueInstruction.objects.filter(
		# 	Q(available=True) & Q(filed=False)).order_by(
		# 	'instruction_code', '-version_code', '-version_number')
		# # self.fields['serial_worktype'].queryset = LAMProductionWorkType.objects.filter(available=True)
		
		self.fields['Technique_Instruction'].widget.attrs.update({'type': 'text', 'list': 'techinst_list', 'onchange': 'checkForm();'})
		
		# self.fields['step'].widget.attrs.update({'type': 'hidden'})
		# self.fields['available'].disabled = True
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})
		# self.fields['Technique_Instruction'].widget.attrs.update(
		# 	{'class': 'form-control chosen-select', 'data-placeholder': "选择技术文件...",'onchange': 'checkForm();'})

class RawStockFlow_Statistic_Form(forms.Form):
	title = '原材料发放统计'
	statistic_data_thead_fields = ['零件编号', '生产任务', '工段',  '合计用粉', '合计收粉']
	statistic_data_with_cluster_basic_thead_fields = ['合计用粉', '合计收粉']
	
	statistic_data_tbody_fields = ['str_product_code', 'str_techinst_serial', 'LAM_mission__work_section__code', 'Sum_Used', 'Sum_Retrieve']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['filter_start_date'] = forms.DateField(label='时间筛选-开始',
		                                                  widget=widgets.TextInput(
			                                                  attrs={'type': 'date',
			                                                         'value': str((datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")),
			                                                         'placeholder': '选择筛选开始日期'}),
		                                                  required=False)
		self.fields['filter_finish_date'] = forms.DateField(label='时间筛选-结束',
		                                                  widget=widgets.TextInput(
			                                                  attrs={'type': 'date',
			                                                         'value': str((datetime.datetime.now() ).strftime("%Y-%m-%d")),
			                                                         'placeholder': '选择筛选结束日期'}),
		                                                  required=False)
		self.fields['filter_product_code'] = forms.MultipleChoiceField(label='产品编号筛选')
		self.fields['filter_product_category'] = forms.MultipleChoiceField(label='产品类别筛选')
		self.fields['filter_techinst_serial'] = forms.MultipleChoiceField(label='工序实例筛选')
		self.fields['cluster_fields'] = forms.MultipleChoiceField(label='聚类', choices=(
			('worksection', '成形工段'),
			('productcategory', '产品类别'),
			('productcode', '产品编号'),
		))
		
		# 产品类别列表
		product_category_list = LAMProductCategory.objects.filter(available=True)
		# 产品按类别分类
		product_choice = [[_category.product_name, [(_product.id, _product.product_code) for _product in
		                                            LAMProduct.objects.filter(
			                                            (Q(product_category=_category) & Q(available=True)))]] for
		                  _category in product_category_list]
		# 工艺文件类别列表
		techinst_list = LAMTechniqueInstruction.objects.filter(available=True)
		# 工序按工艺文件分类
		techinst_serial = [[str(_techinst), [(_serial.id,
		                                              '%s %s[%s]'%(
			                                              _serial.serial_number,
			                                              _serial.serial_worktype,
			                                              _serial.serial_note
		                                              )) for _serial in
		                                            LAM_TechInst_Serial.objects.filter(
			                                            (Q(technique_instruction=_techinst)))]] for
		                  _techinst in techinst_list]
		
		self.fields['filter_product_code'].choices = product_choice
		
		self.fields['filter_product_category'].choices = [(_category.id, str(_category)) for _category in LAMProductCategory.objects.filter(available=True)]
		self.fields['filter_techinst_serial'].choices = techinst_serial
		
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})
		self.fields['cluster_fields'].widget.attrs.update({'class': 'form-control chosen-select', 'data-placeholder': "[可选]选择聚类项..."})
		self.fields['filter_product_code'].widget.attrs.update({'class': 'form-control chosen-select', 'data-placeholder': "[可选]选择产品..."})
		self.fields['filter_product_category'].widget.attrs.update({'class': 'form-control chosen-select', 'data-placeholder': "[可选]选择产品类别..."})
		self.fields['filter_techinst_serial'].widget.attrs.update({'class': 'form-control chosen-select', 'data-placeholder': "[可选]选择工序..."})