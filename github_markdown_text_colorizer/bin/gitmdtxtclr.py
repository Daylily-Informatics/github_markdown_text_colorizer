import cherrypy
import os
from PIL import Image, ImageDraw, ImageFont

class ImageServer:

    @cherrypy.expose
    def format_gh_text(self, txt="", bg_color="white", txt_color="black", 
                       length="100", width="100", font_size="20", 
                       font="arial", ret_type="link"):
        
        # Create image filename based on parameters (for caching)
        filename = f"{txt}_{bg_color}_{txt_color}_{length}_{width}_{font_size}_{font}.png"
        filepath = os.path.join('cache', filename)

        # Check if image is already cached
        if not os.path.exists(filepath):
            self.create_image(txt, bg_color, txt_color, int(length), int(width), 
                              int(font_size), font, filepath)

        # Return image or link
        if ret_type == "img":
            return cherrypy.lib.static.serve_file(filepath, "image/png")
        else:
            return cherrypy.url(filepath)

    def create_image(self, txt, bg_color, txt_color, length, width, 
                     font_size, font, filepath):
        # Create a new image with the given parameters
        img = Image.new("RGB", (width, length), color=bg_color)
        draw = ImageDraw.Draw(img)
        try:
            # Use a truetype font if available
            font = ImageFont.truetype(font, font_size)
        except IOError:
            # Fallback to default font
            font = ImageFont.load_default()
        
        # Draw the text
        draw.text((10, 10), txt, fill=txt_color, font=font)

        # Save the image
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        img.save(filepath)

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/cache': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'cache'
        }
    }
    cherrypy.quickstart(ImageServer(), '/', conf)
