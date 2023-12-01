import matplotlib.pyplot as plt
import json
import matplotlib.image as mpimg
import os.path
import re
from subprocess import check_output
from coordinate import Coordinate
from double_translation import merge_coordinate

with open("data_in/p1_filelist.txt", 'r') as ListFile:
    ListFileLines = ListFile.readlines()

bio_corner_jpg = []
bio_anchor_jpg = []
map_corner_jpg = []
for full_ListFileLine in ListFileLines:
    file_name = full_ListFileLine.strip()
    if 'sturi1p.txt' in file_name:
        map_corners_file_name = file_name
    elif 'sturi.txt' in file_name:
        bio_corners_file_name = file_name
    elif 'sturis' in file_name:
        bio_corner_jpg.append(file_name)
    elif 'anchor' in file_name and '.jpg' in file_name:
        bio_anchor_jpg.append(file_name)
    elif 'sejais.jpg' in file_name:
        map_corner_jpg.append(file_name)
    elif 'session.json' in file_name:
        bio_session_file_name = file_name
    else:
        print(file_name)


fig, ((ax_map, ax0), (ax1, ax2)) = plt.subplots(2, 2)
axs = (ax1, ax2, ax0)

with open(bio_corners_file_name) as bio_corners_file:
    bio_corners_json_object = json.load(bio_corners_file)

ns = 1
bio_corners_x, bio_corners_y = [], []
for bio_corner in bio_corners_json_object['points']:
    print(bio_corner)
    x = bio_corner['x']
    y = bio_corner['y']
    bio_corners_x.append(x)
    bio_corners_y.append(y)
    ax_map.text(x, y, ns)
    ns += 1
ax_map.invert_xaxis()
ax_map.plot(bio_corners_x, bio_corners_y)
ax_map.set_aspect('equal', 'box')

for axn in range(len(axs)):
    ax = axs[axn]
    original_jpg = mpimg.imread(bio_corner_jpg[axn])
    ax.imshow(original_jpg)
    ax.axis('off')
    ax.set_title(os.path.basename(bio_corner_jpg[axn]))
plt.tight_layout()
# plt.show()

OUTFOLDER = "data_out"
if os.path.exists(OUTFOLDER):
    for f in os.listdir(OUTFOLDER):
        os.remove(os.path.join(OUTFOLDER, f))
else:
    os.mkdir(OUTFOLDER)
print(f"OUTFOLDER = {OUTFOLDER}")

plt.savefig(f"{OUTFOLDER}/10010sturi.pdf", dpi=300)
plt.close()


with open(bio_session_file_name) as bio_session_file:
    bio_session_json_object = json.load(bio_session_file)

bio_anchors = bio_session_json_object['anchors']
print(bio_anchors)


fig, ((ax_map, ax0), (ax1, ax2)) = plt.subplots(2, 2)
axs = (ax1, ax2, ax0)
ax_map.invert_xaxis()
ax_map.plot(bio_corners_x, bio_corners_y, label='corners')


na = 1
bio_anchors_x, bio_anchors_y = [], []
for bio_anchor in bio_anchors:
    print(bio_anchor)
    x = bio_anchor['x']
    y = bio_anchor['y']
    bio_anchors_x.append(x)
    bio_anchors_y.append(y)
    ax_map.text(x, y, na)
    ax_map.text(bio_corners_x[na-1], bio_corners_y[na-1], na)

    na += 1

ax_map.plot(bio_anchors_x, bio_anchors_y, label='anchors')


bio_points = bio_session_json_object['points']
bio_point_x, bio_point_y, bio_point_filename = [], [], []


for bio_point in bio_points:
    bio_point_x.append(bio_point['x'])
    bio_point_y.append(bio_point['y'])
    bio_point_filename.append(bio_point['filename'])

ax_map.plot(bio_point_x, bio_point_y, '.', label='points')

#ax_map.set_aspect('equal', 'box')
ax_map.axis('equal')
ax_map.legend(loc='center')


for axn in range(len(axs)):
    ax = axs[axn]
    original_jpg = mpimg.imread(bio_anchor_jpg[axn])
    ax.imshow(original_jpg)
    ax.axis('off')
    ax.set_title(os.path.basename(bio_anchor_jpg[axn]))


