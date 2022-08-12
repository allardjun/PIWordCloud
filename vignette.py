from PIL import Image, ImageDraw, ImageFont
from PIL import PSDraw
from os.path import exists
import math
from random import randint, choice

from PIWordCloud import PI

def makeVignette(thisPI):

    path_to_wordcloud = 'results/220807/' + thisPI.lastName + '.png'

    if exists(path_to_wordcloud):
        img_wordcloud = Image.open(path_to_wordcloud)
    else:
        return

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

        else:
            vignette_width = img_wordcloud.width
            photo_width = math.ceil(vignette_width)
            photo_height = math.ceil(photo_width/photo_raw.width*photo_raw.height)
            title_long_side = img_wordcloud.width

        # ------ Resize
        photo = photo_raw.resize((photo_width, photo_height))
    else:
        photo_true = 0
        vignette_is_landscape = randint(0,1)
        if vignette_is_landscape:
            vignette_height = img_wordcloud.height
            title_long_side = img_wordcloud.height

        else:
            vignette_width = img_wordcloud.width
            title_long_side = img_wordcloud.width

    # ------- Create text

    title = thisPI.firstName.upper() + " " + thisPI.lastName.upper() + "@UCI"

    img_title = Image.new("RGBA", (title_long_side,400), color=(255,255,255))
    # Image is converted into editable form using
    # Draw function and assigned to d1
    img_draw = ImageDraw.Draw(img_title)
    # Font selection and size selection
    myFont = ImageFont.truetype("Arial.ttf", 200)
    title_size = myFont.getbbox(title)
    print(title_size)

    myFont = ImageFont.truetype("Arial.ttf", math.floor(title_long_side*200/title_size[2]))

    title_short_side = myFont.getbbox(title)[3]+10
    print(title_short_side)
    if photo_true == 1:
        if vignette_is_landscape:
            vignette_width = img_wordcloud.width+photo_width+title_short_side
        else:
            vignette_height = img_wordcloud.height+photo_height+title_short_side    
    else:
        if vignette_is_landscape:
            vignette_width = img_wordcloud.width+title_short_side
        else:
            vignette_height = img_wordcloud.height+title_short_side    

    # Decide the text location, color and font
    #d1.text((65, 10), "Sample text", fill =(255, 0, 0),font=myFont)
    img_draw.text((title_long_side/2, 0), title, align="center",anchor='ma', fill =(0, 0, 0),font=myFont)
    img_title_cropped = img_title.crop((0,0,title_long_side,title_short_side))
 
    if vignette_is_landscape:
        img_title_cropped = img_title_cropped.rotate(angle=-90,expand=True)

    # -------  Merge
    image_vignette = Image.new("RGBA", (vignette_width,vignette_height))
    image_vignette.paste(img_wordcloud)

    if vignette_is_landscape:
        if photo_true:
            image_vignette.paste(photo, (img_wordcloud.width, 0))
            image_vignette.paste(img_title_cropped,(img_wordcloud.width+photo_width,0))
        else:
            image_vignette.paste(img_title_cropped,(img_wordcloud.width,0))

    else:
        if photo_true:
            image_vignette.paste(photo, (0, img_wordcloud.height))
            image_vignette.paste(img_title_cropped,(0,img_wordcloud.height+photo_height))
        else:
            image_vignette.paste(img_title_cropped,(0,img_wordcloud.height))


    image_vignette.save("results/vignettes/" + thisPI.lastName + ".png")


if __name__ == "__main__":

    thisPI = PI("Yu", "Jin")
    makeVignette(thisPI)