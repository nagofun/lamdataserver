# -*- coding: gbk -*-
from django.urls import path, re_path

import time
import datetime
from . import views
from . import query_views

# import LAMProcessData.process_realtime_finedata as RT_FineData
# from apscheduler.schedulers.blocking import BlockingScheduler


urlpatterns = [
    path('login/',views.loginview),
    path('logout/', views.logoutview),
    path('userProfile/', views.userprofile),
    path('resetPassword/', views.resetpassword),
    # path('resetPassword/', 'django.contrib.auth.views.password_reset', kwargs={'template_name': 'password_reset_form.html'}, name='password-reset'),

    path('403/', views.errorview_403),

    path('', views.Index),
    path('time/', views.current_datetime),
    path('test/', views.test),
    path('test1/', views.test1),
    path('3Dtestdata/', views.get3DTestData),
    path('3Dtestdata2/', views.get3DTestData2),

    path('gettimeitem/', views.current_datetime_item),
    re_path(
        r'Oxygen/(?P<MACAddress>.{12})/(?P<OxygenValue>.+)/(?P<OxygenSensorValue>.+)/(?P<InternalPressureValue>.+)/(?P<md5Key>.+)$',
        views.GetLAMProcessData_Oxygen),
    re_path(
        r'Laser/(?P<MACAddress>.{12})/(?P<LaserTime>.+)/(?P<LaserPowerValue>.+)/(?P<LaserLightpathTemperatureValue>.+)/(?P<LaserLaserTemperatureValue>.+)/(?P<md5Key>.+)$',
        views.GetLAMProcessData_Laser),

    # 上传激光成形过程参数截图
    # path('LAMProcessData/CNCData/UpdateScreen/', views.LAMProcessData_UpdateCNCData),
    path('LAMProcessData/CNCData/UpdateScreen/', views.PostLAMProcessData_CNCdata),
    # 上传CNC解析数据
    path('LAMProcessData/CNCData/UpdateScreenRecognition/', views.PostLAMProcessData_CNCdataScreenRecognition),

    # re_path(r'POSTCNCdata/', views.PostLAMProcessData_CNCdata),
    # 上传激光器采集数据
    path('LAMProcessData/UpdateLaserData/', views.PostLAMProcessData_Laser),
    # 上传氧分析仪采集数据
    path('LAMProcessData/UpdateOxygenData/', views.PostLAMProcessData_Oxygen),
    # path('PostLAMProcessData/Oxygen/', views.PostLAMProcessData_Oxygen),

    # 更新数据库内时间戳，日期整数 -
    path('LAMProcessData/UpdateRecordTimeStamp/', views.UpdateRecordTimeStamp),
    # 更新数据库CNCProcessStatus表中的Z_Value、ProgramName信息 -
    path('LAMProcessData/UpdateRecordCNCProcessStatus/', views.UpdateRecordCNCProcessStatus),
    # 更新数据库Process_Oxygendata_Date_Worksection_indexing
    path('LAMProcessData/UpdateRecordOxygendataIndexing/', views.UpdateOxygendata_Date_Worksection_indexing),
    # 更新数据库Process_Laserdata_Date_Worksection_indexing
    path('LAMProcessData/UpdateRecordLaserdataIndexing/', views.UpdateLaserdata_Date_Worksection_indexing),
    # 更新数据库Process_CNCStatusdata_Date_Worksection_indexing
    path('LAMProcessData/UpdateRecordCNCStatusdataIndexing/', views.UpdateCNCStatusdata_Date_Worksection_indexing),
    # 更新数据库Process_Realtime_FineData_By_WorkSectionID
    path('LAMProcessData/UpdateRecordToFineData/', views.Update_ExistingData_to_FineData),
    # 更新数据库Process_Realtime_FineData_By_WorkSectionID中的时间戳
    path('LAMProcessData/UpdateFineDataDatetime/', views.Update_ExistingFineData_datetime),
    # 更新数据库Process_Realtime_FineData_By_WorkSectionID中的不连续数据
    path('LAMProcessData/UpdateFineEmptyData/', views.Update_ExistingFineData_PatchEmptyData),
    # 更新数据库Process_Realtime_FineData_By_WorkSectionID中的机床界面信息if_exec_intr，if_interrupt_intr
    path('LAMProcessData/UpdateFineData_IfIntr/', views.Update_ExistingFinData_If_intr),

    path('DrawData/Oxygen/', views.DrawData_Oxygen),
    # 厂房
    path('EditBasicInfomation/Workshop/', views.OperateData_workshop),
	path('EditBasicInfomation/Workshop/add/', views.new_workshop),
    path('EditBasicInfomation/Workshop/edit/', views.edit_workshop),
    path('EditBasicInfomation/Workshop/delete/', views.del_workshop),
    # 计算机
    path('EditBasicInfomation/Computer/', views.OperateData_computer),
	path('EditBasicInfomation/Computer/add/', views.new_computer),
    path('EditBasicInfomation/Computer/edit/', views.edit_computer),
    path('EditBasicInfomation/Computer/delete/', views.del_computer),
    # 工段
    path('EditBasicInfomation/Worksection/', views.OperateData_worksection),
	path('EditBasicInfomation/Worksection/add/', views.new_worksection),
    path('EditBasicInfomation/Worksection/edit/', views.edit_worksection),
    path('EditBasicInfomation/Worksection/delete/', views.del_worksection),
    # 材料
    path('EditBasicInfomation/LAMMaterial/', views.OperateData_lammaterial),
	path('EditBasicInfomation/LAMMaterial/add/', views.new_lammaterial),
    path('EditBasicInfomation/LAMMaterial/edit/', views.edit_lammaterial),
    path('EditBasicInfomation/LAMMaterial/delete/', views.del_lammaterial),
    # 原材料类别
    path('EditBasicInfomation/RawStockCategory/', views.OperateData_rawstockcategory),
	path('EditBasicInfomation/RawStockCategory/add/', views.new_rawstockcategory),
    path('EditBasicInfomation/RawStockCategory/edit/', views.edit_rawstockcategory),
    path('EditBasicInfomation/RawStockCategory/delete/', views.del_rawstockcategory),
    # 数控系统屏幕界面类别
    path('EditBasicInfomation/CNCStatusCategory/', views.OperateData_cncstatuscategory),
	path('EditBasicInfomation/CNCStatusCategory/add/', views.new_cncstatuscategory),
    path('EditBasicInfomation/CNCStatusCategory/edit/', views.edit_cncstatuscategory),
    path('EditBasicInfomation/CNCStatusCategory/delete/', views.del_cncstatuscategory),
    # 产品类别
    path('EditBasicInfomation/ProductCategory/', views.OperateData_lamproductcategory),
	path('EditBasicInfomation/ProductCategory/add/', views.new_lamproductcategory),
    path('EditBasicInfomation/ProductCategory/edit/', views.edit_lamproductcategory),
    path('EditBasicInfomation/ProductCategory/delete/', views.del_lamproductcategory),
    # 激光成形工艺文件
    path('EditBasicInfomation/LAMTechniqueInstruction/', views.OperateData_lamtechniqueinstruction),
	path('EditBasicInfomation/LAMTechniqueInstruction/add/', views.new_lamtechniqueinstruction),
    path('EditBasicInfomation/LAMTechniqueInstruction/edit/', views.edit_lamtechniqueinstruction),
    path('EditBasicInfomation/LAMTechniqueInstruction/delete/', views.del_lamtechniqueinstruction),
    # 激光成形工艺文件与产品类别的关联
    path('EditBasicInfomation/LAMProdCate_TechInst/', views.OperateData_lamprodcate_techinst),
	path('EditBasicInfomation/LAMProdCate_TechInst/add/', views.new_lamprodcate_techinst),
    path('EditBasicInfomation/LAMProdCate_TechInst/edit/', views.edit_lamprodcate_techinst),
    path('EditBasicInfomation/LAMProdCate_TechInst/delete/', views.del_lamprodcate_techinst),
    # 基础工序
    path('EditBasicInfomation/LAMProductionWorkType/', views.OperateData_lamproductionworktype),
	path('EditBasicInfomation/LAMProductionWorkType/add/', views.new_lamproductionworktype),
    path('EditBasicInfomation/LAMProductionWorkType/edit/', views.edit_lamproductionworktype),
    path('EditBasicInfomation/LAMProductionWorkType/delete/', views.del_lamproductionworktype),

    # 基础工序实例
    path('EditBasicInfomation/LAMTechInstSerial/', views.OperateData_lamtechinstserial),
    path('EditBasicInfomation/LAMTechInstSerial/add/', views.new_lamtechinstserial),
    path('EditBasicInfomation/LAMTechInstSerial/edit/', views.edit_lamtechinstserial),
    path('EditBasicInfomation/LAMTechInstSerial/delete/', views.del_lamtechinstserial),
    # 工序实例 PDF生成
    path('EditBasicInfomation/New_LAMTechInstSerial_By_PDF/', views.new_lamtechinstserial_by_pdf),
    # 上传文件，分析后返回结果
    path('EditBasicInfomation/New_LAMTechInstSerial_By_PDF/UploadFile/', views.new_lamtechinstserial_upload_pdf),
    # 保存pdf中的工序信息
    path('EditBasicInfomation/New_LAMTechInstSerial_By_PDF/SavePDF/', views.new_lamtechinstserial_save_pdf),
    # 查询PDF识别进度
    re_path('QueryData/ProgressBarValue/New_LAMTechInstSerial_UploadPDFFile_By_TechInstID/(?P<TechInstID>(.+))/$',
            query_views.queryData_ProgressBarValue_New_LAMTechInstSerial_UploadPDFFile_By_TechInstID),
    

    # 工艺参数包
    path('EditBasicInfomation/LAMProcessParameters/', views.OperateData_lamprocessparameters),
    path('EditBasicInfomation/LAMProcessParameters/delete/', views.del_lamprocessparameters),
    # 增加激光成形参数包
    re_path('EditBasicInfomation/LAMProcessParameters/AddLAMParameter/$',
                views.new_lamprocessparameters),
    # 编辑激光成形参数包
    re_path('EditBasicInfomation/LAMProcessParameters/EditLAMParameter/(?P<ProcessParameterItemID>(.+))/$',
                views.edit_lamprocessparameters),

    # 增加参数条件单元
    re_path('EditBasicInfomation/LAMProcessParameters/AddConditionalCell/(?P<ProcessParameterItemID>(.+))/$',
                views.new_lamprocessparameterConditionalCell),
    # 编辑参数条件单元
    re_path('EditBasicInfomation/LAMProcessParameters/EditConditionalCell/(?P<ConditionalCellItemID>(.+))/$',
                views.edit_lamprocessparameterConditionalCell),

    # 编辑参数累加单元
    re_path('EditBasicInfomation/LAMProcessParameters/EditAccumulateCell/(?P<ProcessParameterItemID>(.+))/$',
                views.edit_lamprocessparameterAccumulateCell),

    # 保存适用的工序
    re_path('EditBasicInfomation/LAMProcessParameters/SaveTechInstSerial/$',
                views.save_lamprocessparameterTechInstSerial),



    # 取样部位
    path('EditBasicInfomation/SamplingPosition/', views.OperateData_samplingposition),
	path('EditBasicInfomation/SamplingPosition/add/', views.new_samplingposition),
    path('EditBasicInfomation/SamplingPosition/edit/', views.edit_samplingposition),
    path('EditBasicInfomation/SamplingPosition/delete/', views.del_samplingposition),

	# 取样方向
    path('EditBasicInfomation/SamplingDirection/', views.OperateData_samplingdirection),
	path('EditBasicInfomation/SamplingDirection/add/', views.new_samplingdirection),
    path('EditBasicInfomation/SamplingDirection/edit/', views.edit_samplingdirection),
    path('EditBasicInfomation/SamplingDirection/delete/', views.del_samplingdirection),

	# 热处理状态
    path('EditBasicInfomation/HeatTreatmentState/', views.OperateData_heattreatmentstate),
	path('EditBasicInfomation/HeatTreatmentState/add/', views.new_heattreatmentstate),
    path('EditBasicInfomation/HeatTreatmentState/edit/', views.edit_heattreatmentstate),
    path('EditBasicInfomation/HeatTreatmentState/delete/', views.del_heattreatmentstate),

    # 产品实例
    path('ProcessRecords/LAMProduct/', views.OperateData_lamproduct),
	path('ProcessRecords/LAMProduct/add/', views.new_lamproduct),
    path('ProcessRecords/LAMProduct/edit/', views.edit_lamproduct),
    path('ProcessRecords/LAMProduct/delete/', views.del_lamproduct),
    # 生产任务
    path('ProcessRecords/LAMProcessMission/', views.OperateData_lamprocessmission),
    path('ProcessRecords/LAMProcessMission/add/', views.new_lamprocessmission),
    path('ProcessRecords/LAMProcessMission/finish/', views.finish_lamprocessmission),
    path('ProcessRecords/LAMProcessMission/delete/', views.del_lamprocessmission),

    # 生产任务事后划分
    path('ProcessRecords/LAMProcessMission/CutRecordsByTime/', views.lamprocessmission_CutRecords_by_Time),

    # 生产工段操作页面
    #
    re_path('ProcessRecords/WorksectionOperate_by_id/(?P<WorksectionID>(.+))/$', views.lamprocess_worksection_operate),


    # 原材料
    path('ProcessRecords/RawStock/', views.OperateData_rawstock),
    path('ProcessRecords/RawStock/add/', views.new_rawstock),
    path('ProcessRecords/RawStock/edit/', views.edit_rawstock),
    path('ProcessRecords/RawStock/delete/', views.del_rawstock),

    # 原材料发放回收
    path('ProcessRecords/RawStockFlow/', views.rawstockflow),
    path('ProcessRecords/RawStockFlow/send/', views.send_rawstockflow),
    path('ProcessRecords/RawStockFlow/retrieve/', views.retrieve_rawstockflow),
    path('ProcessRecords/RawStockFlow/edit/', views.edit_rawstockflow),
    path('ProcessRecords/RawStockFlow/delete/', views.del_rawstockflow),


    # 激光成形现场
    # path('ProcessRecords/WorkSectionOperation/', views.worksection_operation),


    # 检验记录
    path('InspectionRecords/ProcessMissionInspection/LAMProcess/', views.BrowseData_MissionLAMProcessInspection),
    # 绘制曲线
    re_path('InspectionRecords/ProcessMissionInspection/LAMProcess/ByMissionID/(?P<MissionItemID>(.+))/$',views.Inspect_MissionLAMProcessInspection),


    path('InspectionRecords/PhysicochemicalTest/Product/', views.OperateData_ProductPhyChemTest),
    path('InspectionRecords/PhysicochemicalTest/Product/add/', views.new_ProductPhyChemTest),
    path('InspectionRecords/PhysicochemicalTest/Product/edit/', views.edit_ProductPhyChemTest),

    path('InspectionRecords/PhysicochemicalTest/RawStock/', views.OperateData_RawStockPhyChemTest),
    path('InspectionRecords/PhysicochemicalTest/RawStock/add/', views.new_RawStockPhyChemTest),
    path('InspectionRecords/PhysicochemicalTest/RawStock/edit/', views.edit_RawStockPhyChemTest),





    # 检查成形记录
    re_path('QueryData/InspectLAMProcessRecords/Complete/(?P<MissionItemID>(.+))/$', query_views.queryData_Inspect_Complete_MissionLAMProcessRecords),
    re_path('QueryData/ProgressBarValue/InspectionLAMRecords_By_MissionID/(?P<MissionID>(.+))/$',
            query_views.queryData_ProgressBarValue_InspectionLAMRecords_By_MissionID),

    # 打开任务筛选弹窗
    re_path('AnalyseLAMProcess/MissionFilter/(?P<AnalyseType>(.+))/$', views.AnalyseLAMProcess_MissionFilter),
    # 分析成形制造过程-成形高度
    re_path('AnalyseLAMProcess/ZValue/$', views.AnalyseLAMProcess_ZValue),
    re_path('QueryData/AnalyseLAMProcess_ZValue/$', query_views.queryData_Analysedata_Zvalue_By_MissionIDList),
    # 分析成形制造过程-累加数据
    re_path('AnalyseLAMProcess/AccumulateData/$', views.AnalyseLAMProcess_AccumulateData),
    re_path('QueryData/AnalyseLAMProcess_AccumulateData/$', query_views.queryData_Analysedata_AccumulateData_By_MissionIDList),
    # 分析成形制造过程-层内分析
    re_path('AnalyseLAMProcess/LayerData/$', views.AnalyseLAMProcess_LayerData),
    re_path('QueryData/AnalyseLAMProcess_LayerData/$', query_views.queryData_Analysedata_LayerData_By_MissionIDList),
    # 分析成形制造过程-瞬时速率空间分布
    re_path('AnalyseLAMProcess/ScanningRate3D/$', views.AnalyseLAMProcess_ScanningRate3D),
    re_path('QueryData/AnalyseLAMProcess_ScanningRate3D/$', query_views.queryData_Analysedata_ScanningRate3D_By_MissionIDList),



    # 弹出子窗口
    re_path('InspectionRecords/PhysicochemicalTest/AddTensile/(?P<MissionItemID>(.+))/$',
            views.PhyChemTest_AddTensile),
    re_path('InspectionRecords/PhysicochemicalTest/EditTensile/(?P<TensileID>(.+))/$',
            views.PhyChemTest_EditTensile),
    re_path('InspectionRecords/PhysicochemicalTest/AddToughness/(?P<MissionItemID>(.+))/$',
            views.PhyChemTest_AddToughness),
    re_path('InspectionRecords/PhysicochemicalTest/EditToughness/(?P<ToughnessID>(.+))/$',
            views.PhyChemTest_EditToughness),
    re_path('InspectionRecords/PhysicochemicalTest/AddFracturetoughness/(?P<MissionItemID>(.+))/$',
            views.PhyChemTest_AddFracturetoughness),
    re_path('InspectionRecords/PhysicochemicalTest/EditFracturetoughness/(?P<FracturetoughnessID>(.+))/$',
            views.PhyChemTest_EditFracturetoughness),
    re_path('InspectionRecords/PhysicochemicalTest/AddChemicalElement/(?P<MissionItemID>(.+))/(?P<IfProductTest>(.+))/$',
            views.PhyChemTest_AddChemicalElement),
    re_path('InspectionRecords/PhysicochemicalTest/EditChemicalElement/(?P<MissionItemID>(.+))/(?P<ChemicalItemID>(.+))/(?P<IfProductTest>(.+))/$',
            views.PhyChemTest_EditChemicalElement),

    # 编程小工具
    # 复位后自上次已成形的分块继续成形
    path('PracticalTools/BreakBlockResumption/', views.PracticalTools_BreakBlockResumption),
    # 负搭接弓字步拆分输出
    path('PracticalTools/SShapeBreak/', views.PracticalTools_SShapeBreak),
    re_path('QueryData/ProgressBarValue/PracticalTools_SShapeBreak_By_GUID/(?P<GUID>(.+))/$',
            query_views.queryData_ProgressBarValue_PracticalTools_SShapeBreak_By_GUID),
    re_path('QueryData/ProgressBarValue/PracticalTools_BreakBlockResumption_By_GUID/(?P<GUID>(.+))/$',
            query_views.queryData_ProgressBarValue_PracticalTools_BreakBlockResumption_By_GUID),

    # 下载文件
    re_path('DownLoadTempFile/(?P<tempfilepath>(.+))/$',
            views.download_template),

    # axjx查询URL
    re_path('QueryData/PreviewTable/LAMTechniqueInstruction/(?P<TechInstID>(.+))/$',
            query_views.queryData_LAMTechInst_Preview),
    re_path('QueryData/PreviewTable/LAMTechniqueInstruction_SerialDetails/(?P<TechInstID>(.+))/$',
            query_views.queryData_LAMTechInst_SerialDetails),
    re_path('QueryData/PreviewTable/LAMProductMission/(?P<ProductID>(.+))/$',
            query_views.queryData_LAMProductMission_Preview),

    re_path('QueryData/PreviewTable/ProductPhyChemTestMission/(?P<ProductID>(.+))/$',
            query_views.queryData_ProductPhyChemTestMission_Preview),
    re_path('QueryData/PreviewTable/RawStockPhyChemTestMission/(?P<RawStockID>(.+))/$',
            query_views.queryData_RawStockPhyChemTestMission_Preview),


    # re_path('QueryData/LAMTechniqueInstruction_By_ProductCategory/(?P<ProductCategoryID>(.+))/$',
    #         query_views.queryData_LAMTechInst_By_ProdCate),

    # 根据参数包ID查询包含的条件单元
    re_path('QueryData/LAMProcessParameterConditionalCell_By_ProcessParameterID/(?P<ProcessParameterID>(.+))/$',
            query_views.queryData_LAMProcessParameterConditionalCell),

    # 根据参数包ID查询包含的累加单元
    re_path('QueryData/LAMProcessParameterAccumulateCell_By_ProcessParameterID/(?P<ProcessParameterID>(.+))/$',
            query_views.queryData_LAMProcessParameterAccumulateCell),

    # 根据参数包ID查询适用工序列表
    re_path('QueryData/LAMProcessParameter_TechInstSerial_By_ProcessParameterID/(?P<ProcessParameterID>(.+))/$',
            query_views.queryData_LAMProcessParameterTechInstSerial),

    # 列出所有工序
    re_path('QueryData/LAMProcessParameter_TechInstSerial/$',
            query_views.queryData_LAMProcessParameterTechInstSerial_Refresh),



    # 根据零件编号查询可用的工艺文件
    re_path('QueryData/LAMTechniqueInstruction_By_ProductCode/(?P<ProductCode>(.+))/$',
            query_views.queryData_LAMTechInst_By_ProductCode),

    # 以工艺文件id查询该工艺文件所有工序
    re_path('QueryData/WorkType_By_LAMTechInst/(?P<LAMTechInstID>(.+))/$',
            query_views.queryData_WorkType_By_LAMTechInst),

    # 以工艺文件id查询该工艺文件所有可被激光成形模块选择的工序
    re_path('QueryData/WorkType_By_LAMTechInst_filter_LAM/(?P<LAMTechInstID>(.+))/$',
            query_views.queryData_WorkType_By_LAMTechInst_filter_LAM),

    # 以工艺文件id查询该工艺文件所有可被检验模块选择的工序
    re_path('QueryData/WorkType_By_LAMTechInst_filter_PhyChemTest/(?P<LAMTechInstID>(.+))/$',
            query_views.queryData_WorkType_By_LAMTechInst_filter_PhyChemTest),

    # 以工艺文件id查询该工艺文件所有可被库房模块选择的工序
    re_path('QueryData/WorkType_By_LAMTechInst_filter_RawStockSendRetrieve/(?P<LAMTechInstID>(.+))/$',
            query_views.queryData_WorkType_By_LAMTechInst_filter_RawStockSendRetrieve),

    # 以零件类型查询产品列表
    re_path('QueryData/Product_By_ProductCategory/(?P<ProductCategoryID>(.+))/$',
            query_views.queryData_Product_By_ProductCategory),

    # 以零件编号查询零件id
    re_path('QueryData/ProductID_By_ProductCode/(?P<ProductCode>(.+))/$',
            query_views.queryData_ProductID_By_ProductCode),

    # 以原材料批号查询原材料id
    re_path('QueryData/RawStockID_By_RawStockBatchNumber/(?P<RawStockBatchNumber>(.+))/$',
            query_views.queryData_RawStockID_By_RawStockBatchNumber),
    # 以任务id查询工段id
    re_path('QueryData/WorksectionId_By_MissionID/(?P<MissionID>(.+))/$',
            query_views.queryData_WorksectionId_By_MissionID),

    # 以任务id查询已存在的起止时间（如有）
    re_path('QueryData/StartFinishTime_By_MissionID/(?P<MissionID>(.+))/$',
            query_views.queryData_StartFinishTime_By_MissionID),

	# 以任务id查询下达任务日期
    re_path('QueryData/ArrangementDate_By_MissionID/(?P<MissionID>(.+))/$',
            query_views.queryData_ArrangementDate_By_MissionID),

	# 以零件编号查询任务列表
	re_path('QueryData/Mission_By_ProductCode/(?P<ProductCode>(.+))/$',
            query_views.queryData_Mission_By_ProductCode),

    # 以工段id、起止时间、时间间隔查询氧含量数据
    re_path('QueryData/Oxydata_By_WorkSectionDatetime/(?P<WorksectionID>(.+))/(?P<StartDateTime>(.+))/(?P<FinishDateTime>(.+))/(?P<Interval>(.+))/$',
            query_views.queryData_Oxydata_By_WorkSectionDatetime),
    # 以工段id、起止时间、时间间隔查询激光功率数据
    re_path('QueryData/Laserdata_By_WorkSectionDatetime/(?P<WorksectionID>(.+))/(?P<StartDateTime>(.+))/(?P<FinishDateTime>(.+))/(?P<Interval>(.+))/$',
            query_views.queryData_Laserdata_By_WorkSectionDatetime),

    # 以工段id、起止时间、时间间隔查询氧含量、激光功率、CNC-Z数据
    re_path('QueryData/Data_By_WorkSectionDatetime/(?P<ifForceRefresh>(.+))/(?P<WorksectionID>(.+))/(?P<StartDateTime>(.+))/(?P<FinishDateTime>(.+))/(?P<Interval>(.+))/$',
            query_views.queryData_data_By_WorkSectionDatetime),

    # 以任务id、起止时间、时间间隔查询氧含量数据
    re_path(
        'QueryData/Oxydata_By_MissionDatetime/(?P<MissionID>(.+))/(?P<StartDateTime>(.+))/(?P<FinishDateTime>(.+))/(?P<Interval>(.+))/$',
        query_views.queryData_Oxydata_By_MissionDatetime),

    # 以工段id、起止时间、时间间隔查询CNC-Z数据
    # re_path('QueryData/Laserdata_By_WorkSectionDatetime/(?P<Worksection>(.+))/(?P<StartTime>(.+))/(?P<FinishTime>(.+))/interval/$',
    #         query_views.queryData_Laserdata_By_WorkSectionDatetime),

    # 以MissionID查询FindData中记录数据 图形显示 graph
    re_path('QueryData/FineData_By_MissionID/(?P<MissionItemID>(.+))/(?P<DateStr>(.+))/(?P<HourStr>(.+))/$',
            query_views.queryData_finedata_By_MissionID),
    # 以MissionID查询FindData中记录数据
    re_path('QueryData/FineData_By_MissionID_Datetime/(?P<MissionItemID>(.+))/(?P<startTimestamp>(.+))/(?P<finishTimestamp>(.+))/$',
            query_views.queryData_finedata_By_MissionID_timestamp),

    # 以工段id查询最新更新数据时间
    re_path(
        'QueryData/RecordLastTime_by_WorksectionID/(?P<WorksectionID>(.+))/$', query_views.queryData_RecordLastTime_by_WorksectionID),
    # 以工段id查询实时数据
    re_path(
        'QueryData/RealTimeRecord_by_WorksectionID/(?P<WorksectionID>(.+))/$',
        query_views.queryData_RealTimeRecord_by_WorksectionID),




    # analyse 解析激光成形过程参数
    # --获取CNC数控机床界面信息参数
    re_path('QueryData/CNCData/DownloadScreenInfo/', query_views.DownloadCNCScreenInfo),
    # --获取CNC数控机床界面截图
    re_path('QueryData/CNCData/DownloadScreenImage_By_ID/(?P<cncstatus_id>(.+))/$', query_views.DownloadCNCScreenImage_by_id),



    # path('EditBasicInfomation/Workshop/edit.*&item_id=<int:item_id>&.*', views.edit_workshop),

    # path('EditBasicInfomation/Workshop/edit*', views.edit_workshop),
    # path('EditBasicInfomation/Workshop/edit', views.edit_workshop),
    # path('EditBasicInfomation/Workshop/delete.*&item_id=(?P<item_id>.+)&.*', views.del_workshop),

]

# urlpatterns += patterns('lamdataserver.views',
#     (r'^time/$', current_datetime),
#     (r'^gettimeitem/$', current_datetime_item),
#     (r'^GetLAMProcessData/Oxygen/(?P<MACAddress>.{12})/(?P<OxygenValue>.+)/(?P<OxygenSensorValue>.+)/(?P<InternalPressureValue>.+)/(?P<md5Key>.+)$', GetLAMProcessData_Oxygen),
#     (r'^GetLAMProcessData/Laser/(?P<MACAddress>.{12})/(?P<LaserTime>.+)/(?P<LaserPowerValue>.+)/(?P<LaserLightpathTemperatureValue>.+)/(?P<LaserLaserTemperatureValue>.+)/(?P<md5Key>.+)$',
#                         GetLAMProcessData_Laser),
#     (r'^PostLAMProcessData/Oxygen/$', PostLAMProcessData_Oxygen),
#     (r'^DrawData/Oxygen/$',DrawData_Oxygen),
#     # url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document.root':settings.STATICFILES_DIRS}),
# )

# print('urls.py end')
