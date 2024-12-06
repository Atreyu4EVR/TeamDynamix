from setuptools import setup, find_packages

setup(
    name="teamdynamix",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "pyjwt>=2.8.0"
    ],
    extras_require={
        'dev': [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "isort>=5.12.0",
            "mypy>=1.5.0",
            "pylint>=2.17.5",
            "pytest-mock>=3.11.1",
            "responses>=0.23.1"  # For mocking HTTP requests
        ],
        'optional': [
            "requests-cache>=1.1.0",
            "tenacity>=8.2.3"
        ]
    },
    python_requires=">=3.8",
    description="the unofficial, unsactioned Python library for the TeamDynamix API",
    author="Ron Vallejo",
    author_email="ronvallejo@gmail.com",
)