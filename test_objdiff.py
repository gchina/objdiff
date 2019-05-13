
import objdiff


def test_nodiff(capsys):
    a = {"a": 1, "b": 2, "c": {"d": 3, "e": 4}}
    b = {"c": {"e": 4, "d": 3}, "b": 2, "a": 1}
    assert objdiff.dictdiff(a, b) == 0
    assert capsys.readouterr().out == "No differences\n"

    assert objdiff.dictdiff(b, a) == 0
    assert capsys.readouterr().out == "No differences\n"


def test_simple_dict(capsys):
    a = {"a": 1, "b": 2, "c": 3}
    b = {"a": 1, "b": 4, "c": 3}
    assert objdiff.dictdiff(a, b) == 1
    assert capsys.readouterr().out == "-b: 2\n+b: 4\n"

    assert objdiff.dictdiff(b, a) == 1
    assert capsys.readouterr().out == "-b: 4\n+b: 2\n"


def test_complex_dict(capsys):
    a = {"a": {"b": {"c": {"d": 1, "e": 2}}}}
    b = {"a": {"f": 5, "b": {"g": 6, "c": {"d": 3, "e": 4}}}}
    assert objdiff.dictdiff(a, b) == 1
    assert capsys.readouterr().out == (
        " a:\n"
        "   b:\n"
        "     c:\n"
        "-      d: 1\n"
        "+      d: 3\n"
        "-      e: 2\n"
        "+      e: 4\n"
        "+    g: 6\n"
        "+  f: 5\n"
    )

    assert objdiff.dictdiff(b, a) == 1
    assert capsys.readouterr().out == (
        " a:\n"
        "   b:\n"
        "     c:\n"
        "-      d: 3\n"
        "+      d: 1\n"
        "-      e: 4\n"
        "+      e: 2\n"
        "-    g: 6\n"
        "-  f: 5\n"
    )


def test_list_of_objects(capsys):
    a = {"a": {"b": [{"c": 1}, {"d": 2}, {"e": 3}]}}
    b = {"a": {"b": [{"c": 1}, {"d": 4}, {"e": 3}]}}
    assert objdiff.dictdiff(a, b) == 1
    assert capsys.readouterr().out == (" a:\n" "   b[1]:\n" "-    d: 2\n" "+    d: 4\n")
    assert objdiff.dictdiff(b, a) == 1
    assert capsys.readouterr().out == (" a:\n" "   b[1]:\n" "-    d: 4\n" "+    d: 2\n")

    a = {"a": {"b": [{"c": 1}, {"e": 4}]}, "g": 5}
    b = {"a": {"b": [{"c": 1}, {"d": 3}, {"e": 4}, {"f": 5}]}, "g": 6, "h": 7}
    assert objdiff.dictdiff(a, b) == 1
    assert capsys.readouterr().out == (
        " a:\n"
        "   b[1]:\n"
        "+    - d: 3\n"
        "-    - e: 4\n"
        "   b[2]:\n"
        "+    - e: 4\n"
        "   b[3]:\n"
        "+    - f: 5\n"
        "-g: 5\n"
        "+g: 6\n"
        "+h: 7\n"
    )
    assert objdiff.dictdiff(b, a) == 1
    assert capsys.readouterr().out == (
        " a:\n"
        "   b[1]:\n"
        "-    - d: 3\n"
        "+    - e: 4\n"
        "   b[2]:\n"
        "-    - e: 4\n"
        "   b[3]:\n"
        "-    - f: 5\n"
        "-g: 6\n"
        "+g: 5\n"
        "-h: 7\n"
    )

    a = {"a": {"b": []}}
    b = {"a": {"b": [{"c": 1}, {"d": 2}]}}
    assert objdiff.dictdiff(a, b) == 1
    assert capsys.readouterr().out == (
        " a:\n"
        "   b[0]:\n"
        "+    - c: 1\n"
        "   b[1]:\n"
        "+    - d: 2\n"
    )
    assert objdiff.dictdiff(b, a) == 1
    assert capsys.readouterr().out == (
        " a:\n"
        "   b[0]:\n"
        "-    - c: 1\n"
        "   b[1]:\n"
        "-    - d: 2\n"
    )

    a = {"a": {"b": [{"c": 1}, {"d": 2}]}}
    b = {"a": {"b": [{"c": 1}, {"e": 3}, {"d": 2}]}}
    assert objdiff.dictdiff(a, b) == 1
    assert capsys.readouterr().out == (
        " a:\n"
        "   b[1]:\n"
        "-    - d: 2\n"
        "+    - e: 3\n"
        "   b[2]:\n"
        "+    - d: 2\n"
    )
    assert objdiff.dictdiff(b, a) == 1
    assert capsys.readouterr().out == (
        " a:\n"
        "   b[1]:\n"
        "+    - d: 2\n"
        "-    - e: 3\n"
        "   b[2]:\n"
        "-    - d: 2\n"
    )
