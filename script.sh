set -xe
VERSION=1.0.0
VERSION=$(echo $VERSION | sed 's#.*/v##')
PLACEHOLDER='__version__ = "develop"'
VERSION_FILE='machinery/__init__.py'
# ensure the placeholder is there. If grep doesn't find the placeholder
# it exits with exit code 1 and github actions aborts the build.
grep "$PLACEHOLDER" "$VERSION_FILE"
sed -i "s/$PLACEHOLDER/__version__ = \"${VERSION}\"/g" "$VERSION_FILE"
