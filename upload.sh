#!/bin/bash
rm -rf build dist wapchita.egg-info
python3 setup.py sdist bdist_wheel
twine upload dist/*
