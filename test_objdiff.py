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

    a = {"a": 1, "b": 2}
    b = {"c": 3, "d": 4}
    assert objdiff.dictdiff(a, b) == 1
    assert capsys.readouterr().out == "-a: 1\n-b: 2\n+c: 3\n+d: 4\n"


def test_complex_dict(capsys):
    a = {"a": {"b": {"c": {"d": 1, "e": 2}}}}
    b = {"a": {"f": 5, "b": {"g": 6, "c": {"d": 3, "e": 4}}}}
    expected_result = """ a:
   b:
     c:
-      d: 1
+      d: 3
-      e: 2
+      e: 4
+    g: 6
+  f: 5
"""
    assert objdiff.dictdiff(a, b) == 1
    assert capsys.readouterr().out == expected_result

    expected_result = """ a:
   b:
     c:
-      d: 3
+      d: 1
-      e: 4
+      e: 2
-    g: 6
-  f: 5
"""
    assert objdiff.dictdiff(b, a) == 1
    assert capsys.readouterr().out == expected_result


def test_list_of_objects(capsys):
    a = {"a": {"b": [{"c": 1}, {"d": 2}, {"e": 3}]}}
    b = {"a": {"b": [{"c": 1}, {"d": 4}, {"e": 3}]}}
    assert objdiff.dictdiff(a, b) == 1
    assert capsys.readouterr().out == " a:\n   b[1]:\n-    d: 2\n+    d: 4\n"
    assert objdiff.dictdiff(b, a) == 1
    assert capsys.readouterr().out == " a:\n   b[1]:\n-    d: 4\n+    d: 2\n"

    a = {"a": {"b": [{"c": 1}, {"e": 4}]}, "g": 5}
    b = {"a": {"b": [{"c": 1}, {"d": 3}, {"e": 4}, {"f": 5}]}, "g": 6, "h": 7}
    assert objdiff.dictdiff(a, b) == 1
    assert (
        capsys.readouterr().out
        == """ a:
   b[1]:
+    - d: 3
-    - e: 4
   b[2]:
+    - e: 4
   b[3]:
+    - f: 5
-g: 5
+g: 6
+h: 7
"""
    )

    assert objdiff.dictdiff(b, a) == 1
    assert (
        capsys.readouterr().out
        == """ a:
   b[1]:
-    - d: 3
+    - e: 4
   b[2]:
-    - e: 4
   b[3]:
-    - f: 5
-g: 6
+g: 5
-h: 7
"""
    )

    a = {"a": {"b": []}}
    b = {"a": {"b": [{"c": 1}, {"d": 2}]}}
    assert objdiff.dictdiff(a, b) == 1
    assert (
        capsys.readouterr().out
        == """ a:
   b[0]:
+    - c: 1
   b[1]:
+    - d: 2
"""
    )
    assert objdiff.dictdiff(b, a) == 1
    assert capsys.readouterr().out == (
        """ a:
   b[0]:
-    - c: 1
   b[1]:
-    - d: 2
"""
    )

    a = {"a": {"b": [{"c": 1}, {"d": 2}]}}
    b = {"a": {"b": [{"c": 1}, {"e": 3}, {"d": 2}]}}
    assert objdiff.dictdiff(a, b) == 1
    assert (
        capsys.readouterr().out
        == """ a:
   b[1]:
-    - d: 2
+    - e: 3
   b[2]:
+    - d: 2
"""
    )
    assert objdiff.dictdiff(b, a) == 1
    assert (
        capsys.readouterr().out
        == """ a:
   b[1]:
+    - d: 2
-    - e: 3
   b[2]:
-    - d: 2
"""
    )
