class Cell:
    """
    A class used to represent a Cell in a Kakuro grid

    Attributes
    ----------
    pos : list
        The position of the cell in a pre-defined grid.
    value : int or None
        The value contained within a cell, None represents an empty cell.
    row_id : int or None
        The id of the row the cell is contained in.
    col_id : int or None
        The id of the col the cell is contained in.

    Methods
    -------
    is_empty()
        returns whether a given cell is empty
    """

    def __init__(self, pos, value=None, row_id=None, col_id=None):
        if type(pos) not in [list, tuple]:
            raise Exception("The variable pos is not a list or a tuple")
        elif len(pos) != 2:
            raise Exception("The variable pos is not of length 2")
        elif (int(pos[0]) - pos[0] != 0) or (int(pos[1]) - pos[1] != 0):
            raise Exception("The variable pos does not contain integers")
        else:
            self.pos = pos  # of the form (row i, col j)
        self.value = value
        self.row_id = row_id
        self.col_id = col_id

    def is_empty(self):
        """Return whether a cell is empty.

        Returns
        -------
        Boolean
            whether the cell is empty or not.

        """
        return self.value is None

    def copy(self):
        """Creates a copy of the current cell

        Returns
        -------
        Cell
            A copy of the current cell.

        """
        new_cell = Cell(self.pos, self.value, self.row_id, self.col_id)
        return new_cell

    def __eq__(self, other):
        return self.pos == other.pos

    def __repr__(self):
        return (f"{{{self.pos}: {self.value},"
                f" row_id: {self.row_id}, col_id: {self.col_id}}}")


class CellGrid:
    def __init__(self, cells=[]):
        if len(cells) != len(set(c.pos for c in cells)):
            raise Exception("Not all cells are in unique grid positions")
        self.cell_array = cells
        self.cell_pointer = {}
        for i, cell in enumerate(self.cell_array):
            self.cell_pointer[tuple(cell.pos)] = i
        if len(self.cell_array) != 0:
            self.update_grid()

    def get_cell_pointer(self, cell):
        return self.cell_pointer[tuple(cell.pos)]

    def add_cell(self, cell):
        if self.cell_pointer.get(tuple(cell.pos)) is not None:
            raise Exception("There already exists a cell at this position")
        n = len(self.cell_array)
        self.cell_array.append(cell)
        self.cell_pointer[tuple(cell.pos)] = n
        self.update_grid()

    def del_cell(self, cell):
        if self.cell_pointer.get(tuple(cell.pos)) is None:
            raise Exception("There exists no cell at this position")
        i = self.get_cell_pointer(cell)
        del self.cell_array[i]
        del self.cell_pointer[tuple(cell.pos)]
        for key, value in self.cell_pointer.items():
            if value > i:
                self.cell_pointer[key] = value - 1
        self.update_grid()

    def get_cell(self, pos):
        i = self.cell_pointer[pos]
        return self.cell_array[i]

    def set_cell(self, pos, value):
        cell = self.get_cell(pos)
        cell.value = value

    def find_rows(self):
        grid_height_ub = max([cell.pos[0] for cell in self.cell_array])
        grid_height_lb = min([cell.pos[0] for cell in self.cell_array])
        grid_length_ub = max([cell.pos[1] for cell in self.cell_array])
        grid_length_lb = min([cell.pos[1] for cell in self.cell_array])
        rows = []
        cur_row_id = -1
        for i in range(grid_height_lb, grid_height_ub + 1):
            in_void_space = True
            cur_row = []
            for j in range(grid_length_lb, grid_length_ub + 1):
                try:
                    cell = self[i, j]
                except KeyError:
                    cell = None
                if cell is None:
                    if not in_void_space:
                        in_void_space = True
                        rows.append(cur_row)
                        cur_row = []
                    continue
                else:
                    if in_void_space:
                        in_void_space = False
                        cur_row_id += 1
                    cell.row_id = cur_row_id
                    cur_row.append(cell)
            if len(cur_row) != 0:
                rows.append(cur_row)
        self.rows = rows

    def find_cols(self):
        grid_height_ub = max([cell.pos[0] for cell in self.cell_array])
        grid_height_lb = min([cell.pos[0] for cell in self.cell_array])
        grid_length_ub = max([cell.pos[1] for cell in self.cell_array])
        grid_length_lb = min([cell.pos[1] for cell in self.cell_array])
        cols = []
        cur_col_id = -1
        for j in range(grid_length_lb, grid_length_ub + 1):
            in_void_space = True
            cur_col = []
            for i in range(grid_height_lb, grid_height_ub + 1):
                try:
                    cell = self[i, j]
                except KeyError:
                    cell = None
                if cell is None:
                    if not in_void_space:
                        in_void_space = True
                        cols.append(cur_col)
                        cur_col = []
                    continue
                else:
                    if in_void_space:
                        in_void_space = False
                        cur_col_id += 1
                    cell.col_id = cur_col_id
                    cur_col.append(cell)
            if len(cur_col) != 0:
                cols.append(cur_col)
        self.cols = cols

    def update_grid(self):
        self.find_cols()
        self.find_rows()

    def is_connected(self):
        if len(self.cell_array) == 0:
            return True
        else:
            cell_list = [self.cell_array[0].pos]
            ind = 0
            while ind < len(cell_list):
                cur_cell = self.get_cell(cell_list[ind])
                cur_pos = cur_cell.pos
                for offset in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
                    new_pos = (cur_pos[0] + offset[0],
                               cur_pos[1] + offset[1])
                    if new_pos not in cell_list:
                        try:
                            self[new_pos[0], new_pos[1]]
                        except KeyError:
                            continue
                        cell_list.append(new_pos)

                ind += 1

        return len(cell_list) == len(self.cell_array)

    def copy(self):
        new_cell_list = [cell.copy() for cell in self.cell_array]
        return CellGrid(new_cell_list)

    def __getitem__(self, pos):
        return self.get_cell(pos)

    def __setitem__(self, pos, value):
        self.set_cell(pos, value)

    def __delitem__(self, pos):
        cell = self.get_cell(pos)
        self.del_cell(cell)

    def __repr__(self):
        return repr(self.cell_array)


