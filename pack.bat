del dist\* /q
python make_setup.py
python setup.py sdist
python -m twine upload dist/* --verbose
