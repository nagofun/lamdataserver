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
    path('SystemOperation/', views.SystemOperation),
    re_path('QueryData/ProgressBarValue/Update_ExistingData_to_FineData/(?P<dataType>(.+))/$',
            query_views.queryData_ProgressBarValue_Update_ExistingData_to_FineData),
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
    
    

    # �ϴ�������ι��̲�����ͼ
    # path('LAMProcessData/CNCData/UpdateScreen/', views.LAMProcessData_UpdateCNCData),
    path('LAMProcessData/CNCData/UpdateScreen/', views.PostLAMProcessData_CNCdata),
    # �ϴ�CNC��������
    path('LAMProcessData/CNCData/UpdateScreenRecognition/', views.PostLAMProcessData_CNCdataScreenRecognition),

    # re_path(r'POSTCNCdata/', views.PostLAMProcessData_CNCdata),
    # �ϴ��������ɼ�����
    path('LAMProcessData/UpdateLaserData/', views.PostLAMProcessData_Laser),
    # �ϴ��������ǲɼ�����
    path('LAMProcessData/UpdateOxygenData/', views.PostLAMProcessData_Oxygen),
    # path('PostLAMProcessData/Oxygen/', views.PostLAMProcessData_Oxygen),

    # �������ݿ���ʱ������������� -
    path('LAMProcessData/UpdateRecordTimeStamp/', views.UpdateRecordTimeStamp),
    # �������ݿ�CNCProcessStatus���е�Z_Value��ProgramName��Ϣ -
    path('LAMProcessData/UpdateRecordCNCProcessStatus/', views.UpdateRecordCNCProcessStatus),
    # �������ݿ�Process_Oxygendata_Date_Worksection_indexing
    path('LAMProcessData/UpdateRecordOxygendataIndexing/', views.UpdateOxygendata_Date_Worksection_indexing),
    # �������ݿ�Process_Laserdata_Date_Worksection_indexing
    path('LAMProcessData/UpdateRecordLaserdataIndexing/', views.UpdateLaserdata_Date_Worksection_indexing),
    # �������ݿ�Process_CNCStatusdata_Date_Worksection_indexing
    path('LAMProcessData/UpdateRecordCNCStatusdataIndexing/', views.UpdateCNCStatusdata_Date_Worksection_indexing),
    # �������ݿ�Process_Realtime_FineData_By_WorkSectionID
    re_path('LAMProcessData/UpdateRecordToFineData/(?P<datatype>(.+))/', views.Update_ExistingData_to_FineData),
    # �������ݿ�Process_Realtime_FineData_By_WorkSectionID�е�ʱ���
    path('LAMProcessData/UpdateFineDataDatetime/', views.Update_ExistingFineData_datetime),
    # �������ݿ�Process_Realtime_FineData_By_WorkSectionID�еĲ���������
    path('LAMProcessData/UpdateFineEmptyData/', views.Update_ExistingFineData_PatchEmptyData),
    # �������ݿ�Process_Realtime_FineData_By_WorkSectionID�еĻ���������Ϣif_exec_intr��if_interrupt_intr
    path('LAMProcessData/UpdateFineData_IfIntr/', views.Update_ExistingFinData_If_intr),

    path('DrawData/Oxygen/', views.DrawData_Oxygen),
    # ����
    path('EditBasicInfomation/Workshop/', views.OperateData_workshop),
	path('EditBasicInfomation/Workshop/add/', views.new_workshop),
    path('EditBasicInfomation/Workshop/edit/', views.edit_workshop),
    path('EditBasicInfomation/Workshop/delete/', views.del_workshop),
    # �����
    path('EditBasicInfomation/Computer/', views.OperateData_computer),
	path('EditBasicInfomation/Computer/add/', views.new_computer),
    path('EditBasicInfomation/Computer/edit/', views.edit_computer),
    path('EditBasicInfomation/Computer/delete/', views.del_computer),
    # ����
    path('EditBasicInfomation/Worksection/', views.OperateData_worksection),
	path('EditBasicInfomation/Worksection/add/', views.new_worksection),
    path('EditBasicInfomation/Worksection/edit/', views.edit_worksection),
    path('EditBasicInfomation/Worksection/delete/', views.del_worksection),
    # ����
    path('EditBasicInfomation/LAMMaterial/', views.OperateData_lammaterial),
	path('EditBasicInfomation/LAMMaterial/add/', views.new_lammaterial),
    path('EditBasicInfomation/LAMMaterial/edit/', views.edit_lammaterial),
    path('EditBasicInfomation/LAMMaterial/delete/', views.del_lammaterial),
    # ԭ�������
    path('EditBasicInfomation/RawStockCategory/', views.OperateData_rawstockcategory),
	path('EditBasicInfomation/RawStockCategory/add/', views.new_rawstockcategory),
    path('EditBasicInfomation/RawStockCategory/edit/', views.edit_rawstockcategory),
    path('EditBasicInfomation/RawStockCategory/delete/', views.del_rawstockcategory),
    # ����ϵͳ��Ļ�������
    path('EditBasicInfomation/CNCStatusCategory/', views.OperateData_cncstatuscategory),
	path('EditBasicInfomation/CNCStatusCategory/add/', views.new_cncstatuscategory),
    path('EditBasicInfomation/CNCStatusCategory/edit/', views.edit_cncstatuscategory),
    path('EditBasicInfomation/CNCStatusCategory/delete/', views.del_cncstatuscategory),
    # ��Ʒ���
    path('EditBasicInfomation/ProductCategory/', views.OperateData_lamproductcategory),
	path('EditBasicInfomation/ProductCategory/add/', views.new_lamproductcategory),
    path('EditBasicInfomation/ProductCategory/edit/', views.edit_lamproductcategory),
    path('EditBasicInfomation/ProductCategory/delete/', views.del_lamproductcategory),
    # �������
    path('EditBasicInfomation/LAMProductSubarea/', views.OperateData_lamproductsubarea),
	path('EditBasicInfomation/LAMProductSubarea/add/', views.new_lamproductsubarea),
    path('EditBasicInfomation/LAMProductSubarea/edit/', views.edit_lamproductsubarea),
    path('EditBasicInfomation/LAMProductSubarea/delete/', views.del_lamproductsubarea),
    # ����ʶ��
    path('EditBasicInfomation/Chi_Characters/', views.OperateData_chicharacters),
    re_path('EditBasicInfomation/Chi_Characters/media/PDFCode/OriginalImage/(?P<ImageFileName>(.+))', query_views.queryData_GetChicharactersImg),
	# path('EditBasicInfomation/Chi_Characters/add/', views.new_chicharacters),
    path('EditBasicInfomation/Chi_Characters/edit/', views.edit_chicharacters),
    # path('EditBasicInfomation/Chi_Characters/delete/', views.del_chicharacters),
    # ������ι����ļ�
    path('EditBasicInfomation/LAMTechniqueInstruction/', views.OperateData_lamtechniqueinstruction),
	path('EditBasicInfomation/LAMTechniqueInstruction/add/', views.new_lamtechniqueinstruction),
    path('EditBasicInfomation/LAMTechniqueInstruction/edit/', views.edit_lamtechniqueinstruction),
    path('EditBasicInfomation/LAMTechniqueInstruction/delete/', views.del_lamtechniqueinstruction),
    # re_path('QueryData/InspectLAMProcessRecords/Complete/(?P<MissionItemID>(.+))/$',
    #         query_views.queryData_Inspect_Complete_MissionLAMProcessRecords),
    
    # ������ι����ļ����Ʒ���Ĺ���
    path('EditBasicInfomation/LAMProdCate_TechInst/', views.OperateData_lamprodcate_techinst),
	path('EditBasicInfomation/LAMProdCate_TechInst/add/', views.new_lamprodcate_techinst),
    path('EditBasicInfomation/LAMProdCate_TechInst/edit/', views.edit_lamprodcate_techinst),
    path('EditBasicInfomation/LAMProdCate_TechInst/delete/', views.del_lamprodcate_techinst),
    # ��������
    path('EditBasicInfomation/LAMProductionWorkType/', views.OperateData_lamproductionworktype),
	path('EditBasicInfomation/LAMProductionWorkType/add/', views.new_lamproductionworktype),
    path('EditBasicInfomation/LAMProductionWorkType/edit/', views.edit_lamproductionworktype),
    path('EditBasicInfomation/LAMProductionWorkType/delete/', views.del_lamproductionworktype),

    # ��������ʵ��
    path('EditBasicInfomation/LAMTechInstSerial/', views.OperateData_lamtechinstserial),
    path('EditBasicInfomation/LAMTechInstSerial/add/', views.new_lamtechinstserial),
    path('EditBasicInfomation/LAMTechInstSerial/edit/', views.edit_lamtechinstserial),
    path('EditBasicInfomation/LAMTechInstSerial/delete/', views.del_lamtechinstserial),
    # ����ʵ�� PDF����
    path('EditBasicInfomation/New_LAMTechInstSerial_By_PDF/', views.new_lamtechinstserial_by_pdf),
    # �ϴ��ļ��������󷵻ؽ��
    path('EditBasicInfomation/New_LAMTechInstSerial_By_PDF/UploadFile/', views.new_lamtechinstserial_upload_pdf),
    # ����pdf�еĹ�����Ϣ
    path('EditBasicInfomation/New_LAMTechInstSerial_By_PDF/SavePDF/', views.new_lamtechinstserial_save_pdf),
    # ��ѯPDFʶ�����
    re_path('QueryData/ProgressBarValue/New_LAMTechInstSerial_UploadPDFFile_By_TechInstID/(?P<TechInstID>(.+))/$',
            query_views.queryData_ProgressBarValue_New_LAMTechInstSerial_UploadPDFFile_By_TechInstID),
    

    # ���ղ�����
    path('EditBasicInfomation/LAMProcessParameters/', views.OperateData_lamprocessparameters),
    path('EditBasicInfomation/LAMProcessParameters/delete/', views.del_lamprocessparameters),
    # ���Ӽ�����β�����
    re_path('EditBasicInfomation/LAMProcessParameters/AddLAMParameter/$',
                views.new_lamprocessparameters),
    # �༭������β�����
    re_path('EditBasicInfomation/LAMProcessParameters/EditLAMParameter/(?P<ProcessParameterItemID>(.+))/$',
                views.edit_lamprocessparameters),

    # ���Ӳ���������Ԫ
    re_path('EditBasicInfomation/LAMProcessParameters/AddConditionalCell/(?P<ProcessParameterItemID>(.+))/$',
                views.new_lamprocessparameterConditionalCell),
    # �༭����������Ԫ
    re_path('EditBasicInfomation/LAMProcessParameters/EditConditionalCell/(?P<ConditionalCellItemID>(.+))/$',
                views.edit_lamprocessparameterConditionalCell),

    # �༭�����ۼӵ�Ԫ
    re_path('EditBasicInfomation/LAMProcessParameters/EditAccumulateCell/(?P<ProcessParameterItemID>(.+))/$',
                views.edit_lamprocessparameterAccumulateCell),

    # �������õĹ���
    re_path('EditBasicInfomation/LAMProcessParameters/SaveTechInstSerial/$',
                views.save_lamprocessparameterTechInstSerial),



    # ȡ����λ
    path('EditBasicInfomation/SamplingPosition/', views.OperateData_samplingposition),
	path('EditBasicInfomation/SamplingPosition/add/', views.new_samplingposition),
    path('EditBasicInfomation/SamplingPosition/edit/', views.edit_samplingposition),
    path('EditBasicInfomation/SamplingPosition/delete/', views.del_samplingposition),

	# ȡ������
    path('EditBasicInfomation/SamplingDirection/', views.OperateData_samplingdirection),
	path('EditBasicInfomation/SamplingDirection/add/', views.new_samplingdirection),
    path('EditBasicInfomation/SamplingDirection/edit/', views.edit_samplingdirection),
    path('EditBasicInfomation/SamplingDirection/delete/', views.del_samplingdirection),

	# �ȴ���״̬
    path('EditBasicInfomation/HeatTreatmentState/', views.OperateData_heattreatmentstate),
	path('EditBasicInfomation/HeatTreatmentState/add/', views.new_heattreatmentstate),
    path('EditBasicInfomation/HeatTreatmentState/edit/', views.edit_heattreatmentstate),
    path('EditBasicInfomation/HeatTreatmentState/delete/', views.del_heattreatmentstate),
    
    # ��е�ӹ�״̬
    path('EditBasicInfomation/MachiningState/', views.OperateData_machiningstate),
	path('EditBasicInfomation/MachiningState/add/', views.new_machiningstate),
    path('EditBasicInfomation/MachiningState/edit/', views.edit_machiningstate),
    path('EditBasicInfomation/MachiningState/delete/', views.del_machiningstate),

    # ��Ʒʵ��
    path('ProcessRecords/LAMProduct/', views.OperateData_lamproduct),
	path('ProcessRecords/LAMProduct/add/', views.new_lamproduct),
    path('ProcessRecords/LAMProduct/edit/', views.edit_lamproduct),
    path('ProcessRecords/LAMProduct/delete/', views.del_lamproduct),
    # ��������
    path('ProcessRecords/LAMProcessMission/', views.OperateData_lamprocessmission),
    path('ProcessRecords/LAMProcessMission/add/', views.new_lamprocessmission),
    path('ProcessRecords/LAMProcessMission/finish/', views.finish_lamprocessmission),
    path('ProcessRecords/LAMProcessMission/delete/', views.del_lamprocessmission),
    # �����������б��ѯ��ѡ����
    re_path('QueryData/LAMTechInstSerial_LAM_By_ProductCodeList/(?P<ProductIDList>(.+))/$', query_views.queryData_LAMSerial_By_ProductIDList),

    # ���������º󻮷�
    path('ProcessRecords/LAMProcessMission/CutRecordsByTime/', views.lamprocessmission_CutRecords_by_Time),

    # �������β���ҳ��
    #
    re_path('ProcessRecords/WorksectionOperate_by_id/(?P<WorksectionID>(.+))/$', views.lamprocess_worksection_operate),


    # ԭ����
    path('ProcessRecords/RawStock/', views.OperateData_rawstock),
    path('ProcessRecords/RawStock/add/', views.new_rawstock),
    path('ProcessRecords/RawStock/edit/', views.edit_rawstock),
    path('ProcessRecords/RawStock/delete/', views.del_rawstock),

    # ԭ���Ϸ��Ż���
    path('ProcessRecords/RawStockFlow/', views.rawstockflow),
    path('ProcessRecords/RawStockFlow/send/', views.send_rawstockflow),
    # path('ProcessRecords/RawStockFlow/AddSendAddition/(?P<RawStockFlowItemID>(.+))/$', views.new_sendaddition_rawstockflow),
    re_path('ProcessRecords/RawStockFlow/AddSendAddition/(?P<RawStockFlowItemID>(.+))/$', views.new_sendaddition_rawstockflow),
    re_path('ProcessRecords/RawStockFlow/EditSendAddition/(?P<RawStockSendAdditionItemID>(.+))/$', views.edit_sendaddition_rawstockflow),
    path('ProcessRecords/RawStockFlow/retrieve/', views.retrieve_rawstockflow),
    path('ProcessRecords/RawStockFlow/edit/', views.edit_rawstockflow),
    path('ProcessRecords/RawStockFlow/delete/', views.del_rawstockflow),
    
    # ԭ���Ϸ��Ż���ͳ��
    path('ProcessRecords/RawStockFlowStatistic/', views.rawstockflow_statistic),
    re_path('QueryData/Statistic/RawStockFlow/$', query_views.queryData_Statistic_RawStockFlow),


    # ��������ֳ�
    # path('ProcessRecords/WorkSectionOperation/', views.worksection_operation),


    # �����¼
    path('InspectionRecords/ProcessMissionInspection/LAMProcess/', views.BrowseData_MissionLAMProcessInspection),
    # ��������
    re_path('InspectionRecords/ProcessMissionInspection/LAMProcess/ByMissionID/(?P<MissionItemID>(.+))/$',views.Inspect_MissionLAMProcessInspection),

    # ��Ʒ�����
    path('InspectionRecords/PhysicochemicalTest/Product/', views.OperateData_ProductPhyChemTest),
    path('InspectionRecords/PhysicochemicalTest/Product/add/', views.new_ProductPhyChemTest),
    path('InspectionRecords/PhysicochemicalTest/Product/edit/', views.edit_ProductPhyChemTest),

    # ԭ���������
    path('InspectionRecords/PhysicochemicalTest/RawStock/', views.OperateData_RawStockPhyChemTest),
    path('InspectionRecords/PhysicochemicalTest/RawStock/add/', views.new_RawStockPhyChemTest),
    path('InspectionRecords/PhysicochemicalTest/RawStock/edit/', views.edit_RawStockPhyChemTest),
    
    # ��Ʒ������
    path('InspectionRecords/NonDestructiveTest/Product/', views.OperateData_ProductNonDestructiveTest),
    path('InspectionRecords/NonDestructiveTest/Product/add/', views.new_ProductNonDestructiveTest),
    path('InspectionRecords/NonDestructiveTest/Product/edit/', views.edit_ProductNonDestructiveTest),

    # ԭ����������
    path('InspectionRecords/NonDestructiveTest/RawStock/', views.OperateData_RawStockNonDestructiveTest),
    path('InspectionRecords/NonDestructiveTest/RawStock/add/', views.new_RawStockNonDestructiveTest),
    path('InspectionRecords/NonDestructiveTest/RawStock/edit/', views.edit_RawStockNonDestructiveTest),

    # �����������б��ѯ��ѡ���鹤��
    re_path('QueryData/LAMTechInstSerial_Test_By_ProductList/(?P<ProductIDList>(.+))/$', query_views.queryData_TESTSerial_By_ProductIDList),
    # re_path('QueryData/LAMTechInstSerial_Test_By_RawStockList/(?P<RawStockIDList>(.+))/$', query_views.queryData_TESTSerial_By_RawStockIDList),


    # �����μ�¼
    re_path('QueryData/InspectLAMProcessRecords/Complete/(?P<MissionItemID>(.+))/$', query_views.queryData_Inspect_Complete_MissionLAMProcessRecords),
    re_path('QueryData/ProgressBarValue/InspectionLAMRecords_By_MissionID/(?P<MissionID>(.+))/$',
            query_views.queryData_ProgressBarValue_InspectionLAMRecords_By_MissionID),

    # ������ɸѡ����
    re_path('AnalyseLAMProcess/MissionFilter/(?P<AnalyseType>(.+))/$', views.AnalyseLAMProcess_MissionFilter),
    # ���������������-���θ߶�
    re_path('AnalyseLAMProcess/ZValue/$', views.AnalyseLAMProcess_ZValue),
    re_path('QueryData/AnalyseLAMProcess_ZValue/$', query_views.queryData_Analysedata_Zvalue_By_MissionIDList),
    re_path('QueryData/ProgressBarValue/Analyse_ZValue_By_MissionIDList/$', query_views.queryData_ProgressBarValue_Analyse_ZValue_By_MissionIDList),
    # ���������������-�ۼ�����
    re_path('AnalyseLAMProcess/AccumulateData/$', views.AnalyseLAMProcess_AccumulateData),
    re_path('QueryData/AnalyseLAMProcess_AccumulateData/$', query_views.queryData_Analysedata_AccumulateData_By_MissionIDList),
    # ���������������-���ڷ���
    re_path('AnalyseLAMProcess/LayerData/$', views.AnalyseLAMProcess_LayerData),
    re_path('QueryData/AnalyseLAMProcess_LayerData/$', query_views.queryData_Analysedata_LayerData_By_MissionIDList),
    # ���������������-˲ʱ���ʿռ�ֲ�
    re_path('AnalyseLAMProcess/ScanningRate3D/$', views.AnalyseLAMProcess_ScanningRate3D),
    re_path('QueryData/AnalyseLAMProcess_ScanningRate3D/$', query_views.queryData_Analysedata_ScanningRate3D_By_MissionIDList),
    # ���������־�ϴ� - ����
    re_path('AnalyseLAMProcess/DingDingRecords/Upload/$', views.AnalyseLAMProcess_DingDingRecords_Upload),
    # ���������־��� - ����
    re_path('AnalyseLAMProcess/DingDingRecords/Browse/$', views.AnalyseLAMProcess_DingDingRecords_Browse),
    re_path('QueryData/AnalyseLAMProcess/DingDingRecords_by_ID/(?P<RecordID>(.+))/$',
            query_views.queryData_GetDingDingRecordsByID),
    re_path('QueryData/AnalyseLAMProcess/DingDingRecordPictures_by_ID/(?P<PictureID>(.+))/$',
            query_views.queryData_GetDingDingRecordPicturesByID),

    # �����Ӵ���
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
    
    re_path('InspectionRecords/NonDestructiveTest/AddUTDefect/(?P<MissionItemID>(.+))/$',
            views.NonDestructiveTest_AddUTDefect),
    re_path('InspectionRecords/NonDestructiveTest/EditUTDefect/(?P<UTDefectID>(.+))/$',
            views.NonDestructiveTest_EditUTDefect),
    re_path('InspectionRecords/NonDestructiveTest/AddRTDefect/(?P<MissionItemID>(.+))/$',
            views.NonDestructiveTest_AddRTDefect),
    re_path('InspectionRecords/NonDestructiveTest/EditRTDefect/(?P<RTDefectID>(.+))/$',
            views.NonDestructiveTest_EditRTDefect),
    re_path('InspectionRecords/NonDestructiveTest/AddPTDefect/(?P<MissionItemID>(.+))/$',
            views.NonDestructiveTest_AddPTDefect),
    re_path('InspectionRecords/NonDestructiveTest/EditPTDefect/(?P<PTDefectID>(.+))/$',
            views.NonDestructiveTest_EditPTDefect),
    re_path('InspectionRecords/NonDestructiveTest/AddMTDefect/(?P<MissionItemID>(.+))/$',
            views.NonDestructiveTest_AddMTDefect),
    re_path('InspectionRecords/NonDestructiveTest/EditMTDefect/(?P<MTDefectID>(.+))/$',
            views.NonDestructiveTest_EditMTDefect),
    re_path('QueryData/NonDestructiveTest/DefectPicture_by_Defect/(?P<DefectPictureID>(.+))/$',
            query_views.queryData_GetDefectPicture),
    
    re_path('PicturesViewer/NonDestructiveTest/UTDefect/(?P<UTDefectID>(.+))/$',
            views.ViewUTDefectPictures),
    re_path('PicturesViewer/NonDestructiveTest/RTDefect/(?P<RTDefectID>(.+))/$',
            views.ViewRTDefectPictures),
    re_path('PicturesViewer/NonDestructiveTest/PTDefect/(?P<PTDefectID>(.+))/$',
            views.ViewPTDefectPictures),
    re_path('PicturesViewer/NonDestructiveTest/MTDefect/(?P<MTDefectID>(.+))/$',
            views.ViewMTDefectPictures),
    re_path('PicturesViewer/NonDestructiveTest/AllUTDefect/(?P<MissionItemID>(.+))/$',
            views.ViewAllUTDefectPictures),
    re_path('PicturesViewer/NonDestructiveTest/AllRTDefect/(?P<MissionItemID>(.+))/$',
            views.ViewAllRTDefectPictures),
    re_path('PicturesViewer/NonDestructiveTest/AllPTDefect/(?P<MissionItemID>(.+))/$',
            views.ViewAllPTDefectPictures),
    re_path('PicturesViewer/NonDestructiveTest/AllMTDefect/(?P<MissionItemID>(.+))/$',
            views.ViewAllMTDefectPictures),
    
    # ���С����
    path('PracticalTools/ThisMonthPassword/', views.PracticalTools_ThisMonthPassword),
    # ��λ�����ϴ��ѳ��εķֿ��������
    path('PracticalTools/BreakBlockResumption/', views.PracticalTools_BreakBlockResumption),
    # ����ӹ��ֲ�������
    path('PracticalTools/SShapeBreak/', views.PracticalTools_SShapeBreak),
    re_path('QueryData/ProgressBarValue/PracticalTools_SShapeBreak_By_GUID/(?P<GUID>(.+))/$',
            query_views.queryData_ProgressBarValue_PracticalTools_SShapeBreak_By_GUID),
    re_path('QueryData/ProgressBarValue/PracticalTools_BreakBlockResumption_By_GUID/(?P<GUID>(.+))/$',
            query_views.queryData_ProgressBarValue_PracticalTools_BreakBlockResumption_By_GUID),
    # ����������β��ṩ����
    path('PracticalTools/MakeMainProgramFile_8070/', views.PracticalTools_MakeMainProgramFile_8070),
    #     �����ṹ  �����Ӵ�
    re_path('PracticalTools/MakeMainProgramFile_8070/addStructure/(?P<StructureCode>(.+))/$', views.PracticalTools_MakeMainProgramFile_8070_AddStructure),
    #     �༭�ṹ  �����Ӵ�
    re_path('PracticalTools/MakeMainProgramFile_8070/editStructure/(?P<StructureCode>(.+))/(?P<StructureID>(.+))/$', views.PracticalTools_MakeMainProgramFile_8070_EditStructure),
    #     �ύ���ݣ�����G���� �����Ӵ�
    path('PracticalTools/MakeMainProgramFile_8070/MakeCode/', views.PracticalTools_MakeMainProgramFile_8070_MakeCode),
    # /LAMProcessData/PracticalTools/MakeMainProgramFile/addStructure/

    # �����ļ�
    re_path('DownLoadTempFile/(?P<tempfilepath>(.+))/$',
            views.download_template),

    # axjx��ѯURL
    re_path('QueryData/PreviewTable/LAMTechniqueInstruction/(?P<TechInstID>(.+))/$',
            query_views.queryData_LAMTechInst_Preview),
    re_path('QueryData/PreviewTable/LAMTechniqueInstruction_SerialDetails/(?P<TechInstID>(.+))/$',
            query_views.queryData_LAMTechInst_SerialDetails),
    # ���������������  ����Ԥ��
    re_path('QueryData/PreviewTable/LAMProductMission/(?P<ProductIDList>(.+))/$',
            query_views.queryData_LAMProductMission_Preview),

    # ��Ʒ��������������  ����Ԥ��
    re_path('QueryData/PreviewTable/ProductPhyChemTestMission/(?P<ProductIDList>(.+))/$',
            query_views.queryData_ProductPhyChemTestMission_Preview),
    re_path('QueryData/PreviewTable/RawStockPhyChemTestMission/(?P<RawStockID>(.+))/$',
            query_views.queryData_RawStockPhyChemTestMission_Preview),
    
    re_path('QueryData/PreviewTable/ProductNonDestructiveTestMission/(?P<ProductID>(.+))/$',
            query_views.queryData_ProductNonDestructiveTestMission_Preview),
    re_path('QueryData/PreviewTable/RawStockNonDestructiveTestMission/(?P<RawStockID>(.+))/$',
            query_views.queryData_RawStockNonDestructiveTestMission_Preview),

    # re_path('QueryData/LAMTechniqueInstruction_By_ProductCategory/(?P<ProductCategoryID>(.+))/$',
    #         query_views.queryData_LAMTechInst_By_ProdCate),

    # ���ݲ�����ID��ѯ������������Ԫ
    re_path('QueryData/LAMProcessParameterConditionalCell_By_ProcessParameterID/(?P<ProcessParameterID>(.+))/$',
            query_views.queryData_LAMProcessParameterConditionalCell),

    # ���ݲ�����ID��ѯ�������ۼӵ�Ԫ
    re_path('QueryData/LAMProcessParameterAccumulateCell_By_ProcessParameterID/(?P<ProcessParameterID>(.+))/$',
            query_views.queryData_LAMProcessParameterAccumulateCell),

    # ���ݲ�����ID��ѯ���ù����б�
    re_path('QueryData/LAMProcessParameter_TechInstSerial_By_ProcessParameterID/(?P<ProcessParameterID>(.+))/$',
            query_views.queryData_LAMProcessParameterTechInstSerial),

    # �г����й���
    re_path('QueryData/LAMProcessParameter_TechInstSerial/$',
            query_views.queryData_LAMProcessParameterTechInstSerial_Refresh),


    
    
    # ���������Ų�ѯ���õĹ����ļ�
    re_path('QueryData/LAMTechniqueInstruction_By_ProductCode/(?P<ProductCode>(.+))/$',
            query_views.queryData_LAMTechInst_By_ProductCode),

    # �Թ����ļ�id��ѯ�ù����ļ����й���
    re_path('QueryData/WorkType_By_LAMTechInst/(?P<LAMTechInstID>(.+))/$',
            query_views.queryData_WorkType_By_LAMTechInst),

    # �Թ����ļ�id��ѯ�ù����ļ����пɱ��������ģ��ѡ��Ĺ���
    re_path('QueryData/WorkType_By_LAMTechInst_filter_LAM/(?P<LAMTechInstID>(.+))/$',
            query_views.queryData_WorkType_By_LAMTechInst_filter_LAM),

    # �Թ����ļ�id��ѯ�ù����ļ����пɱ�����ģ��ѡ��Ĺ���
    re_path('QueryData/WorkType_By_LAMTechInst_filter_PhyChemTest/(?P<LAMTechInstID>(.+))/$',
            query_views.queryData_WorkType_By_LAMTechInst_filter_PhyChemTest),

    # �Թ����ļ�id��ѯ�ù����ļ����пɱ��ⷿģ��ѡ��Ĺ���
    re_path('QueryData/WorkType_By_LAMTechInst_filter_RawStockSendRetrieve/(?P<LAMTechInstID>(.+))/$',
            query_views.queryData_WorkType_By_LAMTechInst_filter_RawStockSendRetrieve),

    # ��������Ͳ�ѯ��Ʒ�б�
    re_path('QueryData/Product_By_ProductCategory/(?P<ProductCategoryID>(.+))/$',
            query_views.queryData_Product_By_ProductCategory),

    # �������Ų�ѯ���id
    re_path('QueryData/ProductID_By_ProductCode/(?P<ProductCode>(.+))/$',
            query_views.queryData_ProductID_By_ProductCode),

    # ��ԭ�������Ų�ѯԭ����id
    re_path('QueryData/RawStockID_By_RawStockBatchNumber/(?P<RawStockBatchNumber>(.+))/$',
            query_views.queryData_RawStockID_By_RawStockBatchNumber),
    # ������id��ѯ����id
    re_path('QueryData/WorksectionId_By_MissionID/(?P<MissionID>(.+))/$',
            query_views.queryData_WorksectionId_By_MissionID),

    # ������id��ѯ�Ƿ������ֹʱ��
    re_path('QueryData/StartFinishTime_IfExists_By_MissionID/(?P<MissionID>(.+))/$',
            query_views.queryData_StartFinishTime_IfExists_By_MissionID),
    
    # ������id List��ѯ�Ƿ������ֹʱ��
    re_path('QueryData/StartFinishTime_IfExists_By_MissionIDList/(?P<MissionIDList>(.+))/$',
            query_views.queryData_StartFinishTime_IfExists_By_MissionIDList),
    
    # ������id��ѯ�Ѵ��ڵ���ֹʱ�䣨���У�
    re_path('QueryData/StartFinishTime_By_MissionID/(?P<MissionID>(.+))/$',
            query_views.queryData_StartFinishTime_By_MissionID),

	# ������id��ѯ�´���������
    re_path('QueryData/ArrangementDate_By_MissionID/(?P<MissionID>(.+))/$',
            query_views.queryData_ArrangementDate_By_MissionID),

	# �������Ų�ѯ�����б�
	re_path('QueryData/Mission_By_ProductCode/(?P<ProductCode>(.+))/$',
            query_views.queryData_Mission_By_ProductCode),

    # �Թ���id����ֹʱ�䡢ʱ������ѯ����������
    re_path('QueryData/Oxydata_By_WorkSectionDatetime/(?P<WorksectionID>(.+))/(?P<StartDateTime>(.+))/(?P<FinishDateTime>(.+))/(?P<Interval>(.+))/$',
            query_views.queryData_Oxydata_By_WorkSectionDatetime),
    # �Թ���id����ֹʱ�䡢ʱ������ѯ���⹦������
    re_path('QueryData/Laserdata_By_WorkSectionDatetime/(?P<WorksectionID>(.+))/(?P<StartDateTime>(.+))/(?P<FinishDateTime>(.+))/(?P<Interval>(.+))/$',
            query_views.queryData_Laserdata_By_WorkSectionDatetime),

    # �Թ���id����ֹʱ�䡢ʱ������ѯ�����������⹦�ʡ�CNC-Z����
    re_path('QueryData/Data_By_WorkSectionDatetime/(?P<ifForceRefresh>(.+))/(?P<WorksectionID>(.+))/(?P<StartDateTime>(.+))/(?P<FinishDateTime>(.+))/(?P<Interval>(.+))/$',
            query_views.queryData_data_By_WorkSectionDatetime),

    # ������id����ֹʱ�䡢ʱ������ѯ����������
    re_path(
        'QueryData/Oxydata_By_MissionDatetime/(?P<MissionID>(.+))/(?P<StartDateTime>(.+))/(?P<FinishDateTime>(.+))/(?P<Interval>(.+))/$',
        query_views.queryData_Oxydata_By_MissionDatetime),

    # �Թ���id����ֹʱ�䡢ʱ������ѯCNC-Z����
    # re_path('QueryData/Laserdata_By_WorkSectionDatetime/(?P<Worksection>(.+))/(?P<StartTime>(.+))/(?P<FinishTime>(.+))/interval/$',
    #         query_views.queryData_Laserdata_By_WorkSectionDatetime),

    # ��MissionID��ѯFindData�м�¼���� ͼ����ʾ graph
    re_path('QueryData/FineData_By_MissionID/(?P<MissionItemID>(.+))/(?P<DateStr>(.+))/(?P<HourStr>(.+))/$',
            query_views.queryData_finedata_By_MissionID),
    # ��MissionID��ѯFindData�м�¼����
    re_path('QueryData/FineData_By_MissionID_Datetime/(?P<MissionItemID>(.+))/(?P<startTimestamp>(.+))/(?P<finishTimestamp>(.+))/$',
            query_views.queryData_finedata_By_MissionID_timestamp),

    # �Թ���id��ѯ���¸�������ʱ��
    re_path(
        'QueryData/RecordLastTime_by_WorksectionID/(?P<WorksectionID>(.+))/$', query_views.queryData_RecordLastTime_by_WorksectionID),
    # �Թ���id��ѯʵʱ����
    re_path(
        'QueryData/RealTimeRecord_by_WorksectionID/(?P<WorksectionID>(.+))/$',
        query_views.queryData_RealTimeRecord_by_WorksectionID),




    # analyse ����������ι��̲���
    # --��ȡCNC���ػ���������Ϣ����
    re_path('QueryData/CNCData/DownloadScreenInfo/', query_views.DownloadCNCScreenInfo),
    # --��ȡCNC���ػ��������ͼ
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


