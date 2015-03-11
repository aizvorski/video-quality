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

import numpy
import re
import sys
import scipy.misc

import vifp
import ssim
#import ssim_theano
import psnr
import niqe
import reco

def img_greyscale(img):
    return 0.299 * img[:,:,0] + 0.587 * img[:,:,1] + 0.114 * img[:,:,2]

def img_read_yuv(src_file, width, height):
    y_img = numpy.fromfile(src_file, dtype=numpy.uint8, count=(width * height)).reshape( (height, width) )
    u_img = numpy.fromfile(src_file, dtype=numpy.uint8, count=((width/2) * (height/2))).reshape( (height/2, width/2) )
    v_img = numpy.fromfile(src_file, dtype=numpy.uint8, count=((width/2) * (height/2))).reshape( (height/2, width/2) )
    return (y_img, u_img, v_img)

ref_file = sys.argv[1]
dist_file = sys.argv[2]

if ".yuv" in ref_file:
    # Inputs are uncompressed video in YUV420 planar format

    # Get resolution from file name
    m = re.search(r"(\d+)x(\d+)", ref_file)
    if not m:
        print "Could not find resolution in file name: %s" % (ref_file)
        exit(1)

    width, height = int(m.group(1)), int(m.group(2))
    print "Comparing %s to %s, resolution %d x %d" % (ref_file, dist_file, width, height)

    ref_fh = open(ref_file, "rb")
    dist_fh = open(dist_file, "rb")

    frame_num = 0
    while True:
        ref, _, _ = img_read_yuv(ref_fh, width, height)
        dist, _, _ = img_read_yuv(dist_fh, width, height)
        vifp_value = vifp.vifp_mscale(ref.astype(float), dist.astype(float))
        ssim_value = ssim.ssim(ref, dist)
        print "Frame=%d VIFP=%f SSIM=%f" % (frame_num, vifp_value, ssim_value)
        frame_num += 1

else:
    # Inputs are image files
    ref = scipy.misc.imread(ref_file, flatten=True).astype(numpy.float32)
    dist = scipy.misc.imread(dist_file, flatten=True).astype(numpy.float32)

    width, height = ref.shape[1], ref.shape[0]
    print "Comparing %s to %s, resolution %d x %d" % (ref_file, dist_file, width, height)

    vifp_value = vifp.vifp_mscale(ref, dist)
    print "VIFP=%f" % (vifp_value)

    ssim_value = ssim.ssim_exact(ref/255, dist/255)
    print "SSIM=%f" % (ssim_value)

    # FIXME this is buggy, disable for now
    # ssim_value2 = ssim.ssim(ref/255, dist/255)
    # print "SSIM approx=%f" % (ssim_value2)

    psnr_value = psnr.psnr(ref, dist)
    print "PSNR=%f" % (psnr_value)

    # niqe_value = niqe.niqe(dist/255)
    # print "NIQE=%f" % (niqe_value)

    reco_value = reco.reco(ref/255, dist/255)
    print "RECO=%f" % (reco_value)
