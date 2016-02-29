// Activate dynamic table with DataTables.net
// ref: https://datatables.net
$(document).ready( function () {
    $('#gamestab').DataTable({
        dom: "lftip",
        language: {
            // Warning the language files can't be retrieved by bower you have to download them and add them to them project
            url: "/static/internationalisation/French.json"
        }
    });
} );