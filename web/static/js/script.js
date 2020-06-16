piosk = {
    arr_status:["main","photograph","print","end"],
    map : {
        /* 
            setting -> main -> photograph -> print -> end
        */
        _status: 'setting',
        _templates : null,
        _current : null,
        _capture_number : 0,
        _reload_number : 0,
    },
    setTemplates : function(t){
        this.map._templates = t;
    },
    getTemplates : function(inx){
        if (inx != undefined){
            return this.map._templates[inx];
        }else{
            return this.map._templates;
        }
    },
    setCurrent : function(index,pos){

        for(var i=0,len=this.map._templates.length;i<len;i++){
            if(i == index){
                let tmp = this.map._templates[i];
                this.map._current = tmp[pos];
                break;
            }
        }
    },
    getCurrent : function(){
        return this.map._current;
    },
    getStatus: function(){
        return this.map._status;
    },
    goNext: function(){
        console.log("goNext");
        let inx = this.arr_status.indexOf(this.map._status);
        
        if(this.map._status == 'setting'){
            this.map._status = "main";
        }else if(this.map._status == 'end'){
            this.map._status = "main";
        }else{
            this.map._status = this.arr_status[inx+1];
        }
    },
    goPrev: function(){
        let inx = this.arr_status.indexOf(this.map._status);
        if(inx > 0){
            this.map._status = this.arr_status[inx-1];
        }else{
            this.map._status = "main";
        }
    },
    goHome: function(){
        this.map._status = "main";
    },
    getCapturedNumber: function(){
        return this.map._capture_number;
    },
    addCaptureNumber:function(){
        if(this.map._capture_number < this.map._current.capture_count) {
            this.map._capture_number += 1;
            this.map._reload_number = this.map._capture_number -1 ;
        }
    },
    backCaptureNumber:function(){
        if(this.map._capture_number > 0){
            this.map._capture_number -= 1;
            this.map._reload_number = this.map._capture_number;
        }
    },
    reloadCaptureNumber:function(){
        this.map._capture_number = this.map._reload_number;
    },
    doInit: function(){
        this.map._status = 'main';
        this.map._current = null;
        this.map._capture_number = 0;
        this.map._reload_number = 0;
    }

}

/* ========
Debugger plugin, simple demo plugin to console.log some of callbacks
======== */
var activeIndex = 0
var myPlugin = {
    name: 'debugger',
    params: {
        debugger: false,
    },
    on: {
        slideChange: function () {
            activeIndex = this.activeIndex;
            console.log('slideChange', this.previousIndex, '->', this.activeIndex);
        },
        slideChangeTransitionStart: function () {
        console.log('slideChangeTransitionStart');
        },
        slideChangeTransitionEnd: function () {
        console.log('slideChangeTransitionEnd');
        },
    },
};