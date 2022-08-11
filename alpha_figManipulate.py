from PIL import Image, ImageDraw, ImageFont
from PIL import PSDraw

import math

from PIWordCloud import PI

def makeVignette(thisPI):

    title_short_side = 200

    photo_folder = 'data/photos/'

    photo_raw = Image.open(photo_folder + thisPI.lastName + thisPI.firstName[0] + ".jpeg")

    if photo_raw.width < photo_raw.height:
        vignette_is_landscape = 1
    else:
        vignette_is_landscape = 0

    img_wordcloud = Image.open('results/220807/' + thisPI.lastName + '.png')

    if vignette_is_landscape:
        vignette_height = img_wordcloud.height
        photo_height = math.ceil(vignette_height)
        photo_width = math.ceil(photo_height/photo_raw.height*photo_raw.width)
        title_long_side = img_wordcloud.height
        vignette_width = img_wordcloud.width+photo_width+title_short_side

    else:
        vignette_width = img_wordcloud.width
        photo_width = math.ceil(vignette_width)
        photo_height = math.ceil(photo_width/photo_raw.width*photo_raw.height)
        title_long_side = img_wordcloud.width
        vignette_height = img_wordcloud.height+photo_height+title_short_side    

    # ------ Resize
   
    photo = photo_raw.resize((photo_width, photo_height))

    # ------- Create text

    title = thisPI.firstName.upper() + " " + thisPI.lastName.upper()

    img_title = Image.new("RGBA", (title_long_side,title_short_side), color=(255,255,255))
    # Image is converted into editable form using
    # Draw function and assigned to d1
    img_draw = ImageDraw.Draw(img_title)
    # Font selection and size selection
    myFont = ImageFont.truetype("Arial.ttf", 200)
    title_size = myFont.getsize(title)
    myFont = ImageFont.truetype("Arial.ttf", math.floor(title_long_side*200/title_size[0]))


    # Decide the text location, color and font
    #d1.text((65, 10), "Sample text", fill =(255, 0, 0),font=myFont)
    img_draw.text((title_long_side/2, 0), title, align="center",anchor='ma', fill =(0, 0, 0),font=myFont)

    if vignette_is_landscape:
        img_title = img_title.rotate(angle=90,expand=True)

    # show and save the image
    #img.show()
    #img_title.save("title.png")


    # -------  Merge
    image_vignette = Image.new("RGBA", (vignette_width,vignette_height))
    image_vignette.paste(img_wordcloud)

    if vignette_is_landscape:

        image_vignette.paste(photo, (img_wordcloud.width, 0))
        image_vignette.paste(img_title,(img_wordcloud.width+photo_width,0))

    else:
        image_vignette.paste(photo, (0, img_wordcloud.height))
        image_vignette.paste(img_title,(0,img_wordcloud.height+photo_height))

    image_vignette.save("results/vignettes/" + thisPI.lastName + ".png")


if __name__ == "__main__":

    thisPI = PI("Rodriguez-Verdugo", "Alejandra")
    makeVignette(thisPI)