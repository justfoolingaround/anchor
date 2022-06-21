from setuptools import find_packages, setup

from anchor import __version__

setup(
    name="anchor-kr",
    version=__version__,
    author="kr@justfoolingaround",
    author_email="kr.justfoolingaround@gmail.com",
    description="Me, you and anchor make your scraper complete.",
    packages=find_packages(),
    url="https://github.com/justfoolingaround/anchor",
)
