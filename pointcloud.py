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
