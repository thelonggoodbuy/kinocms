$(function () {

    // all document event and view-logic

    $("input[type=file]").hide();

    $(document).on('change', "input[name$='image']", function () {
        var $input = $(this);
        var output = $(this).parent().find("img[class$='preview']")
        var reader = new FileReader();
        reader.onload = function () {
            output.attr("src", reader.result);
        };
        reader.readAsDataURL($input[0].files[0]);
        $(this).parent().parent().parent().find("input[name$='DELETE_IMAGE']").prop( "checked", false )
        $(this).parent().parent().parent().find("#del_button").prop('disabled', false);
        
    });




    // main image
    $("#main_image_container input[name$='DELETE_IMAGE']").hide();
    
    $("div[id^='main_image_container']").on('click', '#add_button', function () {
        browse_button = $(this).parent().parent().find('input[type="file"]')
        browse_button.trigger('click');
    });
  

    $("div[id^='main_image_container']").on('click', '#del_button', function () {
        del_image = $(this).parent().parent().find("img[class$='_preview']");
        del_image.attr("src", "/static/cinema/images/empty_form_logo.png");
        del_image.parent().attr("href", "#");
        $(this).parent().find("input[name$='DELETE_IMAGE']")[0].checked = true;
        $(this).prop('disabled', true);        
    });



    // galery formset
    $("#galery_container input[name$='DELETE']").hide();
    
    var galery_cell_height = $("#add_more").parent().prev().height();
    $("#add_more").parent().css('height', galery_cell_height);
    $("#add_more").css('margin-top', galery_cell_height/2.5);


    $("#galery_container").on('click', '#add_more', function () {
        var form_index = $('#id_form-TOTAL_FORMS').val();
        var new_form = $('#empty_form_container').find('a').prop('href', '#').parent().parent().html().replace(/__prefix__/g, form_index);
        $(new_form).insertBefore($('#add_more').parent());
        $('#id_form-TOTAL_FORMS').val(parseInt(form_index) + 1);
    });

    $("#galery_container").on('click', '#add_button', function () {
        browse_button = $(this).parent().find('input[type="file"]')
        browse_button.trigger('click');
    });

    $("#galery_container").on('click', '#del_button', function () {
        link_len = ($(this).prevAll('a').attr('href')).length
        if ($(this).prevAll('a').attr('href') != ('#')){
            del_image = $(this).prevAll().find("img[class$='_preview']");
            del_image.attr("src", "/static/cinema/images/empty_form_logo.png");
            del_image.parent().attr("href", "#");
        $(this).parent().find("input[name$='DELETE']")[0].checked = true;
        } else {
            $(this).parent().hide();
            
        };   
    });

    

    // cinemas additional view-logic

    if ($('#summernote').length>0){this.summernote({
        placeholder: 'Hello Bootstrap 4',
        tabsize: 2,
        height: 200
      })};

    if($('#datetimepicker4').length>0){$('#datetimepicker4').datetimepicker({
            format: 'MM/DD/YYYY'
        });
    };

    
});