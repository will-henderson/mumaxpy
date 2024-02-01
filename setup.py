import setuptools

setuptools.setup(
    name="mumaxpy",
    version="0.0.3", 
    author="Will Henderson",
    description="Python Interface to mumax3",
    packages=setuptools.find_packages(),
    python_requires='>3.10',
    install_requires=[
        'numpy',
        'grpcio',
        'grpcio-tools',
        'discretisedfield'
    ],
    py_modules=["mumaxpy"],
    package_dir={'':'.'},
)