from setuptools import find_packages, setup

package_name = 'offboard'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='stepan',
    maintainer_email='stepan@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'arm = offboard.arm:main',
        'offboard_mission = offboard.offboard_mission:main',
        'vzlet = offboard.vzlet:main',
        'dopredu = offboard.dopredu:main',
        'pristani = offboard.pristani:main',
        'letova_mise = offboard.letova_mise:main',
        'reset_offboard = offboard.reset_offboard:main', 
        ],
    },
)
