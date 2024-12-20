if (Test-Path -Path "dist") {
    Remove-Item -Path "dist\*" -Recurse -Force
}
python make_setup.py
python setup.py sdist
python -m twine upload dist/* --verbose