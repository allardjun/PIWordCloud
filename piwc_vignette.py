from PIL import Image, ImageDraw, ImageFont
from PIL import PSDraw
from os.path import exists
import math
from random import randint, choice

from piwc_PIWordCloud import PI

def make_vignette(thisPI):
    '''Assembles a wordcloud image, photo, and PI name into a single image'''

    '''There are NINE cases: {wide photo, tall photo, no photo} x {non-MCSB, MCSB w long name, MCSB with short name}'''
    
    # ---------- DIRECTORIES FOR INPUT ----------

    path_to_wordcloud = 'results/220807/' + thisPI.lastName + '.png' # for wordcloud input
    photo_folder      = 'data/photos/'
    logo_file         = 'data/mcsb_logo_for_vignette-01.png'

    if exists(path_to_wordcloud):
        img_wordcloud = Image.open(path_to_wordcloud)
    else:
        return

    img_logo = Image.open(logo_file)
    

    # ---------- DETERMINE OUTPUT ATTRIBUTES SET BY PHOTO STATS

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

    if thisPI.isMCSB==1:
        title = thisPI.firstName.upper() + " " + thisPI.lastName.upper()
    else:
        title = thisPI.firstName.upper() + " " + thisPI.lastName.upper() + "@UCI"
    if len(thisPI.firstName + thisPI.firstName) > 10:
        longNameTF = 1
    else:
        longNameTF = 0

    # ---- Find out the aspect ratio of the text ----
    # First make it 400 pixels tall
    img_title = Image.new("RGBA", (title_long_side,400), color=(255,255,255))
    # Image is converted into editable form using Draw function
    img_draw = ImageDraw.Draw(img_title)
    # Font selection and size selection
    myFont_guess = ImageFont.truetype("Arial.ttf", 200)
    title_size_guess = myFont_guess.getbbox(title)
    print(title_size_guess)

    if thisPI.isMCSB==0 or longNameTF==1: # in these cases, the logo will either not appear or appear on the wordcloud, so is not included in vignette size calc.

        myFont = ImageFont.truetype("Arial.ttf", math.floor(200*title_long_side/title_size_guess[2]))

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

    if thisPI.isMCSB==1 and longNameTF==0: # the name and logo will be co-aligned TODO
        name_ratio = title_size_guess[3]/title_size_guess[2]
        logo_ratio = img_logo.width/img_logo.height
        y_name = logo_ratio*name_ratio*title_long_side/(logo_ratio+name_ratio)
        y_logo = y_name
        x_name = logo_ratio*title_long_side/(logo_ratio+name_ratio)
        x_logo = name_ratio*title_long_side/(logo_ratio+name_ratio)

    # Decide the text location, color and font
    img_draw.text((title_long_side/2, 0), title, align="center",anchor='ma', fill =(0, 0, 0),font=myFont)
    img_title_cropped = img_title.crop((0,0,title_long_side,title_short_side))

    if vignette_is_landscape:
        img_title_cropped = img_title_cropped.rotate(angle=-90,expand=True)

    # -------  Merge the 2 or 3 images and save
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
    thisPI.isMCSB = 0
    make_vignette(thisPI)