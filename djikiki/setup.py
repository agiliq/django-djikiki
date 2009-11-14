import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages
setup(
    name = "djikiki",
    version = "0.4",
    packages = find_packages(),
    author = "Shabda Raaj",
    author_email = "shabda@uswaretech.com",
    description = "A django based wiki",
    url = "https://svn.uswaretech.com/djikiki/trunk/djikiki/",
    include_package_data = True
)
