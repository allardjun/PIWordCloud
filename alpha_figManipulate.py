from PIL import Image, ImageDraw, ImageFont
from PIL import PSDraw
from os.path import exists
import math
from random import randint, choice

from PIWordCloud import PI

def makeVignette(thisPI):

    title_short_side = 200

    img_wordcloud = Image.open('results/220807/' + thisPI.lastName + '.png')

    photo_folder = 'data/photos/'

    path_to_photo = photo_folder + thisPI.lastName + thisPI.firstName[0] + ".jpeg"
    if exists(path_to_photo):
        photo_true = 1
        photo_raw = Image.open(path_to_photo)

        if photo_raw.width < photo_raw.height:
            vignette_is_landscape = 1
        else:
            vignette_is_landscape = 0

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
    else:
        photo_true = 0
        vignette_is_landscape = randint(0,1)
        if vignette_is_landscape:
            vignette_height = img_wordcloud.height
            title_long_side = img_wordcloud.height
            vignette_width = img_wordcloud.width+title_short_side

        else:
            vignette_width = img_wordcloud.width
            title_long_side = img_wordcloud.width
            vignette_height = img_wordcloud.height+title_short_side    




    # ------- Create text

    title = thisPI.firstName.upper() + " " + thisPI.lastName.upper() + "@UCI"

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
        img_title = img_title.rotate(angle=-90,expand=True)

    # -------  Merge
    image_vignette = Image.new("RGBA", (vignette_width,vignette_height))
    image_vignette.paste(img_wordcloud)

    if vignette_is_landscape:
        if photo_true:
            image_vignette.paste(photo, (img_wordcloud.width, 0))
            image_vignette.paste(img_title,(img_wordcloud.width+photo_width,0))
        else:
            image_vignette.paste(img_title,(img_wordcloud.width,0))

    else:
        if photo_true:
            image_vignette.paste(photo, (0, img_wordcloud.height))
            image_vignette.paste(img_title,(0,img_wordcloud.height+photo_height))
        else:
            image_vignette.paste(img_title,(0,img_wordcloud.height))


    image_vignette.save("results/vignettes/" + thisPI.lastName + ".png")


if __name__ == "__main__":

    thisPI = PI("Emerson", "J")
    makeVignette(thisPI)