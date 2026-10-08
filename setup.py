import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

classifiers = [
    # Pick your license as you wish (should match "license" above)
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3.14",
    "Framework :: Django",
    "Framework :: Django :: 6.1",
]

setuptools.setup(
    name='unleash-django-util',
    version='1.0.0',
    author="Amir Alaghmandan",
    author_email="amir.amotlagh@gmail.com",
    description="Unleash Django utility package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/miare-ir/unleash-django",
    packages=setuptools.find_packages(exclude=["tests*"]),
    python_requires=">=3.12",
    install_requires=["python-dateutil>=2.9.0", "UnleashClient>=6.9.0", "Django>=6.1.2", "setuptools>=84.0.0"],
    classifiers=classifiers,
)
