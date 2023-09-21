from setuptools import setup

# exec(open("bolift/version.py").read())

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="doe",
    version="0.0.0", #__version__,
    description="",
    author="Mayk Caldas",
    author_email="maykcaldas@gmail.edu",
    url="https://github.com/maykcaldas/DOE",
    license="MIT",
    packages=["AgML", "BioNano"], #No module. Just using setuptools to install dependencies conveniently
    install_requires=[
        'numpy',
        'pandas',
        'xgboost',
        'scikit-learn',
        'bolift@git+https://github.com/ur-whitelab/BO-LIFT.git',
        'dash',
        'matplotlib',
        'plotly',
        'seaborn',
        'python-dotenv',
        'cloudpickle',
    ],
    extras_require={},
    test_suite="tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
