import os
from glob import glob
from setuptools import setup

package_name = 'brash_application_tools'

data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ]


def package_files(data_files, directory_list):

    paths_dict = {}

    for directory in directory_list:

        for (path, directories, filenames) in os.walk(directory):

            for filename in filenames:

                file_path = os.path.join(path, filename)
                install_path = os.path.join('share', package_name, path)

                if install_path in paths_dict.keys():
                    paths_dict[install_path].append(file_path)

                else:
                    paths_dict[install_path] = [file_path]

    for key in paths_dict.keys():
        data_files.append((key, paths_dict[key]))

    return data_files



setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=package_files( data_files, ['config/', 'launch/', 'meshes/', 'rviz/', 'urdf/', 'worlds/' ] ),
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Ana C. Huaman Quispe',
    maintainer_email='ana@traclabs.com',
    description='BRASH Demonstrations',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
            'console_scripts': [
                    'ground_twist_odom_convert = brash_application_tools.ground_twist_odom_convert:main',
                    'flight_twist_odom_convert = brash_application_tools.flight_twist_odom_convert:main',
                    'joint_state_convert = brash_application_tools.joint_state_convert:main',
                    'canadarm_control_node = brash_application_tools.canadarm_control_node:main',
                    'canadarm_send_command = brash_application_tools.canadarm_send_command:main',
                    'canadarm_hk_joint_state_convert = brash_application_tools.canadarm_hk_joint_state_convert:main',                                  
            ],
    },
)
