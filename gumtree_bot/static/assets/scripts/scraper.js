(function ( $ ) {

    $.Scraper = function(options){
        var $this = $(this);

        var defaults = {

            logID:0,
            getScraperFormURL:'',
            scraperFormDIV:'',
            scraperForm:'',
            scraperPageURL:''
        };

        var options = $.extend(defaults, options);

        var getScraperForm = function () {
            $.get(defaults.getScraperFormURL,{ id:defaults.logID },function (response) {
                $(defaults.scraperFormDIV).html(response);
                addBootstrapClass();
                initAjaxScraperForm();
                validateScraperForm();
            });
        };

        var initAjaxScraperForm = function () {

            $(defaults.scraperForm).ajaxForm({
                beforeSubmit:  function(){
                    createDIVLoader($(defaults.scraperFormDIV));
                },
                success: function(response){
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

        var onSearchADd

        function notification(message){
            $.notify({
                icon: 'pe-7s-gift',
                message: ""

            },{
                type: 'info',
                timer: 4000
            });

        }

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


        };



        var init = function() {

            if(!defaults.logID) defaults.logID = 0;

            getScraperForm();

            registerEvents();

            addBootstrapClass();

        };

        init();
        return this;
    };


}( jQuery ));