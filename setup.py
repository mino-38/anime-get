from setuptools import setup

setup(
    name="anime-get",
    author="minomushi",
    version="1.0.0",
    description="Get anime information",
    keywords="anime",
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "anime-get=anime_get:man"
        ]
    },
    url="https://github.com/mino-38/anime-get"
)