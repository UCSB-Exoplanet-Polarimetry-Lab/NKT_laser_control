from setuptools import setup, find_packages

setup(
    name='NKT_laser_control',  # Replace with your package name
    version='0.1.0',  # Replace with your package version
    author='William Melby',  # Replace with your name
    author_email='wcmelby@ucsb.edu',  # Replace with your email
    description='Python controls for NKT Photonics components.',
    packages=find_packages(include=['nkt_controls', 'nkt_controls.*']),
    # install_requires=[
    #     # List your package dependencies here
    #     # 'some_package>=1.0.0',
    # ],
    # classifiers=[
    #     'Programming Language :: Python :: 3',
    #     'License :: OSI Approved :: MIT License',
    #     'Operating System :: OS Independent',
    # ],
    python_requires='>=3.6',  # Specify the Python version requirement
)