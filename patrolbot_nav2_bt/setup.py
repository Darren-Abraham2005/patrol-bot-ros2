from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'patrolbot_nav2_bt'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'behaviour_trees'), glob('behaviour_trees/*'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='darren-abraham',
    maintainer_email='darrenpaulabraham@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
