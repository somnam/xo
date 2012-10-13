$(".cell").click(function() {
    // Create new stone
    var stone = document.createElement('div');
    stone.className = 'stone';

    // Append stone to cell
    var cell = $(this);
    cell.append(stone);

    $(stone).fadeIn('fast');
});
