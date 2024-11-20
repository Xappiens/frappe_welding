from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in welding/__init__.py
from welding import __version__ as version

setup(
	name="welding",
	version=version,
	description="Custom App to manage welder, welding qualifications, procedures, test and many more.",
	author="Xappiens",
	author_email="xappiens@xappiens.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
