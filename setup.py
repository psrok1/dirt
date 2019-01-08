from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requires = f.read().splitlines()

setup(name='dirt',
      version="1.0.0-alpha",
      description="Dirty Incident Response Toolkit",
      author='psrok1',
      packages=find_packages('.', exclude=['examples*', 'test*']) + ["dirt_plugins.empty_plugin"],
      include_package_data=True,
      install_requires=requires,
      entry_points={
          'console_scripts': ['dirt = dirt:main'],
      },
      scripts=[
          'scripts/dirt-bash'
      ],
      zip_safe=False)
