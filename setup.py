import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

classifiers = [
    # Pick your license as you wish (should match "license" above)
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Framework :: Django",
    "Framework :: Django :: 2.2",
    "Framework :: Django :: 3.0",
    "Framework :: Django :: 3.1",
    "Framework :: Django :: 3.2",
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
    install_requires=["python-dateutil>=2.9.0", "UnleashClient>=6.4.0", "Django>=5.2.8"],
    classifiers=classifiers,
)
