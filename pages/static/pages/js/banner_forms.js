
$(function () {

    // Top-banner view-logic
    // hiding not suitable forms elements proposed by django
    $("#top_banner_cell_form_set input[name$='DELETE']").hide()
    $("#top_banner_cell_form_set input[type=file]").hide()


    // event: add empty form
    $("#top_banner_cell_form_set").on('click', '#add_more',function () {
        var form_index = $('#id_form-TOTAL_FORMS').val();
        var new_form = $('#empty_form_container').html().replace(/__prefix__/g, form_index);
        $(new_form).insertBefore($('#add_more').parent());
        $('#id_form-TOTAL_FORMS').val(parseInt(form_index) + 1);
    });

    // event: prerender of added image in existing and cloned empty forms
    $("#top_banner_cell_form_set").on('change', "input[name$='image']", function () {
        console.log(this)
        var $input = $(this);
        var output = $(this).parent().find("img[class='image_test_card']")
        var reader = new FileReader();
        reader.onload = function () {
            output.attr("src", reader.result);
        };
        reader.readAsDataURL($input[0].files[0]);
    });

    // event: delete exist or empty form using django "can_delete" feature    
    $("#top_banner_cell_form_set").on('click', '#delete_button', function () {
        console.log($(this).parent())
        del_image = $(this).parent().find("img[class='image_test_card']");
        console.log(del_image)
        if (del_image.attr("src") == "/static/cinema/images/empty_form_logo.png") {
            del_image = $(this).parent().find("img");
            del_image.attr("src", "");
            del_true = $(this).parent().find("input[name$='DELETE']");
            del_true[0].checked = true;
            del_container = $(this).parent().parent();
            del_container.hide();
        } else {
            del_image.attr("src", "/static/cinema/images/empty_form_logo.png");
        }
    });


    // event: delete exist or empty form using django "can_delete" feature    
    $("#top_banner_cell_form_set").on('click', '#delete_button', function () {
        del_image = $(this).parent().find("img[class='image_test_card']");
        del_image.attr("src", "/static/cinema/images/empty_form_logo.png");
    });



    // event: event-bunch between custom and buildin button for adding image
    $("#top_banner_cell_form_set").on('click', '#add_button', function () {
        browse_button = $(this).parent().find('input[type="file"]')
        browse_button.trigger('click');
    });


    $('#main_top_banner').on('click', '#save_top_banner', function () {
        // console.log('Start!')
        cell_without_image = $("#banner_form").find("img[src='/static/cinema/images/empty_form_logo.png']").parent().parent().find("input[name$='DELETE']");
        cell_without_image.prop('checked', true);
    });

    var galery_cell_height = $("#add_more").parent().prev().height();
    $("#main_top_banner #add_more").parent().css('height', galery_cell_height);
    $("#main_top_banner #add_more").css('margin-top', galery_cell_height/2.5);


// ************************************************************************
    // Through_backround_banner
    $("#through_banner").find('input[name="delete_image"]').hide()
    $("#through_banner").find('input[type="file"]').hide()
    // name="delete_image"

    // state: state of background, if admin use build-in background
    if ($("#through_banner #id_background_type_1").prop("checked")) {
        $("#through_banner #del_button").prop('disabled', true)
        $("#through_banner #add_button").prop('disabled', true)
    }

    // event: change from build-in image to custom user image, if admin use custom background
    $("#through_banner").on('click', "#id_background_type_0", function(){
        del_button = $("#through_banner #del_button").prop("disabled", false)
        add_button = $("#through_banner #add_button").prop("disabled", false)
        $("#through_banner #add_button").parent().parent().find('#default_image').hide()
        $("#through_banner #add_button").parent().parent().find('#background_container').show()
    });

    // event: change from custom user image to build-in image, if admin use build-in background
    $("#through_banner").on('click', "#id_background_type_1", function(){
        del_button = $("#through_banner #del_button").prop('disabled', true)
        add_button = $("#through_banner #add_button").prop('disabled', true)
        $("#through_banner #add_button").parent().parent().find('#background_container').hide()
        $("#through_banner #add_button").parent().parent().find('#default_image').show()

    });


    $("#through_banner").on('click', '#add_button', function () {
        $(this).parent().next().find('input[name="delete_image"]').prop("checked", false)
        browse_button = $(this).parent().parent().find('input[type="file"]')
        browse_button.trigger('click');
    });

    
    $("#through_banner").on('change', "input[name$='image']", function () {
        console.log(this);
        var $input = $(this);
        var output = $(this).parent().find("img[class='image_test_card']")
        var reader = new FileReader();
        reader.onload = function () {
            output.attr("src", reader.result);
        };
        reader.readAsDataURL($input[0].files[0]);
    });

    $("#through_banner").on('click', '#del_button', function () {
        link_to_photo = $("#through_banner #add_button").parent().parent().find('#background_container img');
        console.log(link_to_photo)
        console.log(link_to_photo[0])
        if(link_to_photo.attr("src") != "/static/cinema/images/empty_form_logo.png"){
            link_to_photo.prop('src', '/static/cinema/images/empty_form_logo.png');
            link_to_photo.parent().prop('href', '');
            $(this).next().prop("checked", "true")
        }
    });
// *****************************************************************************************************************************
    // Banner for promo and images view-logic
    // hiding not suitable forms elements proposed by django
    $("#banner_promo_news input[name$='DELETE']").hide()
    $("#banner_promo_news input[type=file]").hide()


    // event: add empty form
    $("#banner_promo_news").on('click', '#add_more',function () {
        console.log('Click!')
        var form_index = $('#banner_promo_news #id_form-TOTAL_FORMS').val();
        var new_form = $('#banner_promo_news #empty_form_container').html().replace(/__prefix__/g, form_index);
        $(new_form).insertBefore($('#banner_promo_news #add_more').parent());
        $('#banner_promo_news #id_form-TOTAL_FORMS').val(parseInt(form_index) + 1);
    });

    // event: prerender of added image in existing and cloned empty forms
    $("#banner_promo_news").on('change', "input[name$='image']", function () {
        var $input = $(this);
        var output = $(this).parent().find("img[class='image_test_card']")
        var reader = new FileReader();
        reader.onload = function () {
            output.attr("src", reader.result);
        };
        reader.readAsDataURL($input[0].files[0]);
    });

    // // event: delete exist or empty form using django "can_delete" feature    
    $("#banner_promo_news").on('click', '#delete_button', function () {

        del_image = $(this).parent().find("img[class='image_test_card']");
        if (del_image.attr("src") == "/static/cinema/images/empty_form_logo.png") {
            console.log('')
            del_image = $(this).parent().find("img");
            del_image.attr("src", "");
            del_true = $(this).parent().find("input[name$='DELETE']");
            del_true[0].checked = true;
            del_container = $(this).parent().parent();
            del_container.hide();
        } else {
            del_image.attr("src", "/static/cinema/images/empty_form_logo.png");
        }
    });


    // event: delete exist or empty form using django "can_delete" feature    
    $("#banner_promo_news").on('click', '#delete_button', function () {
        del_image = $(this).parent().find("img[class='cinema_preview']");
        del_image.attr("src", "/static/cinema/images/empty_form_logo.png");
    });



    // event: event-bunch between custom and buildin button for adding image
    $("#banner_promo_news").on('click', '#add_button', function () {
        browse_button = $(this).parent().find('input[type="file"]')
        browse_button.trigger('click');
    });


    $('#banner_promo_news').on('click', '#save_promotion_and_news_banner', function () {
        // console.log('Start!')
        cell_without_image = $("#banner_promo_news").find("img[src='/static/cinema/images/empty_form_logo.png']").parent().parent().find("input[name$='DELETE']");
        cell_without_image.prop('checked', true);
    });

    var promo_cell_height = $("#add_more").parent().prev().height();
    $("#banner_promo_news #add_more").parent().css('height', promo_cell_height);
    $("#banner_promo_news #add_more").css('margin-top', promo_cell_height/2.5);


});
