$(function () { 


    $("[id^='id_form-']").prop( "checked", false)
    $("#form_for_letter").hide()
    $("[id^='hidden_block']").hide()
    $("#update_mailing_submit").hide()
    $("#users_list").hide()
    $("#main_card_table").show()


    $("#main_card_table").on('click', '#choose_users_button', function(){
        console.log('!!!!')
        $("#main_card_table").hide()
        $("#users_list").show()
    });


    $("#users_list").on('click', '#submit_to_changed_users', function(){
        console.log('!!!!')
        $("#main_card_table").show()
        $("#users_list").hide()
    });


    

    // console.log($("form_for_letter"))


    
    $("#table_mailing").on('click', '#mailing_checkbox', function () {
        var checked_checkbox_number = ($(this)).parent().next().html();
        // $("input[id^='saved_template_checkbox']").prop("checked", false);
        // $("input[id^='id_form-']").prop("checked", false);
        // $("input[id^='id_main_list_form-']").prop("checked", false);
        // $("input[id='mailing_checkbox']").prop("checked", false);
        number = checked_checkbox_number;

    
        if ($("#id_main_list_form-template").val().length != 0){
            var current_user = $("#form_for_letter").find("label:contains("+ number +")");
            if($(this).is(':checked')){
                $(current_user).find("input").prop("checked", true)
            } else {
                $(current_user).find("input").prop("checked", false)
            }}
            else
            { 
            var actual_checkboxes = $('#formset_saved_templates').find("input[id^='saved_template_checkbox']:checked")
            var current_user = actual_checkboxes.parent().parent().next().find("label:contains("+ number +")")
            if($(this).is(':checked')){
                $(current_user).find("input").prop("checked", true)
            } else {
                $(current_user).find("input").prop("checked", false)
            }};
    });


    $("#formset_saved_templates").on('click', "input[id^='saved_template_checkbox']", function(){
        $("input[id^='saved_template_checkbox']").not(this).prop("checked", false);
        $("input[id^='id_form-']").prop("checked", false);
        $("input[id^='id_main_list_form-']").prop("checked", false);
        $("input[id='mailing_checkbox']").prop("checked", false);
        $("#id_main_list_form-template").val(null)

        $("#downloaded_template_name").text(null);
        $("#current_template_name").text($(this).parent().next().find('#saved_template_name').html());
        $("#mailing_statistic").text($(this).parent().parent().next().find('#mailing_statistic').html());

    });



    $("#main_card").on('click', '#all_users_checkbox', function(){
        if($(this).is(':checked')){
            $('#selectively_users').prop("checked", false)
            $('#choose_users_button').prop('disabled', true)
            var checkboxes = $("[id='mailing_checkbox']")
            for (var [key, value] of Object.entries(checkboxes)){
                if ($(value).prop('checked') == false){
                    $(value).trigger("click");
                }}}});


    $("#table_mailing").on('click', '#mailing_checkbox', function(){
        if($(this).prop('checked') == false){
            $('#selectively_users').prop("checked", true)
            $('#all_users_checkbox').prop("checked", false)
        }});


    $("#main_card").on('click', '#selectively_users', function(){
        $('#all_users_checkbox').prop("checked", false)
        $('#choose_users_button').prop('disabled', false)
        var checkboxes = $("[id='mailing_checkbox']")
        for (var [key, value] of Object.entries(checkboxes)){
            if ($(value).prop('checked') == true){
                $(value).trigger("click");
            }};
    });


    $("#main_card").on('click', '#download_button', function(){
        $('#id_main_list_form-template').trigger("click");
    });


    $("#form_for_letter").on('change', '#id_main_list_form-template', function(){
        var template_name = $(this).val().split('\\').pop()
        $('#downloaded_template_name').text(template_name)
        $('#current_template_name').text(template_name)
        $('#mailing_statistic').text('0%')
    });

    $("#formset_saved_templates").on('click', '#delete_link', function(){
        $(this).parent().parent().parent().next().find('input[id$=DELETE]').prop("checked", true)
        $(this).parent().parent().parent().parent().parent().find('input[type=submit]').click()
    });


    $("#main_card").on('click', '#main_submit_button', function(){
        if($("#id_main_list_form-template").val().length != 0){
            console.log($("#new_template_submit"))
            $("#new_template_submit").trigger("click");
        } else{
            console.log($('#update_mailing_submit'))
            $('#update_mailing_submit').trigger("click");
        }
    });

});


