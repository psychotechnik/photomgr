from setuptools import setup, find_packages

setup(
    name='photomgr',
    version='0.1',
    include_package_data=True,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        photo_importer.py=photomgr.photo_importer:organize_images
        zmq_streamer.py=photomgr.zmqutils.streamer:streamer_device
        push_server.py=photomgr.zmqutils.push_server:server
        push_test.py=photomgr.zmqutils.push_test:run_test
    ''',
)
