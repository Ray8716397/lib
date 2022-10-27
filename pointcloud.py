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


def RemoveNoiseStatistical(pc, nb_neighbors=20, std_ratio=2.0):
    """ remove point clouds noise using statitical noise removal method

    Args:
        pc (ndarray): N x 3 point clouds
        nb_neighbors (int, optional): Defaults to 20.
        std_ratio (float, optional): Defaults to 2.0.

    Returns:
        [ndarray]: N x 3 point clouds
    """

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pc)
    cl, ind = pcd.remove_statistical_outlier(
        nb_neighbors=nb_neighbors, std_ratio=std_ratio)

    return np.asarray(cl.points)


def DetectMultiPlanes(points, min_ratio=0.05, threshold=0.01, iterations=1000):
    """ Detect multiple planes from given point clouds

    Args:
        points (np.ndarray):
        min_ratio (float, optional): The minimum left points ratio to end the Detection. Defaults to 0.05.
        threshold (float, optional): RANSAC threshold in (m). Defaults to 0.01.

    Returns:
        [List[tuple(np.ndarray, List)]]: Plane equation and plane point index
    """

    plane_list = []
    N = len(points)
    target = points.copy()
    count = 0

    while count < (1 - min_ratio) * N:
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(target)
        w, index = pcd.segment_plane(
            threshold, 3, iterations)
        # w, index = PlaneRegression(
        #     target, threshold=threshold, init_n=3, iter=iterations)

        count += len(index)
        plane_list.append((w, target[index]))
        target = np.delete(target, index, axis=0)

    return plane_list
