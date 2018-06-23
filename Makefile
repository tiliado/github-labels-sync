check: mypy flake8 pylint

mypy:
	mypy --strict github_labels_sync

flake8:
	flake8 github_labels_sync

pylint:
	pylint --rcfile .pylintrc github_labels_sync

