import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="ibvlib",
    version="0.1",
    author="Andreas Pösch",
    author_email="andreas.poesch@googlemail.com",
    description="Python functions for Lecture IBV",
    long_description=long_description,
    install_requires=requirements,
    long_description_content_type='text/markdown',
    url="https://github.com/mechaot/ibvlib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operting System :: OS Independent"
    ]
)
