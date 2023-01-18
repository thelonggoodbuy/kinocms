$(document).ready(function () {
    $('#table_id').DataTable({
        
        "pagingType": "numbers",
        "info": false,
        "lengthChange": false,
        "pageLength": 5,

    });

});

$(document).ready(function () {
    $('#news_and_promo_cinema_hall_id').DataTable({
        
        "responsive": true,
        "pagingType": "numbers",
        "info": false,
        "lengthChange": false,
        "pageLength": 5,
        dom:'<t>',
    });

});

$(document).ready(function () {
    $('#pages_id').DataTable({
        "responsive": true,
        order: [],
        dom:'<t>'
    });

});