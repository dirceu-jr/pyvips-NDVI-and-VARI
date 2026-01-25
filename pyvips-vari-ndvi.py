import sys

# Install with 'pip install pyvips'
import pyvips


# Apply image manipulation algebra
# VARI
def vari(image):
  r, g, b, alpha = image.bandsplit()
  index = (g - r) / (g + r - b)
  return [alpha, index]


# NDVI
def ndvi(image):
  r, g, nir, alpha = image.bandsplit()
  index = (nir - r) / (nir + r)
  return [alpha, index]


# Apply index with Contrast Stretching
def apply_index(input_file, index):
  # Load image
  image = pyvips.Image.new_from_file('./' + input_file)

  # Call index method
  if index == 'NDVI':
    alpha, result = ndvi(image)
  elif index == 'VARI':
    alpha, result = vari(image)

  # Find min/max and percentiles
  min_val = result.min()
  max_val = result.max()

  if max_val == min_val:
    nmin = min_val
    nmax = max_val
  else:
    # Scale to 0-65535 to use percent()
    factor = 65535.0 / (max_val - min_val)
    scaled = (result - min_val) * factor
    scaled_ushort = scaled.cast("ushort")

    nmin = min_val + scaled_ushort.percent(3) / factor
    nmax = min_val + scaled_ushort.percent(97) / factor

  if nmax == nmin:
    result = result.new_from_image(0)
  else:
    # Apply image manipulation algebra to 'normalize' results
    # Scale to 0-255 for 8-bit LUT
    result = ((result - nmin) / (nmax - nmin)) * 255

  # Apply Look-Up-Table (LUT)
  rdylgn_image = pyvips.Image.new_from_file('./rdylgn.png')

  rgb = result.maplut(rdylgn_image)

  # Save to file
  rgb[0:3].bandjoin(alpha).write_to_file('./' + index.lower() + '.png')


apply_index(sys.argv[1], sys.argv[2])
