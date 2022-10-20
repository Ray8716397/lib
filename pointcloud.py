# -*- encoding: utf-8 -*-
'''
@File    :   pointcloud.py    
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/10/9 上午9:48   ray      1.0         None
'''

# import lib
import numpy as np
import open3d as o3d

def visualize_pc(pcd):
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    render_option: o3d.visualization.RenderOption = vis.get_render_option()
    render_option.background_color = np.array([0, 0, 0])  # 设置背景色（这里为黑色
    render_option.point_size = 1.0  # 设置渲染点的大小
    vis.add_geometry(pcd)
    vis.run()
    vis.destroy_window()


def load_pointcloud(file_path):
    file_format = file_path.split('.')[-1]
    if file_format == 'asc':
        # detect skip rows for split xyz,rgb
        skiprows = 0
        with open(file_path, 'r') as txt_file:
            while True:
                line = txt_file.readline()
                space_count = len(line.split(' ')) - 1
                if line:
                    if line[0] == '/' or (space_count != 8 and space_count != 9):
                        skiprows += 1
                    if line[0] == '/' or (space_count != 8 and space_count != 9):
                        break
                else:
                    break

        xyz_rgb = pd.read_csv(file_path, sep=' ', header=None, skiprows=skiprows,
                              usecols=[i for i in range(6)]).values
    elif file_format == 'pth':
        xyz, rgb, semantic_label, instance_label = torch.load(file_path)
        rgb = (rgb + 1) * 127.5
        xyz_rgb = np.hstack((xyz, rgb)).astype(np.float32)
    else:
        pc = o3d.io.read_point_cloud(file_path)
        xyz = np.array(pc.points)
        rgb = np.array(pc.colors) * 255
        xyz_rgb = np.hstack((xyz, rgb)).astype(np.float32)

    return xyz_rgb
