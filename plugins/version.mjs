// MyST plugin: the {version} role renders "Version <hash> (<date>)" for the
// commit the site is built from, linked to the commit on GitHub.
// Used in footer.md. The hash and date are those of the checkout's HEAD; on PR
// builds that is the merge commit, the same one the preview comment names.
import { execSync } from 'node:child_process';

const REPO_URL = 'https://github.com/SIVACOR/documentation';

function git(args) {
  try {
    return execSync(`git ${args}`, { encoding: 'utf8' }).trim();
  } catch {
    return '';
  }
}

const sha = git('rev-parse HEAD');
const short = git('rev-parse --short HEAD');
const date = git('log -1 --format=%cs');

const versionRole = {
  name: 'version',
  doc: 'The commit hash and date the site was built from.',
  body: { type: String, required: false },
  run() {
    if (!sha) return [{ type: 'text', value: 'Version unknown' }];
    return [
      { type: 'text', value: 'Version ' },
      {
        type: 'link',
        url: `${REPO_URL}/commit/${sha}`,
        children: [{ type: 'text', value: `${short} (${date})` }],
      },
    ];
  },
};

const plugin = { name: 'Build version', roles: [versionRole] };

export default plugin;
