$(document).ready(function() {
    poll();
});

function getBoardId() {
    var board = $('.board');
    return board.attr("id").replace("_board", "");
}

function getUpdateUrl() {
    return '/go/' + getBoardId() + '/update/';
}

$(".cell").click(function() {
    // Get cell coordinates from id
    var coords = this.id.replace("_cell", "").split("-");
    // Get selected action type
    var action = $('input[name="action"]:radio:checked').val();

    $.ajax({
        type        : "POST",
        url         : getUpdateUrl(),
        dataType    : "json",
        beforeSend  : addCSRFToken,
        data        : {
            'row'    : coords[0],
            'col'    : coords[1],
            'action' : action,
        },
    });
});

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

// Update board after second players move.
function updateBoard(response) {
    if (response) {
        var stones          = response['placed_stones'],
            next_move_color = response['next_move_color'];

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

        // Update next move info
        var nextMoveSpanId      = getBoardId() + "_next_move_color";
        var nextMoveSpan        = document.getElementById(nextMoveSpanId);
        nextMoveSpan.innerHTML  = response['next_move_color'];
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

