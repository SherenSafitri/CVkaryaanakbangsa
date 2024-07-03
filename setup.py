from setuptools import setup, find_packages

setup(
    name='nama-paket',
    version='1.0.0',
    packages=find_packages(),  # Temukan semua paket di dalam direktori ini
    install_requires=[
        'setuptools',
        'wheel',
        'numpy==1.19.3',
        'six',
    ],
    entry_points={
        'console_scripts': [
            'nama-perintah=nama_paket.modul:fungsi_utama',
        ],
    },
    author='Nama Penulis',
    author_email='email@domain.com',
    description='Deskripsi singkat tentang paket ini',
    url='https://github.com/SherenSafitri/CVkaryaanakbangsa.git',
)
