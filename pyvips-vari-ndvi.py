# install with 'pip install numpy'
import numpy

# install with 'pip install pyvips'
import pyvips

# it is bundled with...
from colormaps import RdYlGn_lut

numpy.set_printoptions(threshold=numpy.inf)

# find min/max and histogram
def result_histogram(result):
  np_2d = numpy.ndarray(
    buffer=result.write_to_memory(),
    dtype=numpy.float32,
    shape=[result.height, result.width]
  )
  
  flat_result = np_2d.flatten()

  histogram = numpy.histogram(flat_result, bins=256)[0]
  return histogram


# Remaps value (that has an expected range of in_low to in_high) into a target range of to_low to to_high
def math_map_value(value, in_low, in_high, to_low, to_high):
  return to_low + (value - in_low) * (to_high - to_low) / (in_high - in_low)


def find_clipped_min_max(histogram, nmin, nmax):
  # histogram
  summed = sum(histogram)
  three_percent = summed * 0.03
  lower_sum = 0
  upper_sum = 0
  last_lower_i = 0
  last_upper_i = 0

  histogram_len = len(histogram)

  for i in range(histogram_len):
    # summing up values in lower_sum til the sum is >= 3% of the sum of all data values
    # last_lower_i will be the data position right before lower_sum summed equal to 3% of the sum of all data values
    if lower_sum < three_percent:
      lower_sum += histogram[i]
      last_lower_i = i

    # // the same with last_upper_i
    if upper_sum < three_percent:
      upper_sum += histogram[histogram_len - 1 - i]
      last_upper_i = histogram_len - 1 - i

  return {
    'nmin': math_map_value(last_lower_i, 0, 255, nmin, nmax),
    'nmax': math_map_value(last_upper_i, 0, 255, nmin, nmax)
  }

# return image bands depending of band_order
def bandsplit(image, band_order):
  if band_order == "GRN":
    second, first, third, alpha = image.bandsplit()
  else:
    first, second, third, alpha = image.bandsplit()
  
  return [first, second, third, alpha]

# apply image manipulation algebra
# VARI
def vari(image, band_order):
  r, g, b, alpha = bandsplit(image, band_order)
  index = (g - r) / (g + r - b)
  return [alpha, index]

# NDVI
def ndvi(image, band_order):
  r, g, nir, alpha = bandsplit(image, band_order)
  index = (nir - r) / (nir + r)
  return [alpha, index]


def apply_index(base, index):
  # load image
  image = pyvips.Image.new_from_file(base + ".png")

  # call index method
  if index == 'ndvi':
    alpha, result = ndvi(image, "RGN")
  elif index == 'vari':
    alpha, result = vari(image, "RGB")

  # it will be used to 'normalize' results
  histogram = result_histogram(result)
  clip_min_max = find_clipped_min_max(histogram, result.min(), result.max())

  # normalize min/max
  nmin = clip_min_max['nmin']
  nmax = clip_min_max['nmax']

  # apply image manipulation algebra to 'normalize' results
  result = ((result-nmin) / (nmax-nmin)) * 256

  # apply Look-Up-Table (LUT)
  rdylgn_image = pyvips.Image.new_from_array(RdYlGn_lut).bandfold()
  rgb = result.maplut(rdylgn_image)

  # save to file
  rgb.bandjoin(alpha).write_to_file(index + ".png")


apply_index('nir', 'ndvi')
apply_index('rgb', 'vari')