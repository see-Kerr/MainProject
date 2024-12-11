from PIL import Image
import numpy as np
import cv2

def get_black_pixels_in_portion(image_path, left=0, top=0, right=1, bottom=1):
    img = cv2.imread(image_path)
    w,h= img.shape[:2]
    # Open an image file
    with Image.open(image_path) as img:
        # Convert the image to RGB mode
        img = img.convert('RGB')
        # Get the pixel data
        pixels = img.load()

        black_pixel_count = 0
        black_pixels = []
        c=True
        #count=0
    
        for x in range(left, right):
            #print(right)
            for y in range(top,bottom):
                r, g, b = pixels[x, y]
            
                if r<120 and g<120 and b<120:
                    if(c):
                        Xst,Yst=x,y
                        c=False
                    black_pixel_count += 1
                    black_pixels.append((x-Xst,y-Yst)*np.array([0.12,0.15]))

    
        return black_pixels
def align(coords, ref, key):
    #min_y = min(coord[1] for coord in coords)
    max_y = max(coord[1] for coord in coords)
    min_y = min(coord[1] for coord in coords)
    if key in ["f","g","p","p","q","y","j"]:
       min_y = min(coord[1] for coord in coords)
       diff = (max_y+min_y)//2 
       if diff>=ref[1]:
           step = diff - ref[1]
           coords= np.add(coords,[0,-step])
       else:
           step=ref[1]-diff
           coords= np.add(coords,[0,step])
    elif(max_y>=ref[1]):
        step = max_y-ref[1]
        coords=np.add(coords,[0,-step])
    elif(max_y<ref[1]):
        step=ref[1]-max_y
        coords= np.add(coords,step)
    return coords
def GetImageDimensions(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        return width, height

def scaling(pixels,RefCoordinates):
    c=0
    for key in pixels:
        coords=pixels[key]
        max_y = max(coord[1] for coord in pixels[key])
        min_y = min(coord[1] for coord in pixels[key])

        max_ry = max(coord[1] for coord in RefCoordinates[c])
        min_ry = min(coord[1] for coord in RefCoordinates[c])

        height=abs((max_y)-(min_y))
        refheight=abs((max_ry)-(min_ry))
        step = refheight-height
        if step<0:
            scalingfactor = refheight/height
            pixels[key] = coords*np.array([scalingfactor,scalingfactor])
        else:
            scalingfactor = (height/refheight)
            pixels[key] = coords*np.array([scalingfactor,scalingfactor])
        c=c+1
        print(f"ORIGINAL:  {key} max:{max_y} min:{min_y}")
        print(f"REFERENCE: {key} max:{max_ry} min:{min_ry}")
    return pixels

def alignStraight(pixels):
    for key in pixels:
        coords=pixels[key]
        max_element = max(coords, key=lambda item: item[1])
        min_element = min(coords, key=lambda item: item[1])