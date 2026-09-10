"""Release packaging controls; never execute native control helpers."""
import importlib.util
import io
import json
from pathlib import Path
import re
import tarfile
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


class WorkflowTests(unittest.TestCase):
    def test_zip_uses_the_validated_npm_artifact(self):
        workflow = (ROOT / '.github/workflows/release.yml').read_text()
        self.assertIn('python tools/release_artifacts.py', workflow)
        self.assertNotIn('zip -r', workflow)
        self.assertNotIn('--clobber', workflow)

    def test_release_preserves_ci_contract_commands(self):
        def commands(name):
            text = (ROOT / '.github/workflows' / name).read_text()
            return re.findall(r'^\s+(node .+|python tools/test_release_artifacts.py)$',
                              text, re.MULTILINE)
        self.assertEqual(commands('ci.yml'), commands('release.yml'))


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location(
            'release_artifacts', ROOT / 'tools/release_artifacts.py')
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def pack(self, omit=None, extra=None, version='0.2.0'):
        files = {name: b'fixture' for name in self.module.REQUIRED_FILES}
        files['package.json'] = json.dumps({
            'name': 'project-telos-mcp', 'version': version,
            'bin': {'telos': './demo/telos.mjs',
                    'telos-mcp': './demo/telos-mcp.mjs'},
        }).encode()
        if omit:
            files.pop(omit)
        archive = self.root / 'project-telos-mcp-0.2.0.tgz'
        with tarfile.open(archive, 'w:gz') as handle:
            for name, data in files.items():
                member = tarfile.TarInfo('package/' + name)
                member.size = len(data)
                handle.addfile(member, io.BytesIO(data))
            if extra:
                member = tarfile.TarInfo(extra[0])
                if extra[1] == 'link':
                    member.type = tarfile.SYMTYPE
                    member.linkname = '../outside'
                handle.addfile(member, io.BytesIO())
        return archive, files

    def test_zip_contains_exact_npm_files_and_bytes(self):
        archive, files = self.pack()
        output = self.module.build(archive, 'v0.2.0', self.root)
        with zipfile.ZipFile(output) as zipped:
            self.assertEqual(set(zipped.namelist()),
                             {'telos/' + name for name in files})
            for name, data in files.items():
                self.assertEqual(zipped.read('telos/' + name), data)
        checksums = (self.root / 'SHA256SUMS.txt').read_text()
        self.assertIn(archive.name, checksums)
        self.assertIn(output.name, checksums)

    def test_missing_helpers_and_entrypoints_are_rejected(self):
        self.assertIn('verify_packet.mjs', self.module.REQUIRED_FILES)
        for name in self.module.REQUIRED_FILES:
            with self.subTest(name=name):
                archive, _ = self.pack(omit=name)
                with self.assertRaises(ValueError):
                    self.module.build(archive, 'v0.2.0', self.root)
                self.assertFalse((self.root / 'project-telos-demo-v0.2.0.zip').exists())

    def test_unsafe_and_unreviewed_entries_are_rejected(self):
        for name, kind in [
            ('package/../escape', ''), ('/absolute', ''),
            ('package/.env', ''), ('package/demo/.token', ''),
            ('package/protected/payload.json', ''),
            ('package/node_modules/tool.js', ''),
            ('package/tools/unreviewed.ps1', ''),
            ('package/demo/link', 'link'),
            ('package/demo/test.test.mjs', ''),
            ('package/demo/integrations/scankii-synthetic-corpus/data', ''),
            ('package/docs/brand/product-render-receipt.json', ''),
            ('package/demo/./not-canonical.mjs', ''),
        ]:
            with self.subTest(name=name):
                archive, _ = self.pack(extra=(name, kind))
                with self.assertRaises(ValueError):
                    self.module.build(archive, 'v0.2.0', self.root)

    def test_version_tag_and_existing_outputs_are_rejected(self):
        archive, _ = self.pack(version='0.1.0')
        with self.assertRaises(ValueError):
            self.module.build(archive, 'v0.2.0', self.root)
        archive, _ = self.pack()
        with self.assertRaises(ValueError):
            self.module.build(archive, '../v0.2.0', self.root)
        self.module.build(archive, 'v0.2.0', self.root)
        with self.assertRaises(FileExistsError):
            self.module.build(archive, 'v0.2.0', self.root)

    def test_content_gate_distinguishes_private_inputs_from_public_fixtures(self):
        check = self.module.validate_content
        for body in [{'source': 'C:/Users/fixture/Downloads/input.zip'},
                     {'source': '/home/fixture/input'},
                     {'font_inputs': [{'path': 'D:/Fonts/input.zip'}]}]:
            with self.subTest(body=body), self.assertRaises(ValueError):
                check('demo/data.json', json.dumps(body).encode())
        check('demo/data.json', b'{"url":"https://example.org/home/papers"}')
        check('demo/integrations/ci-triage-fixtures.json',
              b'{"log_text":"Build /home/runner/work/telos/telos"}')
        check('demo/detector.mjs', b'const detector = /home/;')


if __name__ == '__main__':
    unittest.main()
