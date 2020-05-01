import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="solar-pkg-fredrik",
    version="0.0.1",
    author="Fredrik Thernelius",
    description="Get data from the Fronius Solar API",
    url="https://github.com/fredde975/solar_project",
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)