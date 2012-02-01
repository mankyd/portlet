import setuptools

requirements = [
    ]

setuptools.setup(
    name = "portlet",
    version = '0.1',
    author = "Dave Mankoff",
    author_email = "mankyd@gmail.com",
    description = "Frequently user pattern for generating html content",
    long_description = open("README.md").read(),
    test_suite = 'portlet.tests.test_all',
    license = "GPLv3",
    url = "https://github.com/mankyd/portlet",
    install_requires=requirements,
    packages = [
        "portlet",
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ]
)
