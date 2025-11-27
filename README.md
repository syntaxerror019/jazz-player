# Jazz Player

A slick, easy-to-use web interface for the [radio-browser.info](https://www.radio-browser.info/) api interface.

![jazz radio screenshot](/screenshots/ss.png)

## Features

A curated list of the best jazz stations-- straight from the pros.

- Easy access and 24/7 reliable jazz favorites.
- Slick bootstrap-based Web interface easy for anybody to interface
- mpc playback definition: Low-level and lightweight.
- Favorite a station and come back to it later!
- Will run on any hardware: RPi, Laptop, PC
- Support on various OS. Windows, Linux, MacOS.

## Installation

```bash
git clone https://github.com/syntaxerror019/jazz-player.git
cd jazz-player/src

# Install requirements
pip install -r requirements.txt

# Install mpc and mpd
sudo apt-get install mpc mpd

# Run the flask app
python3 app.py

# Visit the web interface
http://localhost:8080

# Change the port and host of the app
# Edit main.py and change the following lines:
# app.run(host="0.0.0.0", port=8080, debug=False)
# app.run(host="192.168.1.100", port=5000, debug=False)
```