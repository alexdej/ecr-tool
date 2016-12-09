# ecr-tool
Command-line utility to list and optionally delete images from AWS ECR

## Examples

List untagged images uploaded since October:

	python ecr.py myrepo --untagged --after 2016/10/01

List and delete images tagged `master*` older than November:

	python ecr.py myrepo --prefix master --before 2016/11/01 --delete
