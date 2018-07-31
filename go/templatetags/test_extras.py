from django.template import Library

register = Library()

@register.filter
def make_cell_id(row, col):
    return "%d-%d" % (row, col)

@register.filter
def get_stone(stones, cell_id):
    # Split coordinates in cell id
    row,col = (int(x) for x in cell_id.split('-'))

    # Check if current row and column contains stone
    has_stone = row in stones and col in stones[row]

    # Return stone color if it's placed in current cell
    return stones[row][col] if has_stone else None

@register.filter
def is_latest_placed_stone(stone, latest_placed_stone):
    # Check if this is the latest placed stone
    return (
        stone.row == latest_placed_stone.row and
        stone.col == latest_placed_stone.col
    )
