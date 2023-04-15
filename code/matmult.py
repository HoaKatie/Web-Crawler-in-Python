#PROBLEM 1- MAMTRIX MULTIPLICATION

#########################################################################
def mult_scalar(matrix, scale): # multiply the matrix by a certain scale
	new_matrix = []
	for row in matrix: #access each row in the matrix
		new_row = []
		for col_ele in row: #access each element in the row of the matrix
			new_row.append(col_ele * scale)
		new_matrix.append(new_row)
	return new_matrix
#########################################################################		
def mult_matrix(a, b): #new matrix is the result of a x b
    row_a = len(a)
    row_b = len(b)
    col_a = len(a[0])
    col_b = len(b[0])
    
    if col_a != row_b: #if  matrices do not have compatible dimensions
        return None
    else:
        new_matrix = []
        for x in range(row_a):
            new_row = []
            for y in range(col_b):
                product = 0
                for z in range(row_b):
                    product += a[x][z] * b[z][y]
                new_row.append(product)
            new_matrix.append(new_row)
        return new_matrix
#########################################################################
	
def euclidean_dist(a,b): # accepts two single-row matrices and calculate the Euclidean distance between these two vectors
    length = len(a[0]) #also = len(b[0])
    # assuming that matrix a and b have same number of elements (from question)
    total = 0
    for n in range(length):
        total += (a[0][n] - b[0][n])**2
    euclidean_dist = total ** 0.5 
    return euclidean_dist
