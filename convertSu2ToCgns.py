import sys
sys.path.append('/home/i/Cassiopee/Dist/bin/x86_r8/lib/python2.7/site-packages')

import Converter.PyTree as C

t = C.convertFile2PyTree('su2_original/mesh_flatplate_65x65.su2', 'fmt_su2')

#t = C.convertArray2Node(t)
print(t)
print(C.getValue(t, 'GridCoordinates', 0))
print(C.getBCs(t))
C.convertPyTree2File(t, 'converted/base.cgns', 'bin_cgns')

# t = C.convertFile2PyTree('su2_modified/mesh_flatplate_65x65.su2', 'fmt_su2')
# print(t)
# C.convertPyTree2File(t, 'out.hdf', 'bin_hdf')


# import Converter as C
# A = C.convertFile2Arrays('su2_modified/mesh_flatplate_65x65.su2', 'fmt_su2')
# C.convertArrays2File(A, 'out.su2', 'fmt_su2')