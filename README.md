# objdiff

objdiff is a command-line utility to diff YAML/JSON files.

## Installation

Download the appropriate binary from the [releases]
(https://github.com/gchina/objdiff/releases) page and rename to objdiff. 
Mark the file as executable via `chmod +x objdiff`.  Copy the objdiff file
somewhere in your `$PATH`.

## Usage

`objdiff FILE1 FILE2`

objdiff can show the differences between files containing either JSON or YAML
objects.  Output will be colorized by default but can be disabled by passing the
`--no-color` flag.

objdiff can also diff a file against stdin:

`kubectl get deployments foo | objdiff foo.yaml -`