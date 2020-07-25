import sys
sys.path.append('/home/i/Cassiopee/Dist/bin/x86_r8/lib/python2.7/site-packages')

import Converter.PyTree as C

t = C.convertFile2PyTree('polowaX/mesh81A1_721.su2', 'fmt_su2')
C.convertPyTree2File(t, 'converted/seria/mesh81A1_721.cgns', 'bin_adf')


# # t = C.convertFile2PyTree('su2_modified/mesh_flatplate_65x65.su2', 'fmt_su2')
# # print(t)
# # C.convertPyTree2File(t, 'out.hdf', 'bin_hdf')


# import Converter as Con
# #A = C.convertFile2PyTree('cgns/mesh2.cgns', 'bin_adf')
# A = C.convertFile2PyTree('su2_original/mesh89.cgns', 'bin_adf')
# C.convertPyTree2File(A, 'converted/cgns.su2', 'fmt_su2')
# #Con.convertArrays2File(A, 'converted/cgns2.su2', 'fmt_su2')