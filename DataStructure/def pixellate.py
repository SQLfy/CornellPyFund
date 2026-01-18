def pixellate(image,step=10):
    """
    Returns True after pixellating the image.
    
    All plug-in functions must return True or False.  This function returns True 
    because it modifies the image. It pixellates the image to give it a blocky feel. 
    
    To pixellate an image, start with the top left corner (e.g. the first row and column).  
    Average the colors (all 4 values including alpha) of the step x step block to the
    right and down from this corner.  For example, if step is 3, you will average the
    colors at positions (0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), and (2,2).
    After computing the averages, assign each color's (and the alpha's) average value
    to ALL the pixels in the block.
    
    If there are less than step rows or step columns, go to the edge of the image.  So
    on a image with 2 rows and 4 columns, a step 3 pixellate would process the colors
    at positions  (0,0), (0,1), (0,2), (1,0), (1,1), and (1,2).
    
    When you are done, skip over step columns to get the the next corner pixel, and 
    repeat  this process again.  Because the blocks do not overlap, it is not necessary 
    to create a copy (like blur). You can reassign the pixels before moving to the next 
    block. For example, suppose step is 3. Then the next block is at position (0,3) and 
    includes the pixels at (0,3), (0,4), (0,5), (1,3), (1,4), (1,5), (2,3), (2,4), 
    and (2,5).  
    
    Continue the process looping over rows and columns to get a pixellated image.
    
    Parameter image: The image to pixelate
    Precondition: image is a 2d table of RGB objects
    
    Parameter step: The number of pixels in a pixellated block
    Precondition: step is an int > 0
    """
    # We recommend enforcing the precondition for step
    # Change this to return True when the function is implemented
    assert type(step) == int and step > 0, "Precondition violation: step is not an int > 0"

    height = len(image)
    if height == 0:
        return False
    width = len(image[0])
    for row in range(0, height, step):
        for col in range(0, width, step):
            r_total = 0
            g_total = 0
            b_total = 0
            a_total = 0
            count = 0
            
            for r in range(row, min(row + step, height)):
                for c in range(col, min(col + step, width)):
                    pixel = image[r][c]
                    r_total += pixel.red
                    g_total += pixel.green
                    b_total += pixel.blue
                    a_total += pixel.alpha
                    count += 1
            
            if count > 0:
                r_avg = r_total // count
                g_avg = g_total // count
                b_avg = b_total // count
                a_avg = a_total // count
                
                for r in range(row, min(row + step, height)):
                    for c in range(col, min(col + step, width)):
                        image[r][c].red = r_avg
                        image[r][c].green = g_avg
                        image[r][c].blue = b_avg
                        image[r][c].alpha = a_avg


    return True