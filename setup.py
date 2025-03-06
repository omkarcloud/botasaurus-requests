from setuptools import setup, find_packages

def get_description():
    try:
        with open("README.md", encoding="utf-8") as readme_file:
            long_description = readme_file.read()
        return long_description
    except:
        return None

setup(
    name="botasaurus_requests",
    version='4.0.38',
    description="botasaurus_requests is a fork of the requests library with the playwright dependencies removed.",
    long_description_content_type="text/markdown",
    long_description=get_description(),
    author="Chetan",
    author_email="chetan@omkar.cloud",
    maintainer="Chetan",
    maintainer_email="chetan@omkar.cloud",
    license="MIT",
    python_requires=">=3.5",
    keywords=[
        "tls", "client", "http", "scraping", "requests", "humans"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    install_requires=[
        "httpx",
        "geventhttpclient",
        "urllib3",
        "rich",
        "beautifulsoup4>=4.11.2",
        "click",
        "gevent"
    ],
    url="https://github.com/omkarcloud/botasaurus-requests",
    project_urls={
        "Homepage": "https://github.com/omkarcloud/botasaurus-requests",
        "Bug Reports": "https://github.com/omkarcloud/botasaurus-requests/issues",
        "Source": "https://github.com/omkarcloud/botasaurus-requests"
    },
    packages=find_packages(include=["botasaurus_requests"]),
    include_package_data=True,
)
