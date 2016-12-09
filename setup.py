from setuptools import setup

setup(
    name='ecr-tool',
    description="Command-line tool to list and optionally delete images in an AWS ECR repository",
    url='https://github.com/alexdej/ecr-tool',
    author='Alex Dejarnatt',
    author_email='adejarnatt@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
    ],
    keywords='aws ecr image',
    install_requires=[
        'boto3>=1.4.2',
        'python-dateutil>=2.6.0',
    ]
)
