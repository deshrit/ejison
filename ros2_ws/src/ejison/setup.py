import os
from glob import glob
from setuptools import find_packages, setup

package_name = "ejison"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (
            # Launch files
            os.path.join("share", package_name, "launch"),
            glob(os.path.join("launch/*")),
        ),
        (
            # Model files
            os.path.join("share", package_name, "model"),
            glob(os.path.join("model", "*.xacro")),
        ),
        (
            # Config files
            os.path.join("share", package_name, "config"),
            glob("config/*"),
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="deshrit",
    maintainer_email="deshritbaral@gmail.com",
    description="A monocular SLAM implementation robot with Raspberry Pi and Arduino Uno board with 28BYJ48 stepper motors.",
    license="MIT",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [],
    },
)
