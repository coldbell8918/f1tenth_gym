import time
from f110_gym.envs.base_classes import Integrator
import yaml
import gym
import numpy as np
from argparse import Namespace

from numba import njit

from pyglet.gl import GL_POINTS

# @njit(fastmath=False, cache=True)

def cluster_consecutive(indices, min_length=60):
    clusters = np.split(indices, np.where(np.diff(indices) != 1)[0] + 1)
    return [cluster for cluster in clusters if len(cluster) >= min_length]

def find_max_gap(free_space_ranges):
    masked = np.ma.masked_where(free_space_ranges == 0, free_space_ranges)
    slices = np.ma.notmasked_contiguous(masked)
    max_len = slices[0].stop - slices[0].start
    chosen_slice = slices[0]
    for sl in slices[1:]:
        sl_len = sl.stop - sl.start
        if sl_len > max_len:
            max_len = sl_len
            chosen_slice = sl
    return chosen_slice.start, chosen_slice.stop

def find_best_point(start_i, end_i, ranges):
    averaged_max_gap = np.convolve(
        ranges[start_i:end_i], np.ones(80), 'same') / 80
    return averaged_max_gap.argmax() + start_i

def find_bounds_of_largest_cluster(clusters,gap_start, gap_end):
    
    largest_indices = [(max(cluster), cluster) for cluster in clusters]
    
    valid_clusters = [cluster for largest_index, cluster in largest_indices if largest_index <= 800]
    
    if valid_clusters:
        next_largest_cluster = max(valid_clusters, key=lambda cluster: max(cluster))
        
        smallest_index = min(next_largest_cluster)
        largest_index = max(next_largest_cluster)
        
        return smallest_index, largest_index
    else:
        return gap_start, gap_end

def get_angle(range_index, range_len, radians_per_elem):
    lidar_angle = (range_index - (range_len / 2)) * radians_per_elem
    steering_angle = lidar_angle / 2.0
    return steering_angle

def scan_callback(lidar_scan):

    radians_per_elem = (1.5 * np.pi) / len(lidar_scan)
    proc_ranges = np.array(lidar_scan[135:-135])

    cluster_distance = 2.5 
    filtered_indices = np.where(proc_ranges >= cluster_distance)[0]
    clusters = cluster_consecutive(filtered_indices)

    left = lidar_scan[720] # 좌측
    right = lidar_scan[380] # 우측
    step = lidar_scan[540] # 정면
    
    angle, velocity = 0.0, 0.0

    #####################################################################
    # 여기에 코드를 삽입하시오.
    # 가장 큰 Gap 찾기: find_max_gap 함수 이용
    # 적절한 point 찾기: find_best_point 함수 이용
    # 적절한 steering angle 찾기: 적절한 point를 기반으로 자동차의 조향각 조정
    # 적절한 velocity 값 구하기: 정면 거리에 따라, 혹은 angle 값에 따라 적잘한 velocity 선정
    #####################################################################
     
    return velocity, angle

def main():
    
    with open('test.yaml') as file:
        conf_dict = yaml.load(file, Loader=yaml.FullLoader)
    conf = Namespace(**conf_dict)

    # Simulation에서 차량을 따라가는 카메라 기능을 구현 및 경로를 시각적으로 rendering
    def render_callback(env_renderer):
        # custom extra drawing function

        e = env_renderer

        # update camera to follow car
        x = e.cars[0].vertices[::2]
        y = e.cars[0].vertices[1::2]
        top, bottom, left, right = max(y), min(y), min(x), max(x)
        e.score_label.x = left
        e.score_label.y = top - 700
        e.left = left - 800
        e.right = right + 800
        e.top = top + 800
        e.bottom = bottom - 800


    env = gym.make('f110_gym:f110-v0', map=conf.map_path, map_ext=conf.map_ext, num_agents=1, timestep=0.01, integrator=Integrator.RK4)
    env.add_render_callback(render_callback)
    
    obs, step_reward, done, info = env.reset(np.array([[conf.sx, conf.sy, conf.stheta]]))
    
    env.render()

    laptime = 0.0
    start = time.time()

    while not done:
        
        lidar_scan = obs['scans'][0]
        speed, steer = scan_callback(lidar_scan)
        obs, step_reward, done, info = env.step(np.array([[steer, speed]]))
        laptime += step_reward
        env.render(mode='human')
        
    print('Sim elapsed time:', laptime, 'Real elapsed time:', time.time()-start)

if __name__ == '__main__':
    main()