class Kakuro:
    def __init__(self, cell_grid, row_values, col_values):
        if not cell_grid.is_connected():
            raise Exception(("The given board is not connected and"
                             " is thus invalid"))
        self.cell_grid = cell_grid
        if len(row_values) != len(self.cell_grid.rows):
            raise Exception(("Number of row constraints does not match"
                             " the number of rows"))
        self.row_values = row_values
        if len(col_values) != len(self.cell_grid.cols):
            raise Exception(("Number of column constraints does not match"
                             " the number of columns"))
        self.col_values = col_values

    def copy(self):
        new_cell_grid = self.cell_grid.copy()
        new_row_values = self.row_values[:]
        new_col_values = self.col_values[:]
        return Kakuro(new_cell_grid, new_row_values, new_col_values)


def main():
    x = CellGrid()
    x.add_cell(Cell((1, 1)))
    x.add_cell(Cell((2, 1)))
    x.add_cell(Cell((3, 1)))
    x.add_cell(Cell((3, 2)))
    x.add_cell(Cell((3, 3)))

    x.update_grid()
    print()
    for row in x.rows:
        print(row)
    print()
    for col in x.cols:
        print(col)
    print()
    print(x.is_connected())

    x.add_cell(Cell((1, 3)))
    x.add_cell(Cell((2, 3)))
    x.add_cell(Cell((5, 1)))
    x.add_cell(Cell((5, 2)))

    x.update_grid()
    print()
    for row in x.rows:
        print(row)
    print()
    for col in x.cols:
        print(col)
    print()
    print(x.is_connected())


if __name__ == '__main__':
    main()
