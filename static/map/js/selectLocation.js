
var SelectLocation = {

    init:function(config){
        var eleId = config.id;
        var mapUrl = config.url;
        var winHeight = config.height || 800;
        var winWidth = config.width || 1024;
        var winTop = config.top || 50;
        var winLeft = config.left || 100;
        this.callbackFun = config.callback;

        if(!eleId){
            alert('元素id不能为空');
            return;
        }

        if(!mapUrl){
            alert('地图url不能为空');
            return;
        }

        var ele = document.getElementById(eleId);
        ele.addEventListener('click',function(){
            window.open(mapUrl,'selectLocation','fullscreen=0,directories=0,location=0,menubar=0,resizable=0,scrollbars=0,status=0,titlebar=0,toolbar=0,' +
                'height='+winHeight+',width='+winWidth+',top='+winTop+',left='+winLeft+'');
        });
    },

    callbackFun:null,

    selectCallback:function(selectedLocation){
        if(this.callbackFun){
            this.callbackFun(selectedLocation);
        }
    }
}