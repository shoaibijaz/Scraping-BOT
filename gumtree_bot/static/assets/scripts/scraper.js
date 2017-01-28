(function ( $ ) {

    $.Scraper = function(options){
        var $this = $(this);

        var extract_ads_interval;

        var defaults = {
            logID:0,
            taskID:0,
            getScraperFormURL:'',
            scraperFormDIV:'',
            scraperForm:'',
            scraperPageURL:'',
            commentFormURL:'',
            commentFormDIV:'',
            commentForm:'',
        };

        var options = $.extend(defaults, options);

        var getScraperForm = function () {
            $.get(defaults.getScraperFormURL,{ id:defaults.logID },function (response) {
                $(defaults.scraperFormDIV).html(response);
                addBootstrapClass();
                initAjaxScraperForm();
                validateScraperForm();
                autoStartExtractAds();
            });
        };

        var initAjaxScraperForm = function () {

            $(defaults.scraperForm).ajaxForm({
                beforeSubmit:  function(){
                    createDIVLoader($(defaults.scraperFormDIV));
                },
                success: function(response){

                    var parsed = $.parseJSON(response);

                    notification("Searching ads completed.");
                    onSearchAdCompleted(parsed);
                    removeDIVLoader($(defaults.scraperFormDIV));
                },
                error:function () {
                    notification("error! failed to extract ads.");
                    removeDIVLoader($(defaults.scraperFormDIV));
                }
            });

        };

        var validateScraperForm = function () {
            $(defaults.scraperForm).validate({
                rules: {
                    website: "required",
                },
                messages: {
                    website: "Please select website.",
                }
            });
        };

        var addBootstrapClass = function () {
            $("select, input[type='text']").addClass('form-control');
        };

        var createDIVLoader= function (targetElement) {

            var src = '/static/assets/img/loader.gif';

            var dv  = $("<div />", { class:'loader' });
            var img = $("<img />", { src:src });

            dv.html(img);

            targetElement.find(".loader").remove();

            targetElement.css('position','relative');

            dv.css({width:targetElement.width(), height:targetElement.height()});

            targetElement.append(dv);
        };

        var removeDIVLoader= function (targetElement) {
            targetElement.find(".loader").remove();
            targetElement.css('position','none');
        };

        var onSearchAdCompleted = function (parsedResponse) {
            if(parsedResponse.status==200 && parsedResponse.data){
                var parsedInfo = $.parseJSON(parsedResponse.data);
                if(parsedInfo.log_id > 0 && parsedInfo.total_ads > 0){
                    window.location = defaults.scraperPageURL + parsedInfo.log_id;
                }
                else{
                    notification("No ad found.");
                    $("#id_ads").val(0);
                    $("#id_pages").val(0);
                    $("#lblAds").html(0);
                    $("#lblPages").html(0);
                }
            }

        };

        var isValidDataForExtract = function () {

            if($("#id_id").val() > 0 && $("#id_ads").val() > 0){
                return true;
            }
            else{
                notification("No ad found. Please search ads first.");
                return false;
            }
        };

        var createTask = function () {
            $.ajax({
                type: "GET",
                url: '/create_task',
                data: { id:defaults.logID },
                beforeSend:function () {
                    setButtonsStatus(true,true, 100);
                },
                success: function(response){
                    var parsed = $.parseJSON(response);
                    if(parsed.status == 200 && parsed.data && parsed.data > 0) {
                        window.location = defaults.scraperPageURL + defaults.logID + "?task=" + parsed.data+'#start'
                    }
                    else{
                        notification('Operation failed to extract data.');
                    }
                },
                error: function(){
                    setButtonsStatus(false,true, 100);
                    notification('Operation failed to extract data.');
                }
            });
        };

        var extractAds = function (){

            $.ajax({
                type: "GET",
                url: '/extract_ads',
                data:{ id:defaults.logID, task: defaults.taskID },
                beforeSend:function () {
                    setButtonsStatus(true,true, 5000);
                    extract_ads_interval = setInterval(function () {
                        $("#btnCancelExtractAds").attr('disabled', false);
                        getAds();

                    }, 5000);
                },
                success: function(response){

                    var parsed = $.parseJSON(response);

                    if(parsed.status == 200){
                        notification('Ads extracted successfully..')
                    }
                    else{
                        notification('Ads extraction process failed..');
                    }

                    clearInterval(extract_ads_interval);
                    extract_ads_interval = undefined;

                    setButtonsStatus(false,true, 100);
                },
                error: function(){
                    setButtonsStatus(false,true, 100);
                }
            });

        };

        var getAds = function () {


            $.ajax({
                type: "GET",
                url: '/get_ads_list',
                data: { id:defaults.taskID },
                beforeSend:function () {
                },
                success: function(response){
                    $("#adsListDiv").html(response)
                },
                error: function(){
                    notification('Operation failed to get ads.');
                }
            });
        };

        var setButtonsStatus = function(operation, cancel, waitFor){
            $(defaults.scraperForm).find('button').attr('disabled',operation);
            $("#btnCancelExtractAds").attr('disabled',cancel);
        };

        var stopExtractAds = function (){

            $.ajax({
                type: "GET",
                url: '/stop_extract_ads',
                data:{ id:defaults.logID, task:defaults.taskID },
                beforeSend:function () {
                },
                success: function(response){
                    var parsed = $.parseJSON(response);


                    var interval = setInterval(function () {
                        if(!extract_ads_interval){
                            notification('Operation stopped..');
                            setButtonsStatus(false,true, 100);
                            clearInterval(interval);
                        }
                    }, 100);

                },
                error: function(){
                    setButtonsStatus(false,true, 100);
                }
            });

        };

        var autoStartExtractAds = function () {

            if(defaults.logID > 0 && defaults.taskID >0) {

                if(window.location.hash.indexOf('start') >= 0){
                    history.pushState("", document.title, window.location.pathname + window.location.search);
                    extractAds();
                }

                getAds();
            }

        };

        /* Comment Form */

        var getCommentForm = function () {

            $.ajax({
                type: "GET",
                url: defaults.commentFormURL,
                data:{ },
                beforeSend:function () {
                },
                success: function(response){
                   $(defaults.commentFormDIV).html(response);
                    validateCommentForm();
                },
                error: function(){
                }
            });
        };

        var validateCommentForm = function () {
            $(defaults.commentForm).validate({
                errorPlacement: function(error, element) {}
            });
        };

        /* End Comment Form */

        function notification(message){
            $.notify({
                icon: 'pe-7s-gift',
                message: message

            },{
                type: 'info',
                timer: 4000
            });

        }

        function wait(ms){
            var start = new Date().getTime();
            var end = start;
            while(end < start + ms) {
                end = new Date().getTime();
            }
        };

        var registerEvents = function(){

            $("div").on('click','#btnSearchAds',function(e){
                e.stopPropagation();

                if($(defaults.scraperForm).valid()){
                    $(defaults.scraperForm).submit();
                }
            });

            $("div").on('click','#btnCreateNewSearch',function(e){
                e.stopPropagation();

                conf  = confirm("Are you sure? You want to reload the page?");

                if(conf){
                    window.location = defaults.scraperPageURL
                }
            });

            $("div").on('click','#btnExtractAds',function(e){
                e.stopPropagation();


                if(isValidDataForExtract()){
                    if(defaults.logID > 0 && defaults.taskID >0 ){
                        extractAds();
                    }
                    else {
                        createTask();
                    }
                }
            });

            $("div").on('click','#btnCancelExtractAds',function(e){
                e.stopPropagation();

                stopExtractAds({'id':$("#id_id").val()});
            });

            $("div").on('click','#btnPostMessage',function(e){
                e.stopPropagation();
                validateCommentForm();
                alert($(defaults.commentForm).valid())
            });

        };

        var init = function() {

            if(!defaults.taskID || defaults.taskID <=0) defaults.taskID =0;

            if(!defaults.logID) defaults.logID = 0;

            getScraperForm();

            getCommentForm();

            registerEvents();

            addBootstrapClass();

        };

        init();

        return this;
    };


}( jQuery ));