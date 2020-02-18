(function($){
    $.fn.extend({
        "wy_inselect":function(options){
            if(!isValid(options)) return this;
            var $Id = $(this);
            var last;
            $Id.find(".wyinput-drop").css("width",$(".wyinput-group input").outerWidth()+"px").hide();
            $Id.find(".wyinput-group input").keyup(function(event){
                last = event.timeStamp;
                setTimeout(function(){    //��ʱ�ӳ�0.5sִ��
                    if(last-event.timeStamp==0)
                    //���ʱ���Ϊ0��Ҳ������ֹͣ����0.5s֮�ڶ�û��������keyup�¼�������
                    {
                        var arr= searchIndex($Id,options);
                        loadDrop($Id,arr);
                    }
                },500);

            })
            $Id.find(".wyinput-drop").delegate(".drop-line a","click",function(){
                var html=$(this).html();
                console.log(html)
                $(this).parents(".wyinput-drop").siblings(".wyinput-group").find("input").val(html);
                $Id.find(".wyinput-drop").hide()
            })

        }
    })

    //�������Ƿ�Ϸ�
    function isValid(options){
        return !options || (options��&& typeof options === "object")?true:false;
    }

    //����������
    function loadDrop($Id,arr){
        var html = "";
        if(arr.length == 0){
            $Id.find(".wyinput-drop").hide().html("");
            return;
        }
        $.each(arr,function(idx,obj){
            html+='<p class="drop-line">' + '<a href="#">'+obj.name+'</a></p>';
        })
        $Id.find(".wyinput-drop").html(html).show();
    }

    //ģ����ѯ
    function searchIndex($Id,options){
        var $input = $Id.find(".wyinput-group input");
        var keywords = $input.val();
        var arr=[];
        if(keywords==""||keywords==" "){
            return arr;
        }
        $.each(options,function(idx,obj){
            if(obj.name.indexOf(keywords)>=0){
                arr.push({name:obj.name});
            }
        })
        console.log(arr);
        return arr;
    }

})(window.jQuery)