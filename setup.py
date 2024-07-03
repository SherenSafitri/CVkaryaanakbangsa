from setuptools import setup, find_packages

setup(
    name='nama-paket',
    version='1.0.0',
    packages=find_packages(),  # Temukan semua paket di dalam direktori ini
    install_requires=[
        'paket-dependency1>=1.0.0',
        'paket-dependency2>=2.1.0',
    ],
    entry_points={
        'console_scripts': [
            'nama-perintah=nama_paket.modul:fungsi_utama',
        ],
    },
    author='Nama Penulis',
    author_email='email@domain.com',
    description='Deskripsi singkat tentang paket ini',
    url='https://github.com/username/nama-paket',
)
