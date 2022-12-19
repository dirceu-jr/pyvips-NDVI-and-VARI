# pyvips NDVI and VARI

How to apply NDVI (Normalized Difference Vegetation Index) in NIR (near-infrared) orthophotos and VARI (Visible Atmospherically Resistant Index) in RGB orthophotos using **[libvips](https://libvips.github.io/libvips/)** image processing library and their [Python binding](https://github.com/libvips/pyvips).

## What is NDVI and VARI?

NDVI and VARI are simple graphical indicators that can be used to analyze remote sensing measurements, assessing whether or not the target being observed contains live green vegetation. It is applied using simple algebra with the bands and in each pixel of an input image.

The NDVI is calculated from these individual measurements as follows: `NDVI = (NIR - Red) / (NIR + Red)`

And `VARI = (Green - Red) / (Green + Red - Blue)`

## What is libvips?

libvips is a fast and open source image processing library.

## Prerequisites

Install [libvips](https://libvips.github.io/libvips/install.html) and [Python](https://www.python.org/). Then use PIP to install 'pyvips' and 'numpy' packages:

```
pip install pyvips
pip install numpy
```

## Run

OK? Run the program:

```
python3 pyvips-vari-ndvi.py nir.png NDVI
python3 pyvips-vari-ndvi.py rgb.png VARI
```

_nir.png_ and _rgb.png_ orthophoto thumbnails will be processed and resulting _NDVI.png_ and _VARI.png_ will be saved.

OBS: The code was made to process images with "alpha" (transparency) layer/band. JPG? Export to PNG before.

## Results

### RGB → VARI
<img src="https://github.com/dirceu-jr/pyvips-NDVI-and-VARI/blob/master/rgb.png" width="400" valign="middle" /> *→* <img src="https://github.com/dirceu-jr/pyvips-NDVI-and-VARI/blob/master/vari.png" width="400" valign="middle" />

### NIR → NDVI
<img src="https://github.com/dirceu-jr/pyvips-NDVI-and-VARI/blob/master/nir.png" width="400" valign="middle" /> *→* <img src="https://github.com/dirceu-jr/pyvips-NDVI-and-VARI/blob/master/ndvi.png" width="400" valign="middle" />
