html1='''
<!doctype html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"> 
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
<title>SpiderMan</title>
<!-- 最新版本的 Bootstrap 核心 CSS 文件 -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

<!-- 可选的 Bootstrap 主题文件（一般不用引入） -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

<script src="http://libs.baidu.com/jquery/1.11.1/jquery.min.js"></script>
<!-- 最新的 Bootstrap 核心 JavaScript 文件 -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
<link rel="stylesheet" type="text/css" href="css/default.css" />

<!--必要样式-->
<link rel="stylesheet" type="text/css" href="css/search-form.css" />

</head>
<body style="background-color: rgb(1,1,1,.5);background-image:url('https://ss0.bdstatic.com/94oJfD_bAAcT8t7mm9GUKT-xh_/timg?image&quality=100&size=b4000_4000&sec=1574687295&di=e31749233fd0f2404e894ee6c6fc63b0&src=http://www.qqaiqin.com/uploads/allimg/131106/4-131106194540.jpg')">

<form onSubmit="submitFn(this, event);">
    <div class="search-wrapper">
        <div class="input-holder">
            <input type="text" class="search-input" placeholder="请输入关键词" />
            <button id='search-icon' class="search-icon" onClick="searchToggle(this, event);"><span></span></button>
        </div>
        <span class="close" onClick="searchToggle(this, event);"></span>
        
    </div>
    <div class="result-container" style="display: block;position:absolute;top:45%;left:31%;margin-botom:100px;">


            '''
html2='''
<div class="well well-lg" style="width: 630px;height: 215px;padding: 5px;margin-top:10px;">
                <div class="col-md-9" style="padding:0px;">
                    <div class="col-md-12">
                        <h3 style="color:rgb(1,1,1,1);">{name}</h3>
                        <div style="font-size:13px;color:rgba(123, 122, 122, 0.99)">{institution}</div>
                    </div>
                    <div class="col-md-12" style="margin-top:10px;">
                        <h4 style="color:rgb(1,1,1,1);">Skills and Expertise</h4>
                        <div style="font-size:13px;color:rgba(123, 122, 122, 0.99)">{expertise}</div>
                    </div>
                </div>
                <div class="col-md-3" style="padding:0px;"><img style="border-radius:300px;" src='{avatar}'></div>
                <div class="col-md-6" style="margin-top:15px;color:#0080FF;font-size: .875rem;"><a href="{follow}">Follow</a></div>
                <div class="col-md-6" style="margin-top:15px;color:#0080FF;font-size: .875rem;"><a href="{email}">Message</a></div>
            </div>
            

            '''

html3='''
        </div>
      </form>      

<script type="text/javascript">
function searchToggle(obj, evt){
    var container = $(obj).closest('.search-wrapper');

    if(!container.hasClass('active')){
          container.addClass('active');
          evt.preventDefault();
    }
    else if(container.hasClass('active') && $(obj).closest('.input-holder').length == 0){
          container.removeClass('active');
          // clear input
          container.find('.search-input').val('');
          // clear and hide result container when we press close
          $('.result-container').fadeOut(100, function(){$(this).empty();});
    }
}

function submitFn(obj, evt){
    value = $(obj).find('.search-input').val().trim();

    _html = "您搜索的关键词： ";
    if(!value.length){
        _html = "关键词不能为空!";
    }
    else{
        //_html += "<b>" + value + "</b>";
        query='?query='+value
        location.href=location.origin+'/'+encodeURI(query);
    }

    //$(obj).find('.result-container').html('<span>' + _html + '</span>');
    $(obj).find('.result-container').fadeIn(100);

    evt.preventDefault();
}
</script>

</body>
</html>
'''
