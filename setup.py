from setuptools import find_packages, setup

package_name = 'lcd_i2c_my_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'smbus', 'time'],
    zip_safe=True,
    maintainer='axel',
    maintainer_email='axel@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "lcd_i2c_16x2 = lcd_i2c_my_robot.lcd_i2c_16x2:main",
        ],
    },
)
