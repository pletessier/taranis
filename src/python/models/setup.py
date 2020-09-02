# coding: utf-8

"""
   Taranis Client
"""

from setuptools import setup  # noqa: H301

NAME = "taranis-cli"
VERSION = "0.3.2"
REQUIRES = ["grpcio==1.21.1", "grpcio-tools==1.21.1"]

setup(
    name=NAME,
    version=VERSION,
    description="Taranis client",
    author="Pierre Letessier",
    author_email="",
    url="https://github.com/pletessier/taranis",
    keywords=["lib", "taranis", "client"],
    install_requires=REQUIRES,
    packages=["."],
    include_package_data=True,
    long_description="""\
    Taranis client
    """
)
