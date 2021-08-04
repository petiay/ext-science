import glob
import numpy
from astropy.table import Table

files_in = sorted(glob.glob('updated_m31_mags/m31*'))
new_phot = sorted(glob.glob('updated_m31_mags/e*.fits'))

for j in range(len(files_in)):
    t = Table.read(new_phot[j])
    mags=[]
    mags_err=[]
    for i in range(len(filters)):
        mag = np.around(t[filters[i] + '_VEGA'][0], decimals=8)
        mag_err = np.around(t[filters[i] + '_ERR'][0], decimals=4)
        mags.append(mag)
        mags_err.append(mag_err)
    data_in = open(files_in[j], 'r')
    lines_in = np.array(data_in.readlines())
    data_in.close()
    file_out = files_in[j].split('.dat')[0] + "_n.dat"
    out = open(file_out, 'w')
    out.write(lines_in[0])
    out.write(lines_in[1])
    out.write(lines_in[2])
    out.write('WFC3_F275W = ' + str(mags[2]) + ' +/- ' + str(mags_err[2]) + '\n')
    out.write('WFC3_F336W = ' + str(mags[3]) + ' +/- ' + str(mags_err[3]) + '\n')
    out.write('ACS_F475W = ' + str(mags[0]) + ' +/- ' + str(mags_err[0]) + '\n')
    out.write('ACS_F814W = ' + str(mags[1]) + ' +/- ' + str(mags_err[1]) + '\n')
    out.write('WFC3_F110W = ' + str(mags[4]) + ' +/- ' + str(mags_err[4]) + '\n')
    out.write('WFC3_F160W = ' + str(mags[5]) + ' +/- ' + str(mags_err[5]) + '\n')
    out.write(lines_in[9])
    out.close()
