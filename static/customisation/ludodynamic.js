// Copyright (C) 2016  Pierre-Yves Martin for DCALK
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published
// by the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

// Activate dynamic table with DataTables.net and set it to french
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