import os 
import pxz
from pxz import *


#file path 
folder_path = ''
#folder with the name of the part in which save the extracted views, it is created if it doesn't already exist
output_folder_path = f''
os.makedirs(output_folder_path, exist_ok=True)

#image dimensions 
WIDTH = 5000
HEIGHT = 5000

#the imported model is centered to the origin and moved to the ground (lays on the plane xz) 
_ret_ = process.guidedImport([folder_path], pxz.process.CoordinateSystemOptions(["automaticOrientation",0], ["automaticScale",0], True, True), ["usePreset",2], pxz.process.ImportOptions(True, True, True), False, False, False, False, False, False)

#Axis Aligned Bounding Box
aabb = scene.getAABB([scene.getRoot()])

#world coordinates of the object in mm
x_min = aabb.low.x
y_min = aabb.low.y
z_min = aabb.low.z
x_max = aabb.high.x
y_max = aabb.high.y
z_max = aabb.high.z
deltax = x_max - x_min
deltay = y_max - y_min
deltaz = z_max - z_min

m = 0.3 #percentage of margin around the object 
alpha = 3 #factor used to setup the distance of the camera 
#d = alpha*(longer dimension between the x and y of the camera) + 1/2 * dimension of the object along the directin of the camera 

################################SET PARAMETERS
########################TOP VIEW 
m_top_bot = m*min(x_max, z_max) #same for top and bottom

l_top = x_min - m_top_bot 
r_top = x_max + m_top_bot
t_top = - (z_min - m_top_bot) 
b_top = - (z_max + m_top_bot)

y_view_top = alpha * max(deltax, deltaz, deltay) + deltay 

########################BOTTOM VIEW 
l_b =  x_min - m_top_bot
r_b =  x_max + m_top_bot
t_b = - (z_min - m_top_bot) 
b_b = - (z_max + m_top_bot)

y_view_bottom = y_view_top - deltay

########################FRONT VIEW 
m_front_back = m*min(x_max, y_max/2) #same for front and back 

l_f = x_min - m_front_back
r_f = x_max + m_front_back
t_f = y_max + m_front_back 
b_f = - m_front_back 

z_view = alpha*max(deltax, deltay) + 0.5*deltaz #same for front and back

########################BACK VIEW 
l_back =  -(x_max + m_front_back)
r_back = -(x_min - m_front_back)
t_back = y_max + m_front_back 
b_back = - m_front_back 


########################LEFT VIEW 
m_left_right = m*min(y_max/2, z_max) 
l_l = -(z_max + m_left_right)
r_l = -(z_min - m_left_right)
t_l = y_max + m_left_right 
b_l = - m_left_right

x_view = alpha*max(deltay, deltaz) + 0.5*deltax #same for left and right 

########################RIGHT VIEW 
l_r = z_min - m_left_right
r_r = z_max + m_left_right
t_r = y_max + m_left_right
b_r =  - m_left_right #y_min is 0



h_view = max(y_view_top, y_view_bottom, z_view, x_view)


################################EXTRACTION 
#########################TOP VIEW 

f_top = y_view_top*2 - y_max
n_top = y_view_top/2 + y_min 

ctb = min(deltax, deltaz) / max(deltax, deltaz) 
s_factor = max( ctb*2/(r_top-l_top), ctb*2/(t_top-b_top)) 

h_view_top = h_view + deltay

viewerMatrices_top = {
	'views': [[[1.0, 0.0, 0.0, 0.0], 
	[0.0, 0.0, -1.0, 0.0], 
	[0.0, 1.0, 0.0, -h_view_top], 
	[0.0, 0.0, 0.0, 1.0]]], 
	'projs': [[[s_factor, 0, 0, -(r_top+l_top)/(r_top-l_top)], 
	[0, s_factor, 0,-(t_top+b_top)/(t_top-b_top)], 
	[0, 0, -2/(f_top-n_top), - (f_top+n_top)/ (f_top-n_top)], 
	[0, 0, 0, 1]]], 'clipping': pxz.geom.Point2(n_top, f_top)}


viewerMatrices = viewerMatrices_top

