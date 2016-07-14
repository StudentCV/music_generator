# Music Generator

A simple Program which runs edge detection on a preformatted sheet of paper to generate music via the Sonic Pi Application.

The rows of the table are equivalent to a note, whereas each column indicates whether the note should be played or not.

Currently work in progress!

To get this project up and running first install dependencies via [this](https://github.com/StudentCV/guides/blob/master/rpi3_image_processing.md) guide.
Furthermore you need Sonic Pi which comes with every current raspbian image, but you will also need to install the Ruby gem `sonic-pi-cli` (e.g. via `gem install sonic-pi-cli`).

If you want to try it out, just print the tamplate `sheet.pdf`, color some cells black and point your camera at it.
*Note: Sonic Pi must be running for this to work otherwise the output of the program can not be parsed by it.*
