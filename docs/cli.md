# Command Line Interface

```console
$ gittable -h
Usage:
  gittable <command> [options]

Commands:
  download                    Download files from a GIT repo matching one or
                              more specified pattern(s).
  tag-version                 Tag your repo with the project version, if a tag
                              for that version doesn't already exist.
```

## gittable tag-version

Note: Currently, `setuptools`, `hatch`, and `poetry` python projects are
supported.

```console
$ gittable tag-version -h
usage: gittable tag-version [-h] [-m MESSAGE] [directory]

Tag your repo with the project version, if a tag for that version
doesn't already exist.

positional arguments:
  directory             Your project directory. If not provided, the current
                        directory will be used.

optional arguments:
  -h, --help            show this help message and exit
  -m MESSAGE, --message MESSAGE
                        The tag message. If not provided, the new version
                        number is used.
```

## gittable download

```console
$ gittable download -h
usage: gittable download [-h] [-b BRANCH] [-d DIRECTORY] [-u USER]
                         [-p PASSWORD]
                         repo [file [file ...]]

Download files from a git repository matching one or more specified file
names or glob patterns

positional arguments:
  repo                  Reference repository
  file                  One or more `glob` pattern(s) indicating a specific
                        file or files to include. If not provided, all files
                        in the repository will be included.

optional arguments:
  -h, --help            show this help message and exit
  -b BRANCH, --branch BRANCH
                        Retrieve files from BRANCH instead of the remote's
                        HEAD
  -d DIRECTORY, --directory DIRECTORY
                        The directory under which to save matched files. If
                        not provided, files will be saved under the current
                        directory.
  -u USER, --user USER  A username for accessing the repository
  -p PASSWORD, --password PASSWORD
                        A password for accessing the repository
```
