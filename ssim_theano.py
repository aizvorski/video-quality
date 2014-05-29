"""
Video Quality Metrics
Copyright (c) 2014 Alex Izvorski <aizvorski@gmail.com>

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

import theano
from theano import tensor

# declare two symbolic floating-point scalars
img1 = tensor.fmatrix()
img2 = tensor.fmatrix()

s1 = img1.sum()
s2 = img2.sum()
ss = (img1 * img1).sum() + (img2 * img2).sum()
s12 = (img1 * img2).sum()
vari = ss - s1*s1 - s2*s2
covar = s12 - s1*s2
ssim_c1 = .01*.01
ssim_c2 = .03*.03
ssim_value = (2*s1*s2 + ssim_c1) * (2*covar + ssim_c2) / ((s1*s1 + s2*s2 + ssim_c1) * (vari + ssim_c2))

ssim = theano.function([img1, img2], ssim_value)
