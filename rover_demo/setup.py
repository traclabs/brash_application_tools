import os
from glob import glob
from setuptools import setup

package_name = 'rover_demo'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*.perspective'))),    
        (os.path.join('share', package_name, 'rviz'), glob(os.path.join('rviz', '*.rviz'))),     
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*')))     
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Ana C. Huaman Quispe',
    maintainer_email='ana@traclabs.com',
    description='BRASH Rover Demo',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
            'console_scripts': [
                    'twist_odom_convert = rover_demo.twist_odom_convert:main'
            ],
    },
)
