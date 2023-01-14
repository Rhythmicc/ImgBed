from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
VERSION = "0.0.0"

setup(
    name="ImgBed",
    version=VERSION,
    description="上传多个图片或Markdown文件内的所有图片到腾讯云或者阿里云",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="ImgBed",
    author="RhythmLian",
    url="https://github.com/Rhythmicc/ImgBed",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=["Qpro", "QuickStart_Rhy"],
    entry_points={
        "console_scripts": [
            "ImgBed = ImgBed.main:main",
        ]
    },
)
