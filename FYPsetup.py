from distutils.core import setup
from setuptools import find_packages
import os
# Optional project description in README.md:
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''
setup(
	# Project name: 
name='cloudExtraction',
# Packages to include in the distribution: 
packages=find_packages(','),
# Project version number:
version='1.0',
# List a license for the project, eg. MIT License
license='MIT license',
# Short description of your library: 
description='this is a cubesat app for Cloud features extraction into a binary file \nusing personal made AI.\n',
# Long description of your library: 
long_description=long_description,
long_description_content_type='text/markdown',
# Your name: 
author='Ahmed Al-Badri',
# Your email address:
author_email='ahmed17badri@gmail.com',
# Link to your github repository or website: 
url='https://github.com/stone030',
# Download Link from where the project can be downloaded from:
download_url='https://github.com/stone030/cloudExtraction.git',
# List of keywords: 
keywords=['cubesat', 'clouds', 'atmosphere', 'AI', 'OpenCV'],
# List project dependencies: 
install_requires=[
'cv2',
'cvzone',
'numpy',
'urllib3',
'imutils',
],
# https://pypi.org/classifiers/ 
classifiers=[]
)
