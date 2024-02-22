# What's this?
Iris dataset consists of 3 different types of irises’ (Setosa, Versicolour, and Virginica) petal and sepal length, stored in a 150x4 numpy.ndarray

This project implements a far simple machine learning algorithm which tries to guess the irises's types through their petal and sepal length.

You can download this Iris dataset [here](https://www.kaggle.com/datasets/vikrishnan/iris-dataset)
# Usage
There are two ways of obtaining this application: through the nix way and the common way.

## Through Nix
`nix run github:Markus328/Iris`

If you clone this repository, run `nix run` inside the project root.

## Common Way
Clone this repository and then run `python3 app.py` once you're inside the project root.

# Contributing
If using nix, clone this repository and inside project root, run `nix develop` and you will be in a shell which provides helpers for coding (some editors may need that) and the python3 binary.

you can also run `run-app` as alias for `python3 app.py`
