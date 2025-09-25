from setuptools import setup

package_name = 'drone_ai_sim_ros'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='connor',
    maintainer_email='you@example.com',
    description='ROS 2 utilities for drone_ai_sim',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'republish = drone_ai_sim_ros.republish:main',
            'odom_tf_broadcaster = drone_ai_sim_ros.odom_tf_broadcaster:main'
        ],
    },
)
