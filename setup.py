from setuptools import find_packages, setup

setup(
    name="ai-pr-reviewer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "pyyaml",
        "tomli; python_version < '3.11'",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "ai-pr-reviewer=core.cli:main",
        ],
    },
)
