"""Build the release zip from validated npm-pack bytes using only the stdlib."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import tarfile
from urllib.parse import urlparse
import zipfile

REQUIRED_FILES = {
    'package.json', 'LICENSE', 'README.md', 'USAGE.md',
    'demo/telos.mjs', 'demo/telos-mcp.mjs',
    'demo/native-control/app.mjs', 'demo/native-control/device.mjs',
    'tools/uia.ps1', 'tools/device.ps1', 'docs/native-control-contract.md',
}
ROOT_FILES = {'package.json', 'LICENSE', 'README.md', 'USAGE.md'}
EXCLUDED = {'node_modules', 'protected', 'secrets', 'private', 'credentials',
            'scankii-synthetic-corpus', 'smallharness-dogfood-pack'}
LOCAL_HOME = re.compile(r'(?<![\w:/])(?:[A-Za-z]:/(?:Users|Documents and Settings)/|/(?:Users|home)/)', re.I)


def validate_content(name, data):
    """Inspect data values, not detector source or public URL path fragments."""
    if not name.endswith(('.json', '.md')):
        return

    def visit(value, key=''):
        if isinstance(value, dict):
            if 'font_inputs' in value:
                raise ValueError('local font input metadata is not a release payload')
            for field, child in value.items():
                visit(child, field)
        elif isinstance(value, list):
            for child in value:
                visit(child, key)
        elif isinstance(value, str):
            if urlparse(value).scheme.lower() in {'https', 'http'}:
                return
            normalized = value.replace('\\', '/')
            if name == 'demo/integrations/ci-triage-fixtures.json' and key == 'log_text':
                normalized = normalized.replace('/home/runner/work/', '/public-ci-workspace/')
            if LOCAL_HOME.search(normalized):
                raise ValueError('local home path is not a release payload')

    visit(json.loads(data) if name.endswith('.json') else data.decode('utf8'))


def read_package(archive, tag):
    if not re.fullmatch(r'v\d+\.\d+\.\d+', tag):
        raise ValueError('release tag must be vMAJOR.MINOR.PATCH')
    files = {}
    with tarfile.open(archive, 'r:gz') as packed:
        for member in packed.getmembers():
            parts = PurePosixPath(member.name).parts
            if (not member.isfile() or not member.name.startswith('package/')
                    or member.name != '/'.join(parts)
                    or '\\' in member.name or any(ord(c) < 32 for c in member.name)
                    or any(p in {'..', '.'} or p.startswith('.') for p in parts)
                    or any(p.lower() in EXCLUDED for p in parts)):
                raise ValueError('unsafe or excluded npm archive entry')
            name = member.name.removeprefix('package/')
            allowed = (name in ROOT_FILES or name.startswith('demo/')
                       or name.startswith('docs/brand/')
                       or name in {'docs/CURRENT-STATE.md',
                                   'docs/native-control-contract.md',
                                   'tools/uia.ps1', 'tools/device.ps1'})
            if (not allowed or name.endswith('.test.mjs')
                    or name.endswith('-render-receipt.json')
                    or name == 'demo/README.md' or name in files):
                raise ValueError('unreviewed or duplicate npm archive entry')
            if member.size > 16 * 1024 * 1024:
                raise ValueError('archive member exceeds release size limit')
            files[name] = packed.extractfile(member).read()
            validate_content(name, files[name])
            if len(files) > 1000 or sum(map(len, files.values())) > 64 * 1024 * 1024:
                raise ValueError('archive exceeds release size limit')
    if not REQUIRED_FILES.issubset(files):
        raise ValueError('npm package lacks required helpers or entrypoints')
    package = json.loads(files['package.json'])
    if (package.get('name') != 'project-telos-mcp'
            or package.get('version') != tag[1:]
            or package.get('bin') != {
                'telos': './demo/telos.mjs', 'telos-mcp': './demo/telos-mcp.mjs'}):
        raise ValueError('package identity, version or entrypoints do not match release')
    return files


def build(archive, tag, output_dir):
    archive, output_dir = Path(archive), Path(output_dir)
    files = read_package(archive, tag)
    output = output_dir / f'project-telos-demo-{tag}.zip'
    checksums = output_dir / 'SHA256SUMS.txt'
    if output.exists() or checksums.exists():
        raise FileExistsError('release outputs already exist; refusing overwrite')
    output_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED) as zipped:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo('telos/' + name)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100755 if name in {
                'demo/telos.mjs', 'demo/telos-mcp.mjs'} else 0o100644) << 16
            zipped.writestr(info, data)
    with checksums.open('x', encoding='utf8', newline='\n') as receipt:
        for artifact in (archive, output):
            digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
            receipt.write(f'{digest}  {artifact.name}\n')
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tarball', required=True, type=Path)
    parser.add_argument('--tag', required=True)
    parser.add_argument('--output-dir', required=True, type=Path)
    args = parser.parse_args()
    print(build(args.tarball, args.tag, args.output_dir))
