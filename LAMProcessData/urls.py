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
    path('LAMProcessData/UpdateRecordToFineData/', views.Update_ExistingData_to_FineData),
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
    # ������ι����ļ�
    path('EditBasicInfomation/LAMTechniqueInstruction/', views.OperateData_lamtechniqueinstruction),
	path('EditBasicInfomation/LAMTechniqueInstruction/add/', views.new_lamtechniqueinstruction),
    path('EditBasicInfomation/LAMTechniqueInstruction/edit/', views.edit_lamtechniqueinstruction),
    path('EditBasicInfomation/LAMTechniqueInstruction/delete/', views.del_lamtechniqueinstruction),
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
    path('ProcessRecords/RawStockFlow/retrieve/', views.retrieve_rawstockflow),
    path('ProcessRecords/RawStockFlow/edit/', views.edit_rawstockflow),
    path('ProcessRecords/RawStockFlow/delete/', views.del_rawstockflow),


    # ��������ֳ�
    # path('ProcessRecords/WorkSectionOperation/', views.worksection_operation),


    # �����¼
    path('InspectionRecords/ProcessMissionInspection/LAMProcess/', views.BrowseData_MissionLAMProcessInspection),
    # ��������
    re_path('InspectionRecords/ProcessMissionInspection/LAMProcess/ByMissionID/(?P<MissionItemID>(.+))/$',views.Inspect_MissionLAMProcessInspection),


    path('InspectionRecords/PhysicochemicalTest/Product/', views.OperateData_ProductPhyChemTest),
    path('InspectionRecords/PhysicochemicalTest/Product/add/', views.new_ProductPhyChemTest),
    path('InspectionRecords/PhysicochemicalTest/Product/edit/', views.edit_ProductPhyChemTest),

    path('InspectionRecords/PhysicochemicalTest/RawStock/', views.OperateData_RawStockPhyChemTest),
    path('InspectionRecords/PhysicochemicalTest/RawStock/add/', views.new_RawStockPhyChemTest),
    path('InspectionRecords/PhysicochemicalTest/RawStock/edit/', views.edit_RawStockPhyChemTest),

    # �����μ�¼
    re_path('QueryData/InspectLAMProcessRecords/Complete/(?P<MissionItemID>(.+))/$', query_views.queryData_Inspect_Complete_MissionLAMProcessRecords),
    re_path('QueryData/ProgressBarValue/InspectionLAMRecords_By_MissionID/(?P<MissionID>(.+))/$',
            query_views.queryData_ProgressBarValue_InspectionLAMRecords_By_MissionID),

    # ������ɸѡ����
    re_path('AnalyseLAMProcess/MissionFilter/(?P<AnalyseType>(.+))/$', views.AnalyseLAMProcess_MissionFilter),
    # ���������������-���θ߶�
    re_path('AnalyseLAMProcess/ZValue/$', views.AnalyseLAMProcess_ZValue),
    # ���������������-���θ߶�
    re_path('AnalyseLAMProcess/AccumulateData/$', views.AnalyseLAMProcess_AccumulateData),
    # ���������������-���θ߶�
    re_path('AnalyseLAMProcess/LayerData/$', views.AnalyseLAMProcess_LayerData),



    # �����Ӵ���
    re_path('InspectionRecords/PhysicochemicalTest/AddTensile/(?P<MissionItemID>(.+))/$',
            views.PhyChemTest_AddTensile),
    re_path('InspectionRecords/PhysicochemicalTest/EditTensile/(?P<TensileID>(.+))/$',
            views.PhyChemTest_EditTensile),
    re_path('InspectionRecords/PhysicochemicalTest/AddToughness/(?P<MissionItemID>(.+))/$',
            views.PhyChemTest_AddToughness),
    re_path('InspectionRecords/PhysicochemicalTest/EditToughness/(?P<ToughnessID>(.+))/$',
            views.PhyChemTest_EditToughness),
    re_path('InspectionRecords/PhysicochemicalTest/AddChemicalElement/(?P<MissionItemID>(.+))/(?P<IfProductTest>(.+))/$',
            views.PhyChemTest_AddChemicalElement),
    re_path('InspectionRecords/PhysicochemicalTest/EditChemicalElement/(?P<MissionItemID>(.+))/(?P<ChemicalItemID>(.+))/(?P<IfProductTest>(.+))/$',
            views.PhyChemTest_EditChemicalElement),





    # axjx��ѯURL
    re_path('QueryData/PreviewTable/LAMTechniqueInstruction/(?P<TechInstID>(.+))/$',
            query_views.queryData_LAMTechInst_Preview),
    re_path('QueryData/PreviewTable/LAMProductMission/(?P<ProductID>(.+))/$',
            query_views.queryData_LAMProductMission_Preview),


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

    # ��������Ͳ�ѯ��Ʒ�б�
    re_path('QueryData/Product_By_ProductCategory/(?P<ProductCategoryID>(.+))/$',
            query_views.queryData_Product_By_ProductCategory),

    # �������Ų�ѯ���id
    re_path('QueryData/ProductID_By_ProductCode/(?P<ProductCode>(.+))/$',
            query_views.queryData_ProductID_By_ProductCode),

    # ������id��ѯ����id
    re_path('QueryData/WorksectionId_By_MissionID/(?P<MissionID>(.+))/$',
            query_views.queryData_WorksectionId_By_MissionID),

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

# print('urls.py end')
