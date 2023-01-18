// $(document).ready(function() {
//     $('#table_id').DataTable();
// });

$(document).ready(function () {
    $('#table_id').DataTable({
        
        
        // "responsive": true,
        "pagingType": "numbers",
        "info": false,
        "lengthChange": false,
        "pageLength": 5,
        scrollX: true,

    });

    // $('#table_id').DataTable( {

    //     rowReorder: {
    //         selector: 'td:nth-child(2)'
    //     },

    //     responsive: true
    // } );




    // $(document).ready(function () {
    //     $('#table_id').DataTable({
            
            
    //         "responsive": true,
    //         "pagingType": "numbers",
    //         "info": false,
    //         "lengthChange": false,
    //         "pageLength": 5,
    
    //     });

    // $('#table_ciname_hall_id').DataTable({
        
    //     "pagingType": "numbers",
    //     "info": false,
    //     "lengthChange": false,
    //     "pageLength": 5,

    // });
});

$(document).ready(function () {
    $('#table_cinema_hall_id').DataTable({
        
        "pagingType": "numbers",
        "responsive": true,
        "info": false,
        "lengthChange": false,
        "pageLength": 5,
        dom:'<t>',
    });

    // $('#table_ciname_hall_id').DataTable({
        
    //     "pagingType": "numbers",
    //     "info": false,
    //     "lengthChange": false,
    //     "pageLength": 5,

    // });

$(document).ready(function () {
    $('#table_mailing').DataTable({
        
        // "pagingType": "numbers",
        // "pageLength": 5,
        "info": false,
        "lengthChange": false,
        "paging": false,

    });

});
});