plt.tight_layout()
# plt.show()
plt.savefig(f"{OUTFOLDER}/10020enkuri.pdf", dpi=300)
plt.close()

fig, ((ax_k_aug, ax_map), (ax_k_apak, ax_l_apak)) = plt.subplots(2, 2)
axs = (ax_k_apak, ax_k_aug, ax_l_apak)
ax_map.invert_xaxis()

with open(map_corners_file_name, 'r') as map_corners_file:
    map_corners_lines = map_corners_file.readlines()

texts = []
map_corners_x = []
map_corners_y = []

for full_map_corner_line in map_corners_lines:
    map_corner_line = full_map_corner_line.strip()
    parts = re.split(r'\t+', map_corner_line)
    txt = parts[0]
    texts.append(txt)
    x = int(parts[1])
    y = int(parts[2])
    map_corners_x.append(x)
    map_corners_y.append(y)
    ax_map.text(x, y, txt)


print(texts)
print(map_corners_x)
print(map_corners_y)


ax_map.plot(bio_corners_x, bio_corners_y, label='corners')
ax_map.plot(bio_anchors_x, bio_anchors_y, label='anchors')
ax_map.plot(bio_point_x, bio_point_y, '.', label='points')
ax_map.plot(map_corners_x, map_corners_y, label='map corners')


ax_map.axis('equal')
ax_map.legend(loc='center')


for axn in range(len(axs)):
    ax = axs[axn]
    original_jpg = mpimg.imread(map_corner_jpg[axn])
    ax.imshow(original_jpg)
    ax.axis('off')
    ax.set_title(os.path.basename(map_corner_jpg[axn]))


plt.tight_layout()
# plt.show()
plt.savefig(f"{OUTFOLDER}/10030karte.pdf", dpi=300)
plt.close()


# Stūri	A	56202	32511
# C	66232	22823
# B	56376	22724
# Enkuri	1	56576	31973
# 2	65556	32220
# 3	65531	23501

redo_corners_x = (56202, 56376, 66232)
redo_corners_y = (32511, 22724, 22823)
redo_corners_abc = ("A", "B", "C")

redo_enc_x = (56576, 65556, 65531)
redo_enc_y = (31973, 32220, 23501)


def abcdef(x, y, x_prim, y_prim):
    x0, x1, x2 = x[0], x[1], x[2]
    y0, y1, y2 = y[0], y[1], y[2]
    x0prim, x1prim, x2prim = x_prim[0], x_prim[1], x_prim[2]
    y0prim, y1prim, y2prim = y_prim[0], y_prim[1], y_prim[2]

    a = (x0prim*(y2-y1)-x1prim*y2+x2prim*y1+(x1prim-x2prim)*y0) / \
        (x0*(y2-y1)-x1*y2+x2*y1+(x1-x2)*y0)
    b = (x0*(x2prim-x1prim)-x1*x2prim+x1prim*x2+x0prim*(x1-x2)) / \
        (x0*(y2-y1)-x1*y2+x2*y1+(x1-x2)*y0)
    c = - ((x0*(x2prim*y1-x1prim*y2)+x0prim*(x1*y2-x2*y1) +
           (x1prim*x2-x1*x2prim)*y0)/(x0*(y2-y1)-x1*y2+x2*y1+(x1-x2)*y0))
    d = (y1*y2prim+y0*(y1prim-y2prim)+y0prim*(y2-y1) -
         y1prim*y2)/(x0*(y2-y1)-x1*y2+x2*y1+(x1-x2)*y0)
    e = - ((x1*y2prim+x0*(y1prim-y2prim)-x2*y1prim+(x2-x1)
           * y0prim)/(x0*(y2-y1)-x1*y2+x2*y1+(x1-x2)*y0))
    f = (x0*(y1prim*y2-y1*y2prim)+y0*(x1*y2prim-x2*y1prim) +
         y0prim*(x2*y1-x1*y2))/(x0*(y2-y1)-x1*y2+x2*y1+(x1-x2)*y0)
    return (a, b, c, d, e, f)


