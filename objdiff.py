#!/usr/bin/env python3

import io
import sys
import tokenize

import click
import deepdiff
import yaml


__version__ = "0.1.0"


class DiffHandler:
    def __init__(self, color=True):
        self.add_color = "green" if color else None
        self.remove_color = "red" if color else None
        self.current_level = []

    def handle_level(self, new_level):
        """Print out the correct whitespace for the indentation level."""
        indent_level = 0
        for indent_level, level in enumerate(new_level):
            if (indent_level + 1) > len(
                self.current_level
            ) or level != self.current_level[indent_level]:
                click.echo(f" {'  ' * indent_level}{new_level[indent_level]}:")
        if new_level != []:
            indent_level += 1
        return indent_level

    def handle_dictionary_item_add_and_remove(self, diff, prefix, color):
        path = get_path(diff[1])
        if len(path) == 1:
            click.secho(f"{prefix}{path[0]}: {diff[2]}", fg=color)
            self.current_level = []
            return

        idx = self.handle_level(path[:-1])

        if "[" in path[-2]:
            click.secho(f"{prefix}{'  ' * idx}- {path[-1]}: {diff[2]}", fg=color)
        else:
            click.secho(f"{prefix}{'  ' * idx}{path[-1]}: {diff[2]}", fg=color)

        self.current_level = path[:-1]

    def handle_dictionary_item_added(self, diff):
        self.handle_dictionary_item_add_and_remove(diff, "+", self.add_color)

    def handle_dictionary_item_removed(self, diff):
        self.handle_dictionary_item_add_and_remove(diff, "-", self.remove_color)

    def handle_iterable_item_add_and_remove(self, diff, prefix, color):
        path = get_path(diff[1])
        idx = self.handle_level(path)
        click.secho(f"{prefix}{'  ' * idx}- {yaml.dump(diff[2]).strip()}", fg=color)
        self.current_level = path

    def handle_iterable_item_added(self, diff):
        self.handle_iterable_item_add_and_remove(diff, "+", self.add_color)

    def handle_iterable_item_removed(self, diff):
        self.handle_iterable_item_add_and_remove(diff, "-", self.remove_color)

    def handle_values_changed(self, diff):
        path = get_path(diff[1])
        if len(path) == 1:
            click.secho(f"-{path[-1]}: {diff[2]['old_value']}", fg=self.remove_color)
            click.secho(f"+{path[-1]}: {diff[2]['new_value']}", fg=self.add_color)
            self.current_level = []
            return

        idx = self.handle_level(path[:-1])
        click.secho(
            f"-{'  ' * idx}{path[-1]}: {diff[2]['old_value']}", fg=self.remove_color
        )
        click.secho(
            f"+{'  ' * idx}{path[-1]}: {diff[2]['new_value']}", fg=self.add_color
        )
        self.current_level = path

    def handle_diff(self, diff):
        """Command handler pattern"""
        command = diff[0]
        func = getattr(self, f"handle_{command}")
        return func(diff)


def get_path(item: str) -> list:
    path = list()
    for i in tokenize.generate_tokens(io.StringIO(item).readline):
        if i.type == tokenize.STRING:
            path.append(i.string.replace("'", ""))
        elif i.type == tokenize.NUMBER:
            path[-1] = f"{path[-1]}[{i.string}]"

    return path


def normalize_diffs(diffs: dict) -> dict:
    """
    Normalize the output of DeepDiff

    DeepDiff returns a dictionary of changes grouped by change type.  For our
    purposes, we need a list of ungrouped changes sorted by path.
    """
    normalized_diffs = list()
    for diff_type, diff_values in diffs.items():
        for path, value in diff_values.items():
            normalized_diffs.append((diff_type, path, value))
    return sorted(normalized_diffs, key=lambda x: x[1])


def dictdiff(dict1: dict, dict2: dict, color=True) -> int:
    diffs = deepdiff.DeepDiff(dict1, dict2, verbose_level=2)
    if not len(diffs):
        click.echo("No differences")
        return 0

    diffs = normalize_diffs(diffs)

    handler = DiffHandler(color)
    for diff in diffs:
        handler.handle_diff(diff)

    return 1


@click.command()
@click.version_option(version=__version__)
@click.argument("file1", type=click.File("r"))
@click.argument("file2", type=click.File("r"))
@click.option(
    "--color/--no-color",
    is_flag=True,
    default=True,
    help="Enable/disable color output (default: enabled)",
)
def objdiff(
    file1: click.File, file2: click.File, color: bool
) -> int:  # pragma: no cover
    """Diff two files containing either JSON or YAML objects."""
    try:
        dict1 = yaml.load(file1, Loader=yaml.Loader)
    except (yaml.scanner.ScannerError, yaml.parser.ParserError):
        click.echo(f"Unrecognized object notation in {file1.name}.")
        sys.exit(2)
    try:
        dict2 = yaml.load(file2, Loader=yaml.Loader)
    except (yaml.scanner.ScannerError, yaml.parser.ParserError):
        click.echo(f"Unrecognized object notation in {file2.name}.")
        sys.exit(2)

    return dictdiff(dict1, dict2, color)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(objdiff())
