"""Compatibility shim for older pip editable installs."""

from setuptools import find_packages, setup


setup(
    name="prime-clock-dynamics",
    version="3.0.0",
    description="Prime-periodic circle dynamics and angular sieve experiments.",
    package_dir={"": "src"},
    packages=find_packages("src"),
    python_requires=">=3.9",
    extras_require={
        "dev": [
            "pytest>=8.0",
            "ruff>=0.6",
        ],
    },
)