viewer = view.createViewer(WIDTH, HEIGHT)
view.addRoot(scene.getRoot(), viewer) 
view.showLines(False, viewer)
view.setViewerMatrices(viewerMatrices['views'], viewerMatrices["projs"], viewerMatrices["clipping"], viewer) 
view.refreshViewer(viewer, forceUpdate=True) 

#save the OUTPUT 
OUTPUT_FILE = os.path.join(output_folder_path, 'output_top.png') #change the name as desired
view.takeScreenshot(OUTPUT_FILE, viewer)

################################BOTTOM VIEW 

n_b = y_view_bottom/2 - y_min
f_b = y_view_bottom*2 + y_max 

s_factor = max( ctb*2/(r_b-l_b), ctb*2/(t_b-b_b)) 

viewerMatrices_bottom = {
	'views': [[[1.0, 0.0, 0.0, 0.0], 
	[0.0, 0.0, 1.0, 0.0], 
	[0.0, -1.0, 0.0, -h_view], 
	[0.0, 0.0, 0.0, 1.0]]], 
	'projs': [[[s_factor, 0, 0, -(r_b+l_b)/(r_b-l_b)], 
	[0, s_factor, 0,-(t_b+b_b)/(t_b-b_b)], 
	[0, 0, -2/(f_b-n_b), - (f_b+n_b)/ (f_b-n_b)], 
	[0, 0, 0, 1]]], 'clipping': pxz.geom.Point2(n_b, f_b)}


viewerMatrices = viewerMatrices_bottom

viewer = view.createViewer(WIDTH, HEIGHT)
view.addRoot(scene.getRoot(), viewer) 
view.showLines(False, viewer)
view.setViewerMatrices(viewerMatrices['views'], viewerMatrices["projs"], viewerMatrices["clipping"], viewer) #change viewerMatrices accordingly
view.refreshViewer(viewer, forceUpdate=True) 

#save the OUTPUT 
OUTPUT_FILE = os.path.join(output_folder_path, 'output_bottom.png') #change the name accordingly to the selected view 
view.takeScreenshot(OUTPUT_FILE, viewer)

################################FRONT VIEW 

n_f = z_view/2 + z_min
f_f = z_view*2 + z_max 

cfb = min(deltax, deltay)/max(deltax, deltay) 

s_factor = max( cfb*2/(r_f-l_f),  cfb*2/(t_f-b_f)) 
	
h_view_front_back = z_view + deltaz/2

viewerMatrices_front = {
	'views': [[[1.0, 0.0, 0.0, 0.0], 
	[0.0, 1.0, 0.0, 0.0], 
	[0.0, 0.0, 1.0, -h_view_front_back], 
	[0.0, 0.0, 0.0, 1.0]]], 
	'projs': [[[s_factor, 0, 0, -(r_f+l_f)/(r_f-l_f)], 
	[0, s_factor, 0,-(t_f+b_f)/(t_f-b_f)], 
	[0, 0, -2/(f_f-n_f), - (f_f+n_f)/ (f_f-n_f)], 
	[0, 0, 0, 1]]], 'clipping': pxz.geom.Point2(n_f, f_f)}


viewerMatrices = viewerMatrices_front

viewer = view.createViewer(WIDTH, HEIGHT)
view.addRoot(scene.getRoot(), viewer) 
view.showLines(False, viewer)
view.setViewerMatrices(viewerMatrices['views'], viewerMatrices["projs"], viewerMatrices["clipping"], viewer) 
view.refreshViewer(viewer, forceUpdate=True)  

#save the OUTPUT 
OUTPUT_FILE = os.path.join(output_folder_path, 'output_front.png')
view.takeScreenshot(OUTPUT_FILE, viewer)


################################BACK VIEW 

n_back = z_view/2 + z_min
f_back = z_view*2 + z_max 

s_factor = max( cfb*2/(r_back-l_back),  cfb*2/(t_back-b_back))  

