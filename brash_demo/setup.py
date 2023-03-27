from setuptools import setup

package_name = 'brash_demo'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml'])
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='swhart',
    maintainer_email='swhart@traclabs.com',
    description='BRASH Demo',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
            'console_scripts': [
                    'joint_state_convert = brash_demo.joint_state_convert:main'
            ],
    },
)
