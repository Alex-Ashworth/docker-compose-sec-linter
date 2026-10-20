import unittest
from contextlib import redirect_stdout
from io import StringIO

from compose_linter.parsing import (
    parse_image,
    parse_port,
    parse_protocol,
    parse_reference,
    parse_volume,
)


class ImageParsingTests(unittest.TestCase):
    def test_image_parts(self):
        digest = "sha256:" + "a" * 64
        cases = [
            ("postgres", ("docker.io", "library", "postgres", "latest", None)),
            (
                "postgres:16-alpine",
                ("docker.io", "library", "postgres", "16-alpine", None),
            ),
            ("gitea/gitea:latest", ("docker.io", "gitea", "gitea", "latest", None)),
            ("team/project/app", ("docker.io", "team/project", "app", "latest", None)),
            ("ghcr.io/team/app:v1", ("ghcr.io", "team", "app", "v1", None)),
            (
                "docker.io/postgres",
                ("docker.io", "library", "postgres", "latest", None),
            ),
            ("localhost:5000/app", ("localhost:5000", None, "app", "latest", None)),
            ("localhost/app:v1", ("localhost", None, "app", "v1", None)),
            (
                "registry.example:5000/team/project/app:v1",
                ("registry.example:5000", "team/project", "app", "v1", None),
            ),
            ("[::1]:5000/team/app:v1", ("[::1]:5000", "team", "app", "v1", None)),
            (f"postgres@{digest}", ("docker.io", "library", "postgres", None, digest)),
            (
                f"postgres:16@{digest}",
                ("docker.io", "library", "postgres", "16", digest),
            ),
            (
                f"localhost:5000/team/project/app@{digest}",
                ("localhost:5000", "team/project", "app", None, digest),
            ),
        ]
        for entry, expected in cases:
            with self.subTest(entry=entry):
                self.assertEqual(parse_image(entry), expected)

    def test_invalid_image_parts(self):
        cases = [
            "",
            " ",
            " postgres",
            "postgres ",
            "post gres",
            "postgres\n",
            ":16",
            "postgres:",
            "postgres:16:alpine",
            "/postgres",
            "team//postgres",
            "team/",
            "ghcr.io/team:v1/app",
            "postgres@",
            "@sha256:abc",
            "postgres@sha256",
            "postgres@:abc",
            "postgres@sha256:",
            "postgres@sha256:abc:def",
            "postgres@sha256:abc@sha256:def",
        ]
        for entry in cases:
            with self.subTest(entry=entry):
                output = StringIO()
                with redirect_stdout(output):
                    result = parse_image(entry)
                self.assertEqual(result, (None, None, None, None, None))
                self.assertIn("Could not parse image:", output.getvalue())

    def test_reference_parts(self):
        self.assertEqual(parse_reference("postgres:16"), ("postgres:16", None))
        self.assertEqual(
            parse_reference("postgres:16@sha256:abc"), ("postgres:16", "sha256:abc")
        )


class ExistingParsingTests(unittest.TestCase):
    def test_port(self):
        self.assertEqual(parse_port("127.0.0.1:8080:80"), ("127.0.0.1", "8080", "80"))

    def test_protocol(self):
        self.assertEqual(parse_protocol("8080:80"), ("8080:80", "tcp"))

    def test_volume(self):
        self.assertEqual(parse_volume("./data:/data:ro"), ("./data", "/data", "ro"))


if __name__ == "__main__":
    unittest.main()
