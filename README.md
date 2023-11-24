# github_markdown_text_colorizer
Service to return images of text where the input text can have font, font size and color set.  Intended as a way to insert colorized and font configurable text into github markdown files. This will need to be hosted someplace accessible to GH to work.

# Install
Likely only will run on mac or linux.

## Clone this repo
  * currently not a pip installable package

## Environment
I'm a fan of conda.

```bash
conda create -n GMTC -c conda-forge python ipython pytest pip Pillow==9.5.0 cherrypy
```

# Run It

```bash
# cd to top level dir of cloned repo

conda activate GMTC
mkdir -p cache
python github_markdown_text_colorizer/bin/gitmdtxtclr3.py

```
Will output

```text
[23/Nov/2023:16:36:57] ENGINE Listening for SIGTERM.
[23/Nov/2023:16:36:57] ENGINE Listening for SIGHUP.
[23/Nov/2023:16:36:57] ENGINE Listening for SIGUSR1.
[23/Nov/2023:16:36:57] ENGINE Bus STARTING
[23/Nov/2023:16:36:57] ENGINE Started monitor thread 'Autoreloader'.
[23/Nov/2023:16:36:57] ENGINE Serving on http://127.0.0.1:8080
[23/Nov/2023:16:36:57] ENGINE Bus STARTED
```

# Development Notes
Start to first satisfying working draft ~50m.
* [Dev work running notes](github_markdown_text_colorizer/docs/chatgpt_convo.md)
