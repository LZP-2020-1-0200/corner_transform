import matplotlib.pyplot as plt
import json
import matplotlib.image as mpimg
import os.path
import re
from subprocess import check_output

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
bio_point_x, bio_point_y = [], []
for bio_point in bio_points:
    bio_point_x.append(bio_point['x'])
    bio_point_y.append(bio_point['y'])

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

fig, ((ax_k_aug,ax_map), (ax_k_apak, ax_l_apak)) = plt.subplots(2, 2)
axs = (ax_k_apak,ax_k_aug,ax_l_apak  )
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
#plt.show()
plt.savefig(f"{OUTFOLDER}/10030karte.pdf", dpi=300)
plt.close()


check_output(
        f"pdftk {OUTFOLDER}\\100*.pdf cat output {OUTFOLDER}\\transform_p1.pdf", shell=True).decode()