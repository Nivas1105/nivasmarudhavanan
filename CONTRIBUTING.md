# Repository checks

Enable the repository's pre-push check once after cloning:

```sh
./scripts/install-git-hooks.sh
```

The hook blocks pushes that contain added or modified binary files in outgoing commits. Text changes remain unaffected. To share large assets, use Git LFS or host them outside this repository. The hook detects binary content through Git's diff output, so it is not limited to a filename extension.
