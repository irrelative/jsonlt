from setuptools import find_packages, setup

setup(
    name="jsonlt",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "jsonlt=jsonlt.cli:main",
        ],
    },
    author="Justin Davis",
    author_email="jedavis83@gmail.com",
    description="A JSON transformation library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/irrelative/jsonlt",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
