from setuptools import setup, find_packages
from yspeed import _version

setup(
    name="yspeed",
    version=_version(),
    packages=find_packages(),
    install_requires=[
        "requests",
        "selenium",
        "rich",
        "halo",
    ],
    author="Foufou-exe",
    author_email="lumina.networks34@gmail.com",
    description="Yspeed is a library that scrapes the Speedtest site",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Foufou-exe/Yspeed",
    py_modules=["yspeed"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
