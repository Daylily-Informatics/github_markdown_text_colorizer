import cherrypy
import os
import sys
import hashlib
from PIL import Image, ImageDraw, ImageFont
import textwrap


if len(sys.argv) > 1:
    root_url = sys.argv[1]
    if not root_url.endswith('/'):
        root_url += '/'
else:
    root_url = "http://localhost:8081" + '/'

def find_system_fonts():
    # Common font directories
    font_directories = ["/usr/share/fonts", "/usr/local/share/fonts", "/Library/Fonts", "~/Library/Fonts", "/Windows/Fonts", "github_markdown_text_colorizer/fonts/"]
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

def get_system_fonts():
    font_files = find_system_fonts()
    fonts = ['default']
    for i in font_files:
        fonts.append(os.path.basename(i).split('.ttf')[0])

    return fonts


class ImageServer:

    @cherrypy.expose
    def format_gh_text(self, txt="", bg_color="white", txt_color="black", 
                       width="100", font_size="20", font="Monoid-Regular-HalfTight-Dollar-0-1-l", ret_type="link"):
        
        if len(txt) < 1 or len(txt) > 3333:
            raise Exception("Text must be between 1 and 3333 characters long")
        
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
            #font_files = find_system_fonts()
            #fonts = ['default']
            #for i in font_files:
            #    fonts.append(os.path.basename(i).split('.ttf')[0])
            fonts = get_system_fonts()  
            if font in ['default']:
                font = ImageFont.load_default()
            else:
                try:
                    font_path = f"github_markdown_text_colorizer/fonts/{font}.ttf"  # Update this path as necessary
                    font = ImageFont.truetype(font_path, font_size)
                except Exception as e:
                   raise Exception(f"\n\nThe font you specified: {font} ... does not have a matching ttf file. Valid choices are: {fonts}.\n\n{e}\n\n")

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

    @cherrypy.expose
    def _ret_header(self):
        ret_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>ratios</title>
            <style>
                body {
                    font-family: 'Dosis', Arial, sans-serif;
                    background-color: #111111; /* Very dark background */
                    color: #ffffff; /* White text */
                    text-align: center;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh; /* Center content vertically */
                }
                .container {
                    margin-top: 20px;
                    background-color: #0b131a; /* Dark blue/gray background */
                    padding: 20px;
                    border-radius: 5px;
                    width: 83%;
                }
                .field {
                    font-size: 36px;
                    font-weight: bold;
                    padding: 20px;
                    color: #ffffff; /* White text for fields */
                }
                #ratio {
                    font-size: 48px;
                    font-weight: bold;
                    margin: 20px 0;
                    color: #ffffff; /* White text for ratio */
                }
                button {
                    font-size: 36px;
                    padding: 10px 20px; /* Adjusted padding to shrink button size by 50% */
                    background-color: #e74c3c; /* Dark red button color */
                    color: #ffffff; /* White text for button */
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    transition: background-color 0.3s ease; /* Smooth background color transition */
                }
                button:hover {
                    background-color: #ff5733; /* Brighter red on hover for the button */
                }
                .date {
                    font-size: 24px;
                    color: #444444; /* Dark gray text for date */
                    margin-top: 20px;
                }
            </style>
            <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Dosis:wght@300&display=swap">

        """
    
        return ret_html
    
    @cherrypy.expose
    def index(self):
        
        font_opts = "<select style='width:80%;' name=font ><option value='Monoid-Regular-HalfTight-Dollar-0-1-l' selected>Monoid-Regular-HalfTight-Dollar-0-1-l</option>"
        for i in sorted(get_system_fonts()): 
            font_opts += f"<option value='{i}'>{i}</option>"
        font_opts += "</select>"
        
        ret_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>GitHub Markdown Text Colorizer</title>
       <script>
        function updateRGBValue() {
            var hexColor = document.getElementById('bg_color').value;
            var rgbColor = hexToRGB(hexColor);
            document.getElementById('bg_color').style.backgroundColor = rgbColor;
            document.getElementById('color_value').textContent = rgbColor;
            document.getElementById('color_value').style.color = rgbColor;  
        }
 function updateRGBValue2() {
            var hexColor2 = document.getElementById('txt_color').value;
            var rgbColor2 = hexToRGB(hexColor2);
            document.getElementById('txt_color').style.backgroundColor = rgbColor2;
            document.getElementById('color_value2').textContent = rgbColor2;
            document.getElementById('color_value2').style.color = rgbColor2;

        }
        function hexToRGB(hex) {
            var r = parseInt(hex.substring(1, 3), 16);
            var g = parseInt(hex.substring(3, 5), 16);
            var b = parseInt(hex.substring(5, 7), 16);
            return "rgb(" + r + ", " + g + ", " + b + ")";
        }
    </script>
            <style>
                body {
                    font-family: 'Dosis', Arial, sans-serif;
                    background-color: #111111; /* Very dark background */
                    color: #ffffff; /* White text */
                    text-align: center;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh; /* Center content vertically */
                }
                .container {
                    background-color: #0b131a; /* Dark blue/gray background */
                    padding: 20px;
                    border-radius: 5px;
                    width: 90%;
                    display: flex;
                    justify-content: space-between;
                }
                .form-container, .result-container {
                    flex: 1;
                    margin: 10px;
                }
                .navigation a {
                    color: #ffffff; /* White text for navigation links */
                    padding: 10px 20px;
                    margin: 0 10px;
                    background-color: #0b131a; /* Dark blue/gray background for navigation links */
                    border-radius: 5px;
                    text-decoration: none;
                    transition: background-color 0.3s ease;
                }
                .navigation a:hover {
                    background-color: #e74c3c; /* Dark red background on hover for navigation links */
                }
                a {
                    color: #e74c3c; /* Red text for links */
                }
                button {
                    font-size: 20px;
                    padding: 10px 20px;
                    background-color: #e74c3c; /* Dark red button color */
                    color: #ffffff; /* White text for button */
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    transition: background-color 0.3s ease; /* Smooth background color transition */
                }
                button:hover {
                    background-color: #ff5733; /* Brighter red on hover for the button */
                }
                .form-field {
                    margin: 10px 0;
                    color: #ffffff;
                }
                input, select {
                    padding: 10px;
                    border-radius: 5px;
                    border: 1px solid #ffffff;
                    background-color: #0b131a;
                    color: #ffffff;
                    width: 20%;
                }
                #requestUrl {
                    color: #e74c3c; /* URL text color */
                }
                .result-image {
                    max-width: 100%;
                    height: auto;
                }
            </style>
            <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Dosis:wght@300&display=swap">
        </head>
        <body>
            <div class="container">
                <div class="form-container" width=60% >
                    <h1><a href=https://github.com/Daylily-Informatics/github_markdown_text_colorizer>GitHub Markdown Text Colorizer</a></h1>
                    <div class="navigation">
                        <a href="https://github.com/Daylily-Informatics">Daylily Informatics</a>
                        <a href="https://github.com/Daylily-Informatics/img_stitcher_day">Tube Image Stitcher</a>
                        <a href="https://en.wikipedia.org/wiki/Petrichor">Petrichor</a>
                        
                    </div><br>
                    <h2>Two Use Cases</h2>
                    <ul>
                    <p> Create an image of your text, save the image, and use it elsewhere. 
                    <p> Formulate the markdown img tag, and use it in your markdown. 
                    </ul>
                    <br>
                    <hr>
                    <br><br>
                    <form style='text-align: inherit;' id="colorizerForm">
                        <div class="form-field">
                            <label for="txt">Text:</label>
                            <input style='width: 85%;' type="text" id="txt" name="txt" value="">
                        </div>
                        <div class="form-field">
                        <br>
                        <table width='100%' ><tr width=100% ><td width='50%' align=center >
                            <label for="bg_color" >Background Color: <small id="color_value" name="color_value" >rgb(255,255,255)</small></label>
                            <input type="color" id="bg_color" name="bg_color" value="#FFFFFF" onchange="updateRGBValue()" >

                 </td><td width='50%' align=center >
                            <label for="txt_color">Text Color: <small id="color_value2" name="color_value2" >rgb(0,0,0)</small></label>
                            <input type="color" id="txt_color" name="txt_color" value="#000000"  onchange="updateRGBValue2()" />
</td></tr></table>
<br>
                        </div>
                         <div class="form-field">
                          <table width=100% ><tr width=100% ><td width='70%'>

                            <label for="font">Font:</label>
                            """+font_opts+"""
                        </td><td width=30%'  >
                           <label for="font_size">Font Size:</label>
                            <input type="text"   id="font_size" name="font_size" value="20">
                        </td></tr></table>
                        <br>
                        </div>
                       <div class="form-field">
                          <table width=100% ><tr width=100% ><td width='50%'>

                        <label for="width">Img Width:</label>
                        <input type="text" id="width" name="width" value="100">
                        </td><td width='50%'>
                            <label for="ret_type">Return Type:</label>
                            <select style='width: 50%;' id="ret_type" name="ret_type">
                                <option value="img">Image</option>
                                <option value="link">Link</option>
                            </select>
                        </td></tr></table>
                        <br>
                        </div>
                        <div class="form-field" style='align:center;' >
                        <button style='align:center;' type="button" onclick="submitForm()">Submit</button>
                        </div>
                    </form>
                </div>
                <div class="result-container" >
                <br><br><br><br>
                <p>NOTICE: this is a proof of concept & there are no guaruntees re: availability.  <br><a href=https://github.com/Daylily-Informatics/github_markdown_text_colorizer >__for routine use, set up your own service__</a></p>

                            <p id="requestUrl"></p>
                    <p id="requestUrl2"></p>

                    <img id="resultImage" class="result-image" />
                </div>
             </div>

            <script>
                function submitForm() {
                    const form = document.getElementById('colorizerForm');
                    const formData = new FormData(form);
                    const queryString = new URLSearchParams(formData).toString();
                    const url = `format_gh_text?${queryString}`;

                    // Update the URL text
                    document.getElementById('requestUrl').textContent = 'Request URL :: """+root_url+"""' + url;
                    document.getElementById('requestUrl2').textContent = 'Use in markdown :: <img src=\""""+root_url+"""' + url + '\" />';
                    // Assuming the server responds with an image or a link to an image
                    if (formData.get('ret_type') === 'img') {
                        // Load and display the image
                        const img = document.getElementById('resultImage');
                        img.src = url;
                    } else {
                        // Open the link in a new tab/window
                        window.open(url, '_blank');
                    }

                    return false; // Prevent default form submission
                }
            </script>
        </body>
        </html>
        """
        
        return ret_html


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
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 80,
    })
    cherrypy.quickstart(ImageServer(), '/', conf)
