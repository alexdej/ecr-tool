import argparse
import boto3
import dateutil.parser
import dateutil.tz
import re


def localdate(s):
  d = dateutil.parser.parse(s)
  return d if d.tzinfo else d.replace(tzinfo=dateutil.tz.tzlocal())

parser = argparse.ArgumentParser(description="Clean old images from ECR")
parser.add_argument('repository', type=str, help="Name of repository")
parser.add_argument('--before', type=localdate,
                    help="Only include images before date")
parser.add_argument('--after', type=localdate,
                    help="Only include images after date")
parser.add_argument('--untagged', action='store_true',
                    help="Include only images without any tag")
parser.add_argument('--prefix', type=str, help="Match tag name by prefix")
parser.add_argument('--regexp', type=str, help="Match tag name by regexp")
parser.add_argument('--invert', '-v', action='store_true',
                    help="Invert tag matching: exclude instead of include")
parser.add_argument('--min-size', type=int,
                    help="Only include images larger than this value in bytes")
parser.add_argument('--max-size', type=int,
                    help="Only include images smaller than this value in bytes")

parser.add_argument('--delete', action='store_true', help="Delete matching images")

ecr = boto3.client('ecr')


def describe_images(repo):
  token = None
  while True:
    if token:
      res = ecr.describe_images(repositoryName=repo, nextToken=token)
    else:
      res = ecr.describe_images(repositoryName=repo)

    for img in res.get('imageDetails'):
      yield img

    token = res.get('nextToken')
    if not token:
      break


def chunks(l, n=100):
  for i in xrange(0, len(l), n):
    yield l[i:i + n]


def main():
  args = parser.parse_args()

  filters = []

  if args.before:
    filters.append(lambda img: img.get('imagePushedAt') <= args.before)

  if args.after:
    filters.append(lambda img: img.get('imagePushedAt') >= args.after)

  if args.min_size:
    filters.append(lambda img: img.get('imageSizeInBytes', 0) > args.min_size)

  if args.max_size:
    filters.append(lambda img: img.get('imageSizeInBytes', 0) > args.max_size)

  if args.untagged:
    filters.append(lambda img: not img.get('imageTags', []))

  regexp = None
  if args.prefix:
    regexp = re.compile(args.prefix)

  if args.regexp:
    regexp = re.compile(args.regexp)

  if regexp:
    def match_tags(img):
      return any([regexp.match(tag) for tag in img.get('imageTags', [])])

    if args.invert:
      filters.append(lambda img: img.get('imageTags') and not match_tags(img))
    else:
      filters.append(match_tags)

  matched = []
  for img in describe_images(args.repository):
    if all(f(img) for f in filters):
      matched.append(img)
      print ' '.join(map(str, [
          img.get('imagePushedAt'),
          img.get('imageSizeInBytes'),
          img.get('imageDigest'),
          ','.join(sorted(img.get('imageTags', []))),
      ]))

  print 'Matched', len(matched), 'images'
  if matched and args.delete:
    if re.match('[Yy]', raw_input('Delete? (y/n) ')):
      print 'Deleting...'
      for batch in chunks(matched, n=100):
        res = ecr.batch_delete_image(
            repositoryName=args.repository,
            imageIds=[{'imageDigest': img.get('imageDigest')} for img in batch])
        print 'Deleted', len(res.get('imageIds', [])), 'images'
        for err in res.get('failures', []):
          print 'Error:', err

if __name__ == '__main__':
  main()
