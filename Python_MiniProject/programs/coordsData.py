import getPixel
from PIL import Image
def getData(image_path):
    
#set dimensions
    width,height = getPixel.GetImageDimensions(image_path)
    w,h = width*0.02,height*0.07
    left,top=w,h
    r=(width/10)*0.977
    b=(height/3)-25
    right,bottom=r,b
    coordinates=[]
    l,u=0,1
    for j in range (1,4):
        #print(top,bottom)
        for i in range(1,11):
            coordinates.append(getPixel.get_black_pixels_in_portion(image_path,int(left),int(top),int(right),int(bottom)))
            l=l+1
            u=u+1
            left=right+w+10
            right=right+r
        top=bottom+h+10
        bottom=bottom+b+10
        left,right=w,r
    #print(coordinates)
    return coordinates
    
    