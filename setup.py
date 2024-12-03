from setuptools import setup, find_packages

setup(
    name='NKTcontrols',  # Replace with your package name
    version='0.1.0',  # Replace with your package version
    author='William Melby',  # Replace with your name
    author_email='wcmelby@ucsb.edu',  # Replace with your email
    description='Python controls for NKT Photonics components.',
    long_description=open('README.md').read(),  # Use your README for a detailed description
    long_description_content_type='text/markdown',  # Use 'text/x-rst' for reStructuredText
    packages=find_packages(where='.', include=['NKTcontrols*']),  # Automatically include submodules
    # install_requires=[
    #     # 'numpy>=1.18.0',  # Example dependency
    #     # 'matplotlib>=3.3.0',
    # ],
    # classifiers=[
    #     'Programming Language :: Python :: 3',
    #     'License :: OSI Approved :: MIT License',  # or your actual license
    #     'Operating System :: OS Independent',
    # ],
    # python_requires='>=3.6',  # Specify the Python version requirement
    # license='MIT',  # or your actual license
)