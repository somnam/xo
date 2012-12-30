from django.template import Library

register = Library()

@register.filter
def make_cell_id(row, col):
    return "%d-%d" % (row, col)

@register.filter
def get_stone(stones, cell_id):
    # Split coordinates in cell id
    row,col = map(lambda(v): int(v), cell_id.split('-'))

    # Check if current row and column contains stone
    has_stone = stones.has_key(row) and stones[row].has_key(col)

    # Return stone color if it's placed in current cell
    return stones[row][col] if has_stone else None
