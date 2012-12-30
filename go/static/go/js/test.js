$(document).ready(function() {
    poll();
});

function getUpdateUrl() {
    var board    = $('.board');
    var board_id = board.attr("id").replace("_board", "");
    return '/go/' + board_id + '/update/';
}

$(".cell").click(function() {
    // Get cell coordinates from id
    var coords = this.id.replace("_cell", "").split("-");

    $.ajax({
        type        : "POST",
        url         : getUpdateUrl(),
        dataType    : "json",
        beforeSend  : addCSRFToken,
        data        : {
            'row' : coords[0],
            'col' : coords[1],
        },
    });
});

// Update board after second players move.
function updateBoard(stones) {
    if (stones) {
        // Clear all current stones from board
        $('.stone').remove();

        // Update board with received stones
        for (var i = 0, j = stones.length; i < j; i++) {
            var stone = stones[i];
            if (stone.hasOwnProperty('fields')) {
                var fields = stone.fields;
                addStone(fields);
            }
        }
    }

    return setTimeout(poll, 0);
}

// Draw stone on board.
function addStone(stone) {
    // Find cell for stone
    var cellId = stone.row + "-" + stone.col + "_cell";
    var cell   = document.getElementById(cellId);
    if (cell) {
        // FIXME
        stoneColor = ['black', 'white'];

        // Create new stone
        var stoneDiv = document.createElement('div');
        stoneDiv.className = "stone block " + stoneColor[stone.color];

        // Append stone to cell
        var $cell = $(cell);
        $cell.append(stoneDiv);
    }
}

// Update board state after other players move.
function poll() {
    $.ajax({
        type        : "POST",
        url         : getUpdateUrl(),
        dataType    : "json",
        beforeSend  : addCSRFToken,
        success     : updateBoard,
    });
}