fig, ((ax_png, ax_enc), (ax_oldenc, ax_mapf)) = plt.subplots(2, 2)
#axs = (ax_k_apak, ax_k_aug, ax_l_apak)
ax_enc.invert_xaxis()

original_png = mpimg.imread("data_in/thumbnail_image.png")
ax_png.imshow(original_png)
ax_png.axis('off')
ax_png.set_title("Atkārtojums")


ax_enc.plot(redo_corners_x, redo_corners_y)
for m in range(len(redo_corners_abc)):
    ax_enc.text(redo_corners_x[m], redo_corners_y[m], redo_corners_abc[m])
ax_enc.plot(redo_enc_x, redo_enc_y)
ax_enc.set_title("pārmērīti enkuri")


T1 = abcdef(bio_anchors_x, bio_anchors_y, redo_enc_x, redo_enc_y)

t1_bio_anch_x = []
t1_bio_anch_y = []

for m in range(len(bio_anchors_x)):
    t1_bio_anch_x.append(bio_anchors_x[m]*T1[0]+bio_anchors_y[m]*T1[1]+T1[2])
    t1_bio_anch_y.append(bio_anchors_x[m]*T1[3]+bio_anchors_y[m]*T1[4]+T1[5])


t1_bio_point_x = []
t1_bio_point_y = []
for m in range(len(bio_point_x)):
    t1_bio_point_x.append(bio_point_x[m]*T1[0]+bio_point_y[m]*T1[1]+T1[2])
    t1_bio_point_y.append(bio_point_x[m]*T1[3]+bio_point_y[m]*T1[4]+T1[5])

#    old_xy=Coordinate(bio_point_x[m],bio_point_y[m])
#    new_xy=merge_coordinate(bio_anchors_x,bio_anchors_y)
#T1 = abcdef(bio_anchors_x, bio_anchors_y, redo_enc_x, redo_enc_y)


x_reverse = []
y_reverse = []
for m in {2, 1, 0}:
    x_reverse.append(redo_corners_x[m])
    y_reverse.append(redo_corners_y[m])

T2 = abcdef(x_reverse, y_reverse, map_corners_x, map_corners_y)
t2_anch_x = []
t2_anch_y = []
for m in range(len(redo_enc_x)):
    t2_anch_x.append(redo_enc_x[m]*T2[0]+redo_enc_y[m]*T2[1]+T2[2])
    t2_anch_y.append(redo_enc_x[m]*T2[3]+redo_enc_y[m]*T2[4]+T2[5])

t2_bio_point_x = []
t2_bio_point_y = []

for m in range(len(t1_bio_point_x)):
    t2_bio_point_x.append(
        t1_bio_point_x[m]*T2[0]+t1_bio_point_y[m]*T2[1]+T2[2])
    t2_bio_point_y.append(
        t1_bio_point_x[m]*T2[3]+t1_bio_point_y[m]*T2[4]+T2[5])


ax_oldenc.invert_xaxis()
ax_oldenc.plot(redo_corners_x, redo_corners_y)
#ax_oldenc.plot(bio_anchors_x, bio_anchors_y, label='anchors')
ax_oldenc.plot(t1_bio_anch_x, t1_bio_anch_y, label='Tanchors')
ax_oldenc.plot(t1_bio_point_x, t1_bio_point_y, '.', label='points')

ax_oldenc.axis('equal')
ax_oldenc.set_title("pārcelti enkuri")

ax_mapf.plot(map_corners_x, map_corners_y)
ax_mapf.plot(t2_anch_x, t2_anch_y)
ax_mapf.plot(t2_bio_point_x, t2_bio_point_y, '.', label='points')
ax_mapf.set_title("punkti kartē")

ax_mapf.invert_xaxis()
plt.tight_layout()
#plt.show()
plt.savefig(f"{OUTFOLDER}/10040redo.pdf", dpi=300)
plt.close()



#bio_point_filename


check_output(
    f"pdftk {OUTFOLDER}\\100*.pdf cat output transform_p1.pdf", shell=True).decode()
