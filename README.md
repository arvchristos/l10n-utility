# l10n utility for LO extensions

This utility helps the localization of LibreOffice extensions. It has started as a project to ease the localization of Page Numbering Addon extension.

### !!! Warning !!!

Currently under development so it only works for Page Numbering Addon. Global implementation to follow.

## Requirements
* Python 2.7
* Python packages
  * sys
  * os
  * argparse
  * zipfile
  * subprocess
* Linux packages
  * zip
  * poedit
  * itstool

## Usage

```bash
    python2.7 l10next.py path_to_oxt locale
```

For example:

```bash
    python2.7 l10next.py ./PageNumberingAddonPython-0.0.1.oxt it
```

The utility creates all required files at the same directory as l10next.py

After every edit, one has to follow the last option to compile a new oxt with the required localization. This is the file that should be commited for pull request along with the `*_extracted` directory