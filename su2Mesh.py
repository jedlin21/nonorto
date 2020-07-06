from optparse import OptionParser

parser=OptionParser()
parser.add_option("-f", "--file", dest="filename", default="Channel.su2",
                  help="write mesh to FILE", metavar="FILE")
parser.add_option("-n", "--nNode", dest="nNode", default=125,
                  help="use this NNODE in x direction", metavar="NNODE")
parser.add_option("-m", "--mNode", dest="mNode", default=100,
                  help="use this MNODE in y direction", metavar="MNODE")
parser.add_option("-x", "--xLength", dest="xLength", default=7.0,
                  help="use this XLENGTH", metavar="XLENGTH")
parser.add_option("--offsetx", dest="offsetx", default=1.0,
                  help="use this OFFSETX", metavar="OFFSETX")
parser.add_option("--xAdapt", dest="xAdapt", default="True",
                  help="Adapt the grid XADAPT", metavar="XADAPT")
parser.add_option("-y", "--yLength", dest="yLength", default=1.0,
                  help="use this YLENGTH", metavar="YLENGTH")
parser.add_option("--offsety", dest="offsety", default=0.5,
                  help="use this OFFSETY", metavar="OFFSETY")
parser.add_option("--yAdapt", dest="yAdapt", default="True",
                  help="Adapt the grid YADAPT", metavar="YADAPT")
(options, args)=parser.parse_args()

nNode = int(options.nNode)
mNode = int(options.mNode)
xLength = float(options.xLength)
yLength = float(options.yLength)
xAdapt = options.xAdapt
yAdapt = options.yAdapt

Mesh_File = open(options.filename,"w")

Mesh_File.write( "%\n" )
Mesh_File.write( "% Problem dimension\n" )
Mesh_File.write( "%\n" )
Mesh_File.write( "NDIME=2\n" )
Mesh_File.write( "%\n" )
Mesh_File.write( "% Inner elements\n" )
Mesh_File.write( "%\n" )
Mesh_File.write( "NELEM=%s\n" % ((nNode-1)*(mNode-1)))


iElem = 0
for jNode in range(mNode-1):
    for iNode in range(nNode-1):
        iPoint = jNode*nNode + iNode
        jPoint = jNode*nNode + iNode + 1
        kPoint = (jNode + 1)*nNode + iNode
        mPoint = (jNode + 1)*nNode + (iNode + 1)
        Mesh_File.write( "9 \t %s \t %s \t %s \t %s \t %s\n" % (iPoint, jPoint, mPoint, kPoint, iElem) )
        iElem = iElem + 1

nPoint = (nNode)*(mNode)
Mesh_File.write( "%\n" )
Mesh_File.write( "NPOIN=%s\n" % ((nNode)*(mNode)) )
iPoint = 0

for jNode in range(mNode):
    for iNode in range(nNode):
        xCoord = float(iNode)/float(nNode-1)
        yCoord = float(jNode)/float(mNode-1)
          
        xCoord_new =  xLength*xCoord - float(options.offsetx)
        yCoord_new =  yLength*yCoord - float(options.offsety)

        Mesh_File.write( "%15.14f \t %15.14f \t %s\n" % (xCoord_new, yCoord_new, iPoint) )
        iPoint = iPoint + 1

Mesh_File.write( "%\n" )
Mesh_File.write( "% Boundary elements\n" )
Mesh_File.write( "%\n" )
Mesh_File.write( "NMARK=4\n" )
Mesh_File.write( "MARKER_TAG= lower\n" )
Mesh_File.write( "MARKER_ELEMS=%s\n" % (nNode-1))
for iNode in range(nNode-1):
    Mesh_File.write( "3 \t %s \t %s\n" % (iNode, iNode + 1) )

Mesh_File.write( "MARKER_TAG= outlet\n" )
Mesh_File.write( "MARKER_ELEMS=%s\n" % (mNode-1))
for jNode in range(mNode-1):
    Mesh_File.write( "3 \t %s \t %s\n" % (jNode*nNode + (nNode - 1),  (jNode + 1)*nNode + (nNode - 1) ) )
Mesh_File.write( "MARKER_TAG= upper\n" )
Mesh_File.write( "MARKER_ELEMS=%s\n" % (nNode-1))
for iNode in range(nNode-1):
    Mesh_File.write( "3 \t %s \t %s\n" % ((nNode*mNode - 1) - iNode, (nNode*mNode - 1) - (iNode + 1)) )
Mesh_File.write( "MARKER_TAG= inlet\n" )
Mesh_File.write( "MARKER_ELEMS=%s\n" % (mNode-1))
for jNode in range(mNode-2, -1, -1):
    Mesh_File.write( "3 \t %s \t %s\n" % ((jNode + 1)*nNode, jNode*nNode ) )
    
Mesh_File.close()