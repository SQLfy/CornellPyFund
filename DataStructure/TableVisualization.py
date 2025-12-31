def crossout(table,row,col):
    """
    Modifies the table to remove the given row and column.
    
    Examples:
        If a = [[1,3,5],[6,2,7],[5,8,4]], crossout(a,1,2) changes a to [[1,3],[5,8]]
        If a = [[1,3,5],[6,2,7],[5,8,4]], crossout(a,0,0) changes a to [[2,7],[8,4]]
        If a = [[1,3],[6,2]], crossout(a,0,0) changes a to [[2]]
        If a = [[6]], crossout(a,0,0) changes a to []
    
    Parameter table: the nested list to modify
    Precondition: table is a table of numbers.  In other words, 
        (1) table is a nested 2D list in row-major order, 
        (2) each row contains only numbers, and 
        (3) each row is the same length.
    
    Parameter row: the row to remove
    Precondition: row is an index (int) for a row of table
    
    Parameter col: the column to remove
    Precondition: col is an index (int) for a column of table
    """

    for rpos in range(len(table)):
        if rpos != row:
            for cpos in range(len(table[rpos])):
                if cpos != col:
                    print(f"Row {rpos} Column {cpos} = {table[rpos][cpos]}")
                    result = table[rpos][cpos]
    
            
def loop_visualize(table):
    table = [[1,3,5],[6,2,7],[5,8,4]]

    for rpos in range(len(table)):
        for cpos in range(len(table[rpos])):
            print(f"Row {rpos} Column {cpos} = {table[rpos][cpos]}")
    result = f"Row {rpos} Column {cpos} = {table[rpos][cpos]}"
    print(result)

