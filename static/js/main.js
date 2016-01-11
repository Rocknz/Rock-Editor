/**
 * Created by JungRockJoon on 2016. 1. 8..
 */
$(document).ready(function($){
    //$(".folder_layer").load("{% url 'folder' %}");
    $(".folder_layer").load("/folder/");
    $(".toggle_btn").click(function(){
        $btn = this;
        $str = $btn.getAttribute("value");
        $folder_layer = $(".folder_layer");
        $source_layer = $(".source_layer");
        $triangle = $(".triangle");
        if($str.localeCompare("close") == 0){
            $folder_layer.animate({height:"0%"},"fast",function(){
                $btn.setAttribute("value","open");
                $folder_layer.hide();
            });
            $triangle.css('borderBottomWidth','0px');
            $triangle.css('borderTopWidth','10px');
            $source_layer.animate({height:"100%"},"fast");
        }
        else if($str.localeCompare("open") == 0){
            $folder_layer.show();
            $autoHeight = $folder_layer.css('height', 'auto').height();
            $folder_layer.height(0);
            $folder_layer.stop().animate({ height: $autoHeight }, "fast",function(){
                $btn.setAttribute("value","close");
                $folder_layer.height("auto");
            });
            $triangle.css('borderBottomWidth','10px');
            $triangle.css('borderTopWidth','0px');
            $str = $source_layer.height() - $autoHeight;
            $source_layer.animate({height:$str},"fast",function(){
                resize_source();
            });
        }
    });
});

// source_layer resize.
function resize_source(){
    $folder = $(".folder_layer");
    $height = $folder.height().toString();
    $str = "100% - " + $folder.height().toString() + "px";
    $(".source_layer").height("calc("+$str+")");
}
// notification.
function notice($str){
    $notice_layer = $(".notice_layer");
    $notice_layer.html($str);
    $notice_layer.fadeIn();
    setTimeout(function g(){
        notice_delete($str)
    }, 3000);
}
function notice_delete($str){
    $notice_layer = $(".notice_layer");
    if($notice_layer.html().localeCompare($str) == 0){
        $notice_layer.fadeOut();
    }
}
// popup_layer.
function show_popup_layer(){
    $popup_layer = $(".popup_layer");
    $popup_layer.css("top","calc(40% - "+($popup_layer.height()/2.0)+"px)");
    $popup_layer.css("left","calc(50% - "+($popup_layer.width()/2.0)+"px)");
    $popup_layer.show();
}



/**
* Here is right click menu script
*/

// right_click event catch.
$(document).bind("contextmenu", function (event) {
    if ($(event.target).attr('class') != null) {
        var g = $(event.target).attr('class').split(' ');
        for (var i = 0; i < g.length; i++) {
            if (g[i].localeCompare('folder_button') == 0 || g[i].localeCompare('file_button') == 0) {
                $(".custom-menu").show().
                    css({top: event.pageY+"px", left: event.pageX+"px"})
                        .attr('link',$(event.target).attr('link'))
                        .attr('path',$(event.target).attr('path'));
            }
        }
    }
    event.preventDefault();
});

// right_click menu event catch.
$(document).bind("mousedown", function (e) {
    if(event.which == 1) {
        // If the clicked element is the menu
        // Hide it
        if ($(e.target).parents(".custom-menu").length > 0) {
            if ($(e.target).attr('value').localeCompare("Delete") == 0) {
                $now = $(e.target).parents(".custom-menu");
                $path = $now.attr('path');
                $delete_path = $now.attr('link');
                if($delete_path.localeCompare("null") != 0) {
                    $csrf_token = $(".csrf_token").attr("value");
                    $(".folder_layer").load("/folder/delete/", {
                        path: $path,
                        delete_path: $delete_path,
                        csrfmiddlewaretoken: $csrf_token
                    });
                }else{
                    notice("Not possible");
                }
            }
        }
        $(".custom-menu").hide(100);
    }
});
