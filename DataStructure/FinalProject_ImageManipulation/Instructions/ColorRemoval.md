8. Overview of Color Removal
Monochromatic colors are colors where the red, green, and blue values are all the same. One popular example of monochromatic colors is grayscale. To convert an image into grayscale, you read the red, green, and blue values and compute the brightness
brightness = 0.3 * red + 0.6 * green + 0.1 * blue
You then reassign the red, green, and blue attributes to this single value. Note that you leave the alpha value unchanged. Converting an image to grayscale does not affect its transparency.
The function mono is responsible for converting an image to monochrome, though it has two different versions depending on whether sepia is True or False. You will approach this function in two steps. First you will implement it assuming sepia is False.
You will add the code for the True option at the second step.
This function is fairly straightforward as you do not need to add or remove pixels from the image; you just change attributes. Therefore, it is a good warm-up for the rest of the project.
Next