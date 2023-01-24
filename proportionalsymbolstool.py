import arcpy

in_featureclass = arcpy.GetParameterAsText(0)
in_numerical_field = arcpy.GetParameterAsText(1)
in_number_of_class = float(arcpy.GetParameterAsText(2))
in_user_friendly = arcpy.GetParameterAsText(3)
output = arcpy.GetParameterAsText(4)

#select current project file
aprx = arcpy.mp.ArcGISProject('CURRENT')

#list groups in table of contents
maps = aprx.listMaps()

#making sure selected map is not None like in layout view
map = None
for m in maps:
    print(m.name)
    if m.name == 'Map':
        map = m
        break

#making sure input feature class doesn't have a None layer 
map = aprx.activeMap
layer = map.addDataFromPath(in_featureclass)

if layer != None:
    print(layer.dataSource)

if layer is not None:
    layer.name = 'User Feature Class'

#create proportional symbols
symbology = layer.symbology
symbology.updateRenderer('GraduatedSymbolsRenderer')
symbology.renderer.classificationField = in_numerical_field
symbology.renderer.breakCount = in_number_of_class
symbology.renderer.minimumSymbolSize = 5
symbology.renderer.maximumSymbolSize = 40
upperbounds = []
for bounds in symbology.renderer.classBreaks:
    upperbounds.append(bounds.upperBound)
arcpy.AddMessage(upperbounds)

#if user friendly      
if in_user_friendly == 'true':
    renderer = symbology.renderer
    renderer.label = 'User Numerical Field'
    i=0
    for brk in symbology.renderer.classBreaks:
        if i==0:
            brk.label = 'Less than {:.0f}'.format(upperbounds[i])
        else:
            brk.label = '{:.0f} - {:.0f}'.format(upperbounds[i-1], upperbounds[i])
        i+=1

layer.symbology = symbology



