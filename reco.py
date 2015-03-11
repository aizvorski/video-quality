"""
Video Quality Metrics
Copyright (c) 2015 Alex Izvorski <aizvorski@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
RECO: Relative Polar Edge Coherence

An excellent reduced-reference metric (need just one number from the source image to compare with).

This implementation follows closely the notation and terminology in the original paper, except that some of the kernels are reflected 
(probably due to y axis pointing down rather than up in images).

Cite:
Baroncini, V., Capodiferro, L., Di Claudio, E. D., & Jacovitti, G. (2009). The polar edge coherence: 
a quasi blind metric for video quality assessment. EUSIPCO 2009, Glasgow, 564-568.
"""

import numpy
from numpy import sqrt, pi
import scipy.ndimage.filters

def Laguerre_Gauss_Circular_Harmonic_3_0(size, sigma):
    x = numpy.linspace(-size/2.0, size/2.0, size)
    y = numpy.linspace(-size/2.0, size/2.0, size)
    xx, yy = numpy.meshgrid(x, y)
    
    r = numpy.sqrt(xx*xx + yy*yy)
    gamma = numpy.arctan2(yy, xx)
    l30 = - (1/6.0) * (1 / (sigma * sqrt(pi))) * numpy.exp( -r*r / (2*sigma*sigma)) * (sqrt(r*r/(sigma*sigma)) ** 3) * numpy.exp( -1j * 3 * gamma )
    return l30

def Laguerre_Gauss_Circular_Harmonic_1_0(size, sigma):
    x = numpy.linspace(-size/2.0, size/2.0, size)
    y = numpy.linspace(-size/2.0, size/2.0, size)
    xx, yy = numpy.meshgrid(x, y)
    
    r = numpy.sqrt(xx*xx + yy*yy)
    gamma = numpy.arctan2(yy, xx)
    l10 = - (1 / (sigma * sqrt(pi))) * numpy.exp( -r*r / (2*sigma*sigma)) * sqrt(r*r/(sigma*sigma)) * numpy.exp( -1j * gamma )
    return l10

"""
Polar edge coherence map
Same size as source image
"""
def pec(img):
    # TODO scale parameter should depend on resolution
    l10 = Laguerre_Gauss_Circular_Harmonic_1_0(17, 2)
    l30 = Laguerre_Gauss_Circular_Harmonic_3_0(17, 2)
    y10 = scipy.ndimage.filters.convolve(img, numpy.real(l10)) + 1j * scipy.ndimage.filters.convolve(img, numpy.imag(l10))
    y30 = scipy.ndimage.filters.convolve(img, numpy.real(l30)) + 1j * scipy.ndimage.filters.convolve(img, numpy.imag(l30))
    pec_map = - (numpy.absolute(y30) / numpy.absolute(y10)) * numpy.cos( numpy.angle(y30) - 3 * numpy.angle(y10) )
    return pec_map

"""
Edge coherence metric
Just one number summarizing typical edge coherence in this image.
"""
def eco(img):
    l10 = Laguerre_Gauss_Circular_Harmonic_1_0(17, 2)
    l30 = Laguerre_Gauss_Circular_Harmonic_3_0(17, 2)
    y10 = scipy.ndimage.filters.convolve(img, numpy.real(l10)) + 1j * scipy.ndimage.filters.convolve(img, numpy.imag(l10))
    y30 = scipy.ndimage.filters.convolve(img, numpy.real(l30)) + 1j * scipy.ndimage.filters.convolve(img, numpy.imag(l30))
    eco = numpy.sum( - (numpy.absolute(y30) * numpy.absolute(y10)) * numpy.cos( numpy.angle(y30) - 3 * numpy.angle(y10) ) )
    return eco

"""
Relative edge coherence
Ratio of ECO
"""
def reco(img1, img2):
    C = 1 # TODO what is a good value?
    return (eco(img2) + C) / (eco(img1) + C)

