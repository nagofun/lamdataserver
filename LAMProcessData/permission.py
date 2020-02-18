# -*- coding: gbk -*-
from django.shortcuts import render
from LAMProcessData import models
from django.db.models import Q
from django.urls import reverse   #�˷������Խ�url��ַת����url��name

def perm_check(request, *args, **kwargs):
    url_obj = reverse(request.path_info)
    url_name = url_obj.url_name
    perm_name = ''
    #Ȩ�ޱ����urlname���ʹ��
    if url_name:
        #��ȡ���󷽷������������
        url_method, url_args = request.method, request.GET
        url_args_list = []
        #������������ֵ�ö��Ÿ�������ַ�������Ϊ���ݿ������������
        for i in url_args:
            url_args_list.append(str(url_args[i]))
        url_args_list = ','.join(url_args_list)
        #�������ݿ�
        get_perm = models.Permission.objects.filter(Q(url=url_name) and Q(per_method=url_method) and Q(argument_list=url_args_list))
        if get_perm:
            for i in get_perm:
                perm_name = i.name
                perm_str = 'lamprocessdata.%s' % perm_name
                if request.user.has_perm(perm_str):
                    print('====��Ȩ����ƥ��')
                    return True
            else:
                print('---->Ȩ��û��ƥ��')
                return False
        else:
            return False
    else:
        return False   #û��Ȩ�����ã�Ĭ�ϲ��Ź�


def check_permission(fun):    #����һ��װ��������views��Ӧ��
    def wapper(request, *args, **kwargs):
        if perm_check(request, *args, **kwargs):  #���������Ȩ����֤����
            return fun(request, *args, **kwargs)
        return render(request, '403.html', locals())
    return wapper