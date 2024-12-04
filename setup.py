from setuptools import setup, find_packages

setup(
    name='github_repo_cloner',
    version='1.0.0',
    author='Khushal Pareta',
    author_email='khushalpareta@example.com',
    description='A tool to fetch and clone GitHub repositories',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'repo-cloner=main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
