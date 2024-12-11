from PIL import Image
import getPixel
def select_portion(image_path, left, top, right, bottom, output_path):
    # Open an image file
    with Image.open(image_path) as img:
        # Define the coordinates for the portion to be selected
        box = (left, top, right, bottom)
        # Crop the image using the defined box
        cropped_image = img.crop(box)
        # Save the cropped image
        cropped_image.save(output_path)
        print(f'Cropped image saved to {output_path}')


def getData(image_path):
    alpha=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","bl","bl","bl","bl"]
    #image_path = r"C:\Users\Piyush\Desktop\Code\Python_MiniProject\database\alphabets_config\Snehil5000.jpg"
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
            output_path = "C:\\Users\\Piyush\\Desktop\\MainMiniProject-main\\Python_MiniProject\\database\\alphabets_config\\{}.jpg".format(alpha[l])
            print(i)
            print(left,top)
            print(right,bottom)
            select_portion(image_path,left,top,right,bottom,output_path)
            l=l+1
            left=right+w+10
            right=right+r
        top=bottom+h+10
        bottom=bottom+b+10
        left,right=w,r

