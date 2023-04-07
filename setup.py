from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name='Discord_Rust_Team_bot',
    version='0.1.0',    
    description="!!! add short description !!!",
    long_description = readme,
    long_description_content_type="text/markdown",
    url='https://github.com/NapoII/Discord_Rust_Team_bot',
    author='NapoII',
    author_email='!!! add mail !!!',
    license='MIT License',
    packages="!!! add content from requirements.txt !!!",
    install_requires= [],

    classifiers=[
    !!! add classifiers !!!
        ],)