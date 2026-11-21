"""Create independent, standard ZIPs without changing accepted lesson content."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import json
import shutil
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'delivery'
RUN = ROOT / 'records/runs/attention-v3-001'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_zip(target, files, extra):
    payload = {name: (ROOT / name).read_bytes() for name in files}
    payload.update(extra)
    manifest = {
        'created_at': datetime.now(ZoneInfo('Asia/Taipei')).isoformat(),
        'source_commit': git('rev-parse', 'HEAD').strip(),
        'kind': target.stem,
        'files': {name: digest(data) for name, data in payload.items()},
    }
    payload['PACKAGE-MANIFEST.json'] = (json.dumps(
        manifest, ensure_ascii=False, indent=2) + '\n').encode()
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name, data in payload.items():
            archive.writestr('attention-v3/' + name, data)
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        for name, data in payload.items():
            assert archive.read('attention-v3/' + name) == data
    return {
        'file': target.name, 'bytes': target.stat().st_size,
        'entries': len(payload), 'zip_sha256': digest(target.read_bytes()),
        'crc': 'pass', 'all_archived_bytes_match': 'pass',
    }


def main():
    DEST.mkdir(exist_ok=True)
    state = json.loads((RUN / 'state.json').read_text())
    accepted = (ROOT / 'attention-v3.html').read_bytes()
    assert state['final_acceptance'] is True
    assert digest(accepted) == state['gate3_approval']['html_sha256']
    assert digest(accepted) == state['html_sha256']
    tracked = git('ls-files').splitlines()
    prefixes = (
        'wiki/', 'sources/', 'content/v3/', 'presentation/v3/', 'samples/v3/',
        'records/runs/attention-v3-001/', 'review-packets/v3-',
        'records/ingest/', 'records/checks/',
    )
    named = {
        'AGENTS.md', 'README.md', 'DELIVERY-v3.md', 'attention-v3.html',
        'attention-v3-sample.html', 'workflow/v3-graph.md',
        'tools/package_delivery.py', 'delivery/README.txt',
    }
    core = [name for name in tracked
            if (name in named or name.startswith(prefixes))
            and Path(name).suffix != '.png']
    screenshots = [name for name in tracked
                   if name.startswith('records/runs/attention-v3-001/screens/')
                   and name.endswith('.png')]
    text_paths = [name for name in tracked if Path(name).suffix != '.png']
    history = git('log', '--date=iso-strict', '--format=%H%n%ad%n%s%n').encode()
    patches = git('log', '--format=fuller', '--date=iso-strict', '-p',
                  '--no-ext-diff', '--no-renames', '--', *text_paths).encode()
    guide = (DEST / 'README.txt').read_bytes()
    checks = [write_zip(DEST / 'attention-assignment.zip', core, {
        'START-HERE.txt': guide, 'GIT-HISTORY.txt': history,
        'GIT-TEXT-HISTORY.patch': patches,
    })]
    checks.append(write_zip(DEST / 'attention-screenshots.zip', screenshots, {
        'SCREENSHOTS-README.txt': (
            'These are actual v3 test captures. See the corresponding JSON reports.\n'
            'aborted-prior-artifact captures are not evidence of a completed test.\n'
        ).encode(),
    }))
    with tempfile.TemporaryDirectory(prefix='attention-git-export-') as temp:
        bundle = Path(temp) / 'attention-history.bundle'
        subprocess.run(['git', 'bundle', 'create', str(bundle), '--all'],
                       cwd=ROOT, check=True, capture_output=True)
        subprocess.run(['git', 'bundle', 'verify', str(bundle)],
                       cwd=ROOT, check=True, capture_output=True)
        checks.append(write_zip(DEST / 'attention-git-history.zip', [], {
            'attention-history.bundle': bundle.read_bytes(),
            'GIT-HISTORY.txt': history, 'START-HERE.txt': guide,
        }))
    shutil.copyfile(ROOT / 'attention-v3.html', DEST / 'attention-final.html')
    assert (DEST / 'attention-final.html').read_bytes() == accepted
    result = {
        'time': datetime.now(ZoneInfo('Asia/Taipei')).isoformat(),
        'source_commit': git('rev-parse', 'HEAD').strip(),
        'accepted_html_sha256': digest(accepted),
        'html_copy': 'byte-identical', 'git_bundle_verify': 'pass',
        'packages': checks,
        'remote_file_service': 'not verified; local tests cannot test download UI',
    }
    (DEST / 'PACKAGE-CHECKS.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
