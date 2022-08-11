from PIL import Image
from PIL import PSDraw

image_folder = 'data/photos/'

im = Image.open(image_folder + "ShiX.jpeg")

out = im.resize((128, 128))

out.show()


if 0:


    with Image.open("hopper.ppm") as im:
        title = "hopper"
        box = (1 * 72, 2 * 72, 7 * 72, 10 * 72)  # in points

        ps = PSDraw.PSDraw()  # default is sys.stdout or sys.stdout.buffer
        ps.begin_document(title)

        # draw the image (75 dpi)
        ps.image(box, im, 75)
        ps.rectangle(box)

        # draw title
        ps.setfont("HelveticaNarrow-Bold", 36)
        ps.text((3 * 72, 4 * 72), title)

        ps.end_document()

    def merge(im1, im2):
        w = im1.size[0] + im2.size[0]
        h = max(im1.size[1], im2.size[1])
        im = Image.new("RGBA", (w, h))

        im.paste(im1)
        im.paste(im2, (im1.size[0], 0))

        return im