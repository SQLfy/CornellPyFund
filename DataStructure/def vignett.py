def vignette(image):
    """
    Returns True after vignetting (corner darkening) the current image.
    
    All plug-in functions must return True or False.  This function returns True 
    because it modifies the image. It simulates vignetting, which is a characteristic 
    of antique lenses. This plus sepia tone helps give a photo an antique feel.
    
    To compute the vignette, you must compute the distance of each pixel from the
    center.  For any two pixels at position (r0,c0) and (r1,c1), the distance between
    the two is
        
        dist( (r0,c0), (r1,c1)) = sqrt( (r0-r1)*(r0-r1)+(c0-c1)*(c0-c1) )
    
    The vignette factor for a pixel at row r, col r is
        
        1 - (d / H)^2
    
    where d is the distance from the pixel to the center of the image and H (for the
    half diagonal) is the distance from the center of the image to a corner. To 
    vignette an image, multiply each NON-ALPHA color value by its vignette factor.
    The alpha value should be left untouched.
    
    Parameter image: The image buffer
    Precondition: image is a 2d table of RGB objects
    """
    # calculate the center of the image
    height = len(image)
    width = len(image[0]) if height > 0 else 0
    center_r = height / 2
    center_c = width / 2
    # calculate the half diagonal
    half_diagonal = ((center_r)**2 + (center_c)**2)**0.5
    # apply vignette to each pixel looping through rows and columns
    for r in range(height):
        for c in range(width):
            d = ((r - center_r)**2 + (c - center_c)**2)**0.5
            vignette_factor = 1 - (d / half_diagonal)**2
            pixel = image[r][c]
            pixel.red = int(pixel.red * vignette_factor)
            pixel.green = int(pixel.green * vignette_factor)
            pixel.blue = int(pixel.blue * vignette_factor)

    return True