from setuptools import setup, find_packages

from setup_utils import build_dependency_links

with open('README.md') as readme_file:
    README = readme_file.read()

with open('requirements.txt') as requirements_file:
    REQUIREMENTS = requirements_file.read().split("\n")


setup_args = dict(
    name='plugp100',
    version='2.1.10b3',
    install_requires=REQUIREMENTS,
    description='Controller for TP-Link Tapo P100 and other devices',
    long_description_content_type="text/markdown",
    long_description=README,
    license='GPL3',
    packages=find_packages(),
    author='@petretiandrea',
    author_email='petretiandrea@gmail.com',
    keywords=['Tapo', 'P100'],
    url='https://github.com/petretiandrea/plugp100',
    download_url='https://github.com/petretiandrea/plugp100',
    classifiers=[
        # 'Development Status :: 4 - Beta',
        'Development Status :: 5 - Production/Stable'
    ],
    dependency_links=build_dependency_links()
)

if __name__ == '__main__':
    setup(**setup_args)