viewerMatrices_back = {
	'views': [[[-1.0, 0.0, 0.0, 0.0], 
	[0.0, 1.0, 0.0, 0.0], 
	[0.0, 0.0, -1.0, -h_view_front_back], 
	[0.0, 0.0, 0.0, 1.0]]], 
	'projs': [[[s_factor, 0, 0, -(r_back+l_back)/(r_back-l_back)], 
	[0, s_factor, 0,-(t_back+b_back)/(t_back-b_back)], 
	[0, 0, -2/(f_back-n_back), - (f_back+n_back)/ (f_back-n_back)], 
	[0, 0, 0, 1]]], 'clipping': pxz.geom.Point2(n_back, f_back)}


viewerMatrices = viewerMatrices_back

viewer = view.createViewer(WIDTH, HEIGHT)
view.addRoot(scene.getRoot(), viewer) 
view.showLines(False, viewer)
view.setViewerMatrices(viewerMatrices['views'], viewerMatrices["projs"], viewerMatrices["clipping"], viewer) 
view.refreshViewer(viewer, forceUpdate=True)

#save the OUTPUT 
OUTPUT_FILE = os.path.join(output_folder_path, 'output_back.png') #change the name accordingly to the selected view 
view.takeScreenshot(OUTPUT_FILE, viewer)


################################LEFT VIEW 

n_l = x_view/2 + x_min
f_l = x_view*2 + x_max 

clr = min(deltay, deltaz)/max(deltay, deltaz)
s_factor = max( clr*2/(r_l-l_l),  clr*2/(t_l-b_l))  

h_left_right = h_view + deltax/2
viewerMatrices_left = {
	'views': [[[0.0, 0.0, 1.0, 0.0], 
	[0.0, 1.0, 0.0, 0.0], 
	[-1.0, 0.0, 0.0, -h_left_right], 
	[0.0, 0.0, 0.0, 1.0]]], 
	'projs': [[[s_factor, 0, 0, -(r_l+l_l)/(r_l-l_l)], 
	[0, s_factor, 0,-(t_l+b_l)/(t_l-b_l)], 
	[0, 0, -2/(f_l-n_l), - (f_l+n_l)/ (f_l-n_l)], 
	[0, 0, 0, 1]]], 'clipping': pxz.geom.Point2(n_l, f_l)}


viewerMatrices = viewerMatrices_left

viewer = view.createViewer(WIDTH, HEIGHT)
view.addRoot(scene.getRoot(), viewer) 
view.showLines(False, viewer)
view.setViewerMatrices(viewerMatrices['views'], viewerMatrices["projs"], viewerMatrices["clipping"], viewer)
view.refreshViewer(viewer, forceUpdate=True) 

#save the OUTPUT 
OUTPUT_FILE = os.path.join(output_folder_path, 'output_left.png') #change the name accordingly to the selected view 
view.takeScreenshot(OUTPUT_FILE, viewer)


################################RIGHT VIEW 

n_r = x_view/2 + x_min
f_r = x_view*2 + x_max 

s_factor = max( clr*2/(r_r-l_r),  clr*2/(t_r-b_r)) 

viewerMatrices_right = {
	'views': [[[0.0, 0.0, -1.0, 0.0], 
	[0.0, 1.0, 0.0, 0.0], 
	[1.0, 0.0, 0.0, -h_left_right], 
	[0.0, 0.0, 0.0, 1.0]]], 
	'projs': [[[s_factor, 0, 0, -(r_r+l_r)/(r_r-l_r)], 
	[0, s_factor, 0,-(t_r+b_r)/(t_r-b_r)], 
	[0, 0, -2/(f_r-n_r), - (f_r+n_r)/ (f_r-n_r)], 
	[0, 0, 0, 1]]], 'clipping': pxz.geom.Point2(n_r, f_r)}


viewerMatrices = viewerMatrices_right

viewer = view.createViewer(WIDTH, HEIGHT)
view.addRoot(scene.getRoot(), viewer) 
view.showLines(False, viewer)
view.setViewerMatrices(viewerMatrices['views'], viewerMatrices["projs"], viewerMatrices["clipping"], viewer) 
view.refreshViewer(viewer, forceUpdate=True) 

#save the OUTPUT 
OUTPUT_FILE = os.path.join(output_folder_path, 'output_right.png') 
view.takeScreenshot(OUTPUT_FILE, viewer)

