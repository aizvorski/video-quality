import numpy
import re
import sys
import scipy.misc
import subprocess
import os.path

import vifp
import ssim
import psnr
import niqe
import reco

import matplotlib.pyplot as plt

ref_file = 'lena.png'
dist_file = 'lena_tmp.jpg'

ref = scipy.misc.imread(ref_file, flatten=True).astype(numpy.float32)

quality_values = []
size_values = []
vifp_values = []
ssim_values = []
psnr_values = []
niqe_values = []
reco_values = []

plt.figure(figsize=(8, 8))

for quality in range(0, 101, 1):
    subprocess.check_call('gm convert %s -quality %d %s'%(ref_file, quality, dist_file), shell=True)
    file_size = os.path.getsize(dist_file)

    dist = scipy.misc.imread(dist_file, flatten=True).astype(numpy.float32)

    quality_values.append( quality )
    size_values.append( int(file_size/1024) )
    vifp_values.append( vifp.vifp_mscale(ref, dist) )
    ssim_values.append( ssim.ssim_exact(ref/255, dist/255) )
    psnr_values.append( psnr.psnr(ref, dist) )
    # niqe_values.append( niqe.niqe(dist/255) )
    reco_values.append( reco.reco(ref/255, dist/255) )

plt.plot(quality_values, vifp_values, label='VIFP')
plt.plot(quality_values, ssim_values, label='SSIM')
# plt.plot(niqe_values, label='NIQE')
plt.plot(quality_values, reco_values, label='RECO')
plt.plot(quality_values, numpy.asarray(psnr_values)/100.0, label='PSNR/100')
plt.legend(loc='lower right')
plt.xlabel('JPEG Quality')
plt.ylabel('Metric')
plt.savefig('jpg_demo_quality.png')

plt.figure(figsize=(8, 8))

plt.plot(size_values, vifp_values, label='VIFP')
plt.plot(size_values, ssim_values, label='SSIM')
# plt.plot(size_values, label='NIQE')
plt.plot(size_values, reco_values, label='RECO')
plt.plot(size_values, numpy.asarray(psnr_values)/100.0, label='PSNR/100')
plt.legend(loc='lower right')
plt.xlabel('JPEG File Size, KB')
plt.ylabel('Metric')
plt.savefig('jpg_demo_size.png')

