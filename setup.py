import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django_firebase_scrypt",
    version="0.0.2",
    author="Matthew Simpson",
    author_email="mcsimps2@gmail.com",
    description="A Django password hasher to use for users imported from Firebase",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mcsimps2/django-firebase-scrypt",
    packages=["django_firebase_scrypt"],
    install_requires=["pyscryptfirebase"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        "Framework :: Django :: 3.0",
        'License :: OSI Approved :: MIT License',
    ],
)
