import numpy
from PIL import Image as im
from PIL import ImageFilter as im_f
from PIL import ImageEnhance as im_e

#User prompts
image = im.open(input('Enter path to the file (Include file extension): '))
resolution = int(input('Specify the resolution width starting point (400 to 800 values reccomended): ')) - 50
output = input('Enter output filename and path: ')

#Resolution setter
baseWidth = []
for k in range (0, 5):
    resolution = resolution + 50
    baseWidth.append(resolution)

#First mold loop (Specified by user)
for j in range (0, 3):

    #Prevent loading of old image thus canceling the effect
    if j > 0:
        image = im.open(output)

    #Second mold loop (resolution iterations)
    for i in range(0,5):

        #Prevent loading of old image thus canceling the effect
        if i > 0:
            image = im.open(output)

        #Scale resolution of image
        widthSize = (baseWidth[i]/float(image.size[0]))
        heightSize = int((float(image.size[1])*float(widthSize)))
        image = image.resize((baseWidth[i],heightSize), im.Resampling.LANCZOS)

        #Convert image to 'YCbCr'
        ycbcr = image.convert('YCbCr')


        Y = 0
        Cb = 1
        Cr = 2

        YCbCr=list(ycbcr.getdata())
        imYCbCr = numpy.reshape(YCbCr, (image.size[1], image.size[0], 3))
        imYCbCr = imYCbCr.astype(numpy.uint8)

        #Split 'YCbCr' channels
        (y, cb, cr) = ycbcr.split()


        #Apply blur to Cb and Cr to achieve color bleed
        blur_cr = cr.filter(im_f.GaussianBlur(1.85))
        blur_cb = cb.filter(im_f.GaussianBlur(1.85))


        

        #Merge channels back together
        imageMerge = im.merge('YCbCr', (y, blur_cb, blur_cr))

        #Apply sharpness and save image
        enchancer = im_e.Sharpness(imageMerge)
        enchancer.enhance(2).save(output, quality = 43)

        #Open saved image and add slight blur
        ycbcr4 = im.open(output)
        ycbcr4.filter(im_f.GaussianBlur(0.6)).save(output)
    enchancer = im_e.Color(imageMerge)
    enchancer.enhance(1.02).save(output)

