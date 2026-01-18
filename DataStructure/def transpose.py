def transpose(image):
    """
    Returns True after transposing the image
    
    All plug-in functions must return True or False.  This function returns True 
    because it modifies the image. It transposes the image, swaping colums and rows.
    
    Transposing is tricky because you cannot just change the pixel values; you have
    to change the size of the image table.  A 10x20 image becomes a 20x10 image.
    
    The easiest way to transpose is to make a transposed copy with the pixels from
    the original image.  Then remove all the rows in the image and replace it with
    the rows from the transposed copy.
    
    Parameter image: The image buffer
    Precondition: image is a 2d table of RGB objects
    """
    # Change this to return True when the function is implemented
    orig_height = len(image)
    orig_width = len(image[0])
    transposed = []
    for col in range(orig_width):
        new_row = []
        for row in range(orig_height):
            new_row.append(image[row][col])
        transposed.append(new_row)
    image.clear()
    for row in transposed:
        image.append(row)
        
    return True