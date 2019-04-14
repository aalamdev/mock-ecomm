from setuptools import setup, find_packages
import os


def find_files(root, prune=[]):
    return [os.path.join(root, f) for f in os.listdir(root) if os.path.isfile(
        os.path.join(root, f))]


setup(
    name='aalamecomm_app',
    description='Test application',
    packages=find_packages(),
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Environment :: No Input/Output (Daemon)'],
    install_requires=['aalam-common'],
    data_files=[('resources', find_files("resources")),
                ('resources/images', find_files("resources/images"))]
)
