var socket = io.connect('http://localhost:4040/');

// Subscribe to two channels.
socket.on('connect', function() {
    socket.emit('subscribe', 'go');
    socket.emit('subscribe', 'chat');

    scrollMessageBox();
});

// Listen for 'message' event.
socket.on('message', function (data) {
    // Update board.
    if (data.channel === 'go') {
        updateBoard($.parseJSON(data.message));
    // Update chat.
    } else if (data.channel === 'chat') {
        updateChat($.parseJSON(data.message));
    }
});

// Get Board id from board div
function getBoardId() {
    var board = $('.board');
    return board.attr('id').replace('_board', '');
}

// Get update url
function getBoardUpdateUrl() {
    return '/go/' + getBoardId() + '/update/';
}
function getChatUpdateUrl() {
    return '/go/' + getBoardId() + '/say/';
}

// Place stone on board via Ajax
$('.cell').click(function() {
    // Get cell coordinates from id
    var coords = this.id.replace('_cell', '').split('-');
    // Get selected action type
    var action = $('input[name="action"]:radio:checked').val();

    $.ajax({
        type        : 'POST',
        url         : getBoardUpdateUrl(),
        dataType    : 'json',
        beforeSend  : addCSRFToken,
        data        : {
            'row'    : coords[0],
            'col'    : coords[1],
            'action' : action,
        },
    });
});

// Update board after second players move
function updateBoard(response) {
    if (response) {
        var stones              = response['placed_stones'],
            next_move_color     = response['next_move_color'];
            latest_placed_stone = response['latest_placed_stone'];

        // Clear all current stones from board
        $('.stone').remove();

        // Update board with received stones
        for (var i = 0, j = stones.length; i < j; i++) {
            var stone = stones[i];
            if (stone.hasOwnProperty('fields')) {
                addStone(stone.fields, latest_placed_stone.fields);
            }
        }

        // Update next move info
        var nextMoveSpan        = document.getElementById('next_move_color');
        nextMoveSpan.innerHTML  = response['next_move_color'];
    }
}

// Draw stone on board
function addStone(stone, latest_placed_stone) {
    // Find cell for stone
    var cellId = stone.row + '-' + stone.col + '_cell';
    var cell   = document.getElementById(cellId);
    if (cell) {
        // FIXME
        stoneColor = ['black', 'white'];

        // Create new stone
        var stoneDiv = document.createElement('div');
        stoneDiv.className = 'stone block ' + stoneColor[stone.color];

        // Append stone to cell
        var $cell = $(cell);
        $cell.append(stoneDiv);

        // Append latest placed stone
        if (latest_placed_stone &&
            stone.row === latest_placed_stone.row &&
            stone.col === latest_placed_stone.col
        ) {
            var latestDiv       = document.createElement('div');
            latestDiv.className = 'stone block latest';
            $(stoneDiv).append(latestDiv);
        }
    }
}

// Submit chat message via Ajax
$('.chat').submit(function () {
    // Get message box elem
    var messageInput = $('#chat-message');

    // Send ajax request
    $.ajax({
        type        : 'POST',
        url         : getChatUpdateUrl(),
        dataType    : 'json',
        beforeSend  : addCSRFToken,
        data        : {
            'message' : messageInput.val(),
        },
    });

    // Clear message
    messageInput.val('');

    return false;
});

// Update chat after second players message
function updateChat(response) {
    if (response) {
        var chatMessages = response['chat_messages'];

        // Clear all current messages
        $('.message-wrapper').remove();

        // Update chat box with received messages
        for (var i = 0, j = chatMessages.length; i < j; i++) {
            var message = chatMessages[i];
            if (message.hasOwnProperty('fields')) {
                addChatMessage(message.fields);
            }
        }

        scrollMessageBox();
    }
}

function scrollMessageBox(scrollSpeed) {
    scrollSpeed = scrollSpeed || 1000;

    // Scroll down to last message
    var $messageBox = $('#message-box');
    if ($messageBox.prop('scrollHeight') > $messageBox.height()) {
        $messageBox.animate(
            { scrollTop : $messageBox.prop('scrollHeight') },
            scrollSpeed
        );
    }
}

function addChatMessage(message) {
    // Create message wrapper
    var messageWrapper = document.createElement('div');
    messageWrapper.className = 'message-wrapper';
    var $messageWrapper = $(messageWrapper);

    // Create timestamp elem
    var timestampSpan = document.createElement('span');
    timestampSpan.className = 'timestamp';
    timestampSpan.innerHTML = message.timestamp;
    $messageWrapper.append(timestampSpan);

    // Create author elem
    if (message.type === 'm') {
        var authorSpan = document.createElement('span');
        authorSpan.className = 'author';
        authorSpan.innerHTML = message.author;
        $messageWrapper.append(authorSpan);
        $messageWrapper.append(':');
    }

    // Create messsage elem
    var messageSpan = document.createElement('span');
    messageSpan.className = 'message ' + message.type;
    messageSpan.innerHTML = message.message;
    $messageWrapper.append(messageSpan);

    // Appent message to message box
    var $messageBox = $('#message-box');
    $messageBox.append(messageWrapper);
}

