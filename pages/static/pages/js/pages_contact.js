$(function () {
    $("input[type=file]").hide();
    $("input[id$=DELETE]").hide();

    // "div[id^='main_image_container']"
    
    // $("#contact_form").on('click', '#add_more', function () {
    //     var form_index = $('#id_form-TOTAL_FORMS').val();
    //     var empty_form = $('#main_card_table_empty_form');
    //     new_form = $(empty_form).clone();
    //     changed_obj = $(new_form).find("[id^='id_form-__prefix__']");
        
    //     // console.log(changed_obj)
        
    //     $(new_form).html().replace(/__prefix__/g, form_index);
    //     $(new_form).insertBefore($('#add_more').parent().parent());
    //     $('#id_form-TOTAL_FORMS').val(parseInt(form_index) + 1);

 
        
    // });

    $("#contact_form").on('click', '#add_more', function () {
        var form_index = $('#id_form-TOTAL_FORMS').val();
        var new_form = $('#main_card_table_empty_form').find('a').prop('href', '#').parent().parent().parent().parent().parent().html().replace(/__prefix__/g, form_index);
        $(new_form).insertBefore($('#add_more').parent());
        $('#id_form-TOTAL_FORMS').val(parseInt(form_index) + 1);
    });


    $(document).on('change', "input[name$='-logo']", function () {
        console.log('changed!')
        var $input = $(this);
        var output = $(this).parent().find("img[class$='preview']")
        var reader = new FileReader();
        reader.onload = function () {
            output.attr("src", reader.result);
        };
        reader.readAsDataURL($input[0].files[0]);
        $(this).parent().parent().parent().find("#del_button").prop('disabled', false);  
    });

        // main image
    $(document).on('click', '#add_button', function () {
        console.log('add button!')
        browse_button = $(this).parent().parent().find('input[type="file"]')
        browse_button.trigger('click');
        });

    $(document).on('click', '#del_button', function () {
        // link_len = ($(this).prevAll('a').attr('href')).length
        // if ($(this).prevAll('a').attr('href') != ('#')){
        //     del_image = $(this).prevAll().find("img[class$='_preview']");
        //     del_image.attr("src", "/static/cinema/images/empty_form_logo.png");
        //     del_image.parent().attr("href", "#");
        // $(this).parent().find("input[name$='DELETE']")[0].checked = true;
        // } else {
            $(this).next()[0].checked = true;
            $(this).parent().parent().parent().parent().hide();
            
            
        }); 


});