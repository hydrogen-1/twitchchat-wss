from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    version="0.0.1",
    name="twitchchat-wss",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="Twitch chat client using WebSockets",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    author="hydrogen-1",
    author_email="johannes@becker.computer",
    url="https://github.com/hydrogen-1/twitchchat-wss",
    install_requires=["websocket-client >= 1.6.4"],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    extra_require={
        "dev": ["twine>=4.0.2"]
    },
    python_requres=">=python3.9"
)
