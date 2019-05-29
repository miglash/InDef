import setuptools

with open("README.md", "r") as fh:
     long_description = fh.read()

setuptools.setup(
    name="InDef",
    version="0.0.1",
    author="Migle Grauzinyte",
    author_email="m.grauzinyte@gmail.com",
    description="A visual defect calculation analysis tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/miglash/InDef",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    license="MIT"
)
