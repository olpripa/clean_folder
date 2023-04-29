from setuptools import setup, find_namespace_packages

setup(
    name='Schone_Map',
    version='1.1.0',
    description='A script for sorting files by etemsion in folder',
    author='Oleksandr Pripa',
    author_email='ol.pripa@gmail.com',
    url='https://github.com/olpripa/clean_folder',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_namespace_packages(),
    entry_points={'console_scripts': [
        'cleanfolder=src.cleanfolder.sort:main']}
)
