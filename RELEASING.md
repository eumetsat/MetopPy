# Releasing metoppy

1. checkout main branch
2. pull from repo
3. run the unittests
4. Update the `CHANGELOG.md` file.
5. Create a tag with the new version number, starting with a 'v', eg:

   ```
   git tag -a v<new version> -m "Version <new version>"
   ```

   For example if the previous tag was `v0.9.0` and the new release is a
   patch release, do:

   ```
   git tag -a v0.9.1 -m "Version 0.9.1"
   ```

   See [semver.org](http://semver.org/) on how to write a version number.


6. push changes to github `git push --follow-tags`
7. Verify github action unittests passed.
8. Create a "Release" on GitHub by going to
   https://github.com/eumetsat/MetopDatasets.jl/releases and clicking "Draft a new release".
   On the next page enter the newly created tag in the "Tag version" field,
   "Version X.Y.Z" in the "Release title" field, and paste the markdown from
   the changelog (the portion under the version section header) in the
   "Describe this release" box. Finally click "Publish release".

9. Now you can start the process to release on PyPI (only admins)

9.1 Build package

Now generate the distribution. To build the package, use PyPA build.

1. Install the build tool
```bash
pip install -q build
```

```bash
python3 -m build
```

you will end up with a `/dist` file. The .whl file and .tar.gz can then be distributed and installed or pushed to PyPI.

9.2 Push package to PyPI

Install twine
```bash
pip install twine
```

If you want to test first, use TestPyPI:
```bash
twine upload --repository testpypi dist/*
```

To upload your package to PyPI, use Twine:
```bash
twine upload dist/*
```
You'll be prompted for your PyPI username & password.
