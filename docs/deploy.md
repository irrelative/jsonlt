# Deploy steps

## Python

```sh
python setup.py sdist bdist_wheel
twine upload dist/*
```
