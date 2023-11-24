import cherrypy
import os
import hashlib
from PIL import Image, ImageDraw, ImageFont
import textwrap



def find_system_fonts():
    # Common font directories
    font_directories = ["/usr/share/fonts", "/usr/local/share/fonts", "/Library/Fonts", "~/Library/Fonts", "/Windows/Fonts"]
    ttf_fonts = []

    for directory in font_directories:
        # Expand user and environment variables in the path
        directory = os.path.expanduser(os.path.expandvars(directory))

        if os.path.isdir(directory):
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith(".ttf"):
                        ttf_fonts.append(os.path.join(root, file))

    return ttf_fonts

class ImageServer:

    @cherrypy.expose
    def format_gh_text(self, txt="", bg_color="white", txt_color="black", 
                       width="100", font_size="20", font="arial", ret_type="link"):
        
        # Convert string width and font_size to integers
        width = int(width)
        font_size = int(font_size)

        # Create a hash of the parameters
        hash_input = f"{txt}_{bg_color}_{txt_color}_{width}_{font_size}_{font}".encode('utf-8')
        filename_hash = hashlib.md5(hash_input).hexdigest()
        filename = f"{filename_hash}.png"
        filepath = os.path.join('cache', filename)

        # Check if image is already cached
        if not os.path.exists(filepath):
            self.create_image(txt, bg_color, txt_color, width, font_size, font, filepath)

        # Return image or link
        if ret_type == "img":
            return cherrypy.lib.static.serve_file(os.path.abspath(filepath), "image/png")
        else:
            return cherrypy.url(filepath)

    def create_image(self, txt, bg_color, txt_color, width, font_size, font, filepath):
        # Create a font object
        try:
            font = ImageFont.truetype(font, font_size)
        except IOError:
            font_files = find_system_fonts()
            fonts = []
            for i in font_files:
                fonts.append(os.path.basename(i).rstrip('.ttf'))

            if font in ['arial']:
                font = ImageFont.load_default()
            else:
                raise Exception(f"\n\nThe font you specified: {font} ... does not have a matching ttf file. Valid choices are: {fonts}.\n\n")

        # Create a dummy image to calculate text size
        dummy_img = Image.new("RGB", (width, 100))
        dummy_draw = ImageDraw.Draw(dummy_img)

        # Calculate the average width of a character
        avg_char_width = sum(font.getsize(char)[0] for char in txt) / len(txt)

        # Estimate the number of characters per line
        chars_per_line = max(1, int(width / avg_char_width))

        # Wrap text
        wrapped_text = textwrap.fill(txt, width=chars_per_line)
        lines = wrapped_text.split('\n')

        # Calculate the height of a single line
        line_height = dummy_draw.textbbox((0, 0), 'Ay', font=font)[3] + 5  # Adding a small buffer

        # Calculate image height based on number of lines
        img_height = line_height * len(lines) + 20  # Adding extra space for padding

        # Create the actual image
        img = Image.new("RGB", (width, img_height), color=bg_color)
        draw = ImageDraw.Draw(img)

        # Draw each line of text
        y_text = 10
        for line in lines:
            draw.text((10, y_text), line, font=font, fill=txt_color)
            y_text += line_height

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
