import pygame

#n is the number of columns in the source image
def spriteSheetToList(sourceImage, n):
    imageList = []
    sourceRect = sourceImage.get_rect()
    #width and height of each frame
    w = sourceRect.width/n
    h = sourceRect.height

    for i in range(n):
        subImage = sourceImage.subsurface(pygame.Rect((w*i,0),(w,h)))

        imageList.append(subImage)
        
    return imageList
