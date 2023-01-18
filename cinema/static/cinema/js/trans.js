$(function () {

    // console.log($('#uk-block-tab'))
    // console.log($('#ru-block-tab'))
    // console.log($('#main_form_container'))
    console.log($("[class$='ru-block']"))
    var ru_block = $("[class$='ru-block']")
    var ua_block = $("[class$='uk-block']")
    ru_block.hide()

    $('#main_form_container').on('click', '#uk-block-tab', function(){
        ru_block.hide();
        ua_block.fadeIn('slow');
    });

    $('#main_form_container').on('click', '#ru-block-tab', function(){
        ua_block.hide();
        ru_block.fadeIn('slow');
    });
});