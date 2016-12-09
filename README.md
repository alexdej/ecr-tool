# ecr-tool
Command-line utility to list and optionally delete images from AWS ECR

## Usage

    ecr.py [-h] [--before BEFORE] [--after AFTER] [--untagged]
           [--prefix PREFIX] [--regexp REGEXP] [--invert]
           [--smaller SMALLER] [--larger LARGER] [--delete]
           repository

## Examples

List untagged images uploaded since October:

	python ecr.py myrepo --untagged --after 2016/10/01

Delete images tagged `master*` older than November:

	python ecr.py myrepo --prefix master --before 2016/11/01 --delete

Delete images *not* tagged `master*`:

	python ecr.py myrepo --prefix master -v --delete

Delete images larger than 500MB:

	python ecr.py myrepo --larger 500000000 --delete
