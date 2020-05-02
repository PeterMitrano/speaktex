from distutils.core import setup

setup(name='speaktex',
      description='read tex documents',
      author='Peter Mitrano',
      packages=[
          'speaktex'
      ],
      requires=[
          'tex2py'
      ],
      scripts=['scripts/speak'],
      )
