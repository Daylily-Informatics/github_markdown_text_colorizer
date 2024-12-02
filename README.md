# [Text To Styled & Colorized Image Service](https://gtc.dyly.bio)
Service to return images of specified text where text color, bg color, font and font size can be configured.  Images may be generated via the service, or dyanmically requested and used in `<img />` tags. <img src="https://gtc.dyly.bio/format_gh_text?txt=this+is+dynamic%2C+and+check+out+these+0%27s&bg_color=%239e0a72&txt_color=%2361edff&font=Monoid-Regular-HalfTight-Dollar-0-1-l&font_size=22&width=249&ret_type=img" />, which looks like this `<img src="https://gtc.dyly.bio/format_gh_text?txt=this+is+dynamic%2C+and+check+out+these+0%27s&bg_color=%239e0a72&txt_color=%2361edff&font=Monoid-Regular-HalfTight-Dollar-0-1-l&font_size=22&width=249&ret_type=img" />`, you can generate these urls [here](https://gtc.dyly.bio).

# Quickest Start
## Demo Service
_this service has no promises re:uptime! run your own service if you require high reliability_

### [https://gtc.dyly.bio](https://gtc.dyly.bio)
  * This service is running the current version of this repo. You may create and download images, or experiment with embedding them.

<img width="1243" alt="fglass" src="https://github.com/Daylily-Informatics/github_markdown_text_colorizer/assets/4713659/cc1ddbbb-0668-49a6-9e7c-d23e1f3874c0">


#### Embedding
> Enter values via the UI and get your embeddable link.
##### UI
<img width="1311" alt="fgembed" src="https://github.com/Daylily-Informatics/github_markdown_text_colorizer/assets/4713659/539506d9-78c9-4ccf-ac45-0ff9371da767">

##### Dynamically Generated Img Using Link Generated Above

> Use in markdown `<img src="https://gtc.dyly.bio/format_gh_text?txt=Embedding&bg_color=%23121111&txt_color=%2309caf1&font=Monoid-Regular-HalfTight-Dollar-0-1-l&font_size=20&width=140&ret_type=img" /> `

  Using The Link Produced Above

  <img src="https://gtc.dyly.bio/format_gh_text?txt=Embedding&bg_color=%23121111&txt_color=%2309caf1&font=Monoid-Regular-HalfTight-Dollar-0-1-l&font_size=20&width=140&ret_type=img" />

  Changing The Link Text & Color

  <img src="https://gtc.dyly.bio/format_gh_text?txt=Embedding+W%2FColor&bg_color=%237c66ea&txt_color=%23d1e821&font=Monoid-Regular-HalfTight-Dollar-0-1-l&font_size=20&width=228&ret_type=img" />


  Change The Font, Colors, Size
  
  <img src="https://gtc.dyly.bio/format_gh_text?txt=Embedding+W%2FColor&bg_color=%2315e595&txt_color=%236721e8&font=arial&font_size=24&width=249&ret_type=img" />
  
... you get the idea

##  <img src="https://gtc.dyly.bio/format_gh_text?txt=Embedding+W%2FColor&bg_color=%2315e595&txt_color=%236721e8&font=arial&font_size=24&width=249&ret_type=img" alt=xxx />



# Install And Run Service Yourself (advised for dynamic use)
Likely only will run on mac or linux.

## Clone this repo
```bash
git clone git@github.com:Daylily-Informatics/github_markdown_text_colorizer.git
cd github_markdown_text_colorizer
```

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
python github_markdown_text_colorizer/bin/gitmdtxtclr3.py 0.0.0.0 8080 https://PUBLIC_IP # :<PORT> will be appended

```
Will output

```text
[23/Nov/2023:16:36:57] ENGINE Listening for SIGTERM.
[23/Nov/2023:16:36:57] ENGINE Listening for SIGHUP.
[23/Nov/2023:16:36:57] ENGINE Listening for SIGUSR1.
[23/Nov/2023:16:36:57] ENGINE Bus STARTING
[23/Nov/2023:16:36:57] ENGINE Started monitor thread 'Autoreloader'.
[23/Nov/2023:16:36:57] ENGINE Serving on https://127.0.0.1:8080
[23/Nov/2023:16:36:57] ENGINE Bus STARTED
```

# Next Steps

## Limtations
* [the demo server, gtc.dyly.bio](https://gtc.dyly.bio) is not intended for operational use.
* The fonts available have optimal font sizes, and when not set to these sizes, can look blurry.
* These can not be used in header tagged lines.


# Development Notes
Start to first satisfying working draft ~40m.
* [Dev work running notes](github_markdown_text_colorizer/docs/chatgpt_convo.md)
