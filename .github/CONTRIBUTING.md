Contributing to Debatekeeper formats
====================================

Thank you for considering submitting a contribution to the official Debatekeeper debate formats repository!

This page has some information about what you agree to by submitting your debate format, and what you can expect to happen after your contribution is accepted ("merged").

> This page is primarily written for an audience not already familiar with open-source licences. If you're familiar with open source conventions, most of this will be familiar to you, though please consider checking the [Conventions in this repository](#conventions-in-this-repository) section.

Contents
--------

* [Contributions of debate style format files](#contributions-of-debate-style-format-files)
   * [Licence information](#licence-information)
   * [How to submit a new format](#how-to-submit-a-new-format)
   * [Conventions in this repository](#conventions-in-this-repository)
   * [What happens when you submit](#what-happens-when-you-submit)
   * [When will my format become available on Debatekeeper?](#when-will-my-format-become-available-on-debatekeeper)
* [Contributions of other code](#contributions-of-other-code)

Contributions of debate style format files
------------------------------------------

### Licence information

First, some legal stuff. By submitting to this repository, you're agreeing to have your contributions licensed under the MIT License. You can see the licence text in [the LICENCE.md](https://github.com/czlee/debatekeeper-formats/tree/main/LICENCE.md) file.

As a definitely-not-legal-advice summary, this licence allows anyone to use all code in this repository without restriction, subject only to a requirement to retain copyright and licence information. This _includes_ use for purposes other than Debatekeeper, and it _includes_ commercial uses. For example, if someone wants to use the format files in this repository in a new debating app, they're allowed to do so.

If you'd like to discuss any of this, please feel free to send me an email (probably somewhere on [my GitHub profile](https://github.com/czlee/).)

> Note that the [Debatekeeper app itself](https://github.com/czlee/debatekeeper) is licensed under a different licence (GPL-3.0).

### How to submit a new format

First, write your XML file [according to these specifications](https://github.com/czlee/debatekeeper/wiki/Writing-your-own-custom-debate-format-file), and test it by importing it into your phone and running it through a few debates.

1. **Go to** the "[v1/formats](https://github.com/czlee/debatekeeper-formats/tree/main/v1/formats)" directory.
2. Click the **Add file** button in the top right of that page (not this one). Either upload your file, or create one then copy-paste your file's contents. Please double-check that you're in the **v1/formats** directory.
3. Propose the file, and then submit your **pull request**.

> This will automatically create a "fork", a copy of this repository under your control. A "pull request" is a proposed change.

It's helpful if you can provide a bit of information about where the league, circuit or tournaments where your format is used. The pull request template will ask you to add this information, and will remind you that you're agreeing to license your contribution under the MIT License.

### Conventions in this repository

Some conventions in this repository are stricter than in the app.

- **File names**:
  - should be in lower case, _e.g._ "bp.xml" not "~~BP.xml~~"
  - should use hyphens rather than underscores, _e.g._ "asd-juniors.xml" not "~~ASD_Juniors.xml~~"
  - It's preferable (but not essential) to keep file names reasonably short.
  - Abbreviations in file names (like "apda") are fine.
- **XML formatting**:
  - XML should be neatly indented, preferably using a tab width of 2.
  - Any trailing whitespace at the end of lines should be removed.
- **Cross-references**, _i.e._ the `ref` attribute of speech types and period types:
  - should be in lower case, and
  - can have hyphens, dots and numbers, but no other symbols or whitespace.
  - If you have a good reason to break this rule, I'll consider—feel free to explain in your pull request.
- **Human-readable names**, _e.g._ the style name and speech names:
  - should be in the grammatically appropriate case for that language
  - should prefer the technically "correct" name to the common colloquial name (if they differ)
- **Version numbers**:
  - should be 1 if it's a new format
  - should increase when a format is updated (increments preferred)
- **In [multilingual files](https://github.com/czlee/debatekeeper/wiki/Writing-your-own-custom-debate-format-file#multilingual-formats)**:
  - All languages must be declared in the `<languages>` element.
  - Every human-readable string must have a translation in all declared languages.
  - It's preferable for languages always to appear in the same order.
  - (While it's common for formats include English translations, it's not a requirement.)

There are some scripts that run automatically on all submissions to check for conformity with some of these conventions.

If you want to run the scripts locally to check your work before pushing, you can run `python scripts/validate_all.py` from the repository root directory.

### What happens when you submit

This repository has some scripts that run automatically on all pull requests. These scripts check that the debate style format files are well-formed and follow the [conventions above](#conventions-in-this-repository). The pull request will show whether the checks succeeded.

If you're new to GitHub, it might want me to "approve" the workflow before it runs.

_Note:_ Because this is the official repository, the scripts are stricter than the app. So the file might work on your device, but still fail the checks in this repository. If this happens, check the errors and see if you can fix them in your fork. If the errors are confusing to you (some of them are admittedly obscure), please don't hesitate to ask by commenting on your pull request.

### When will my format become available on Debatekeeper?

After I merge your pull request, your format will become available via Debatekeeper's downloads function after GitHub Pages regenerates the website. This normally takes just 1–2 minutes.

Users do _not_ need to update the app before they can access the new file.

Depending on how busy I am with life, it might take a while for me to attend to your pull request. I apologise in advance. Before this repository was introduced in 2021, some contributions sat around for years; I'm hoping this new system will reduce to that a few days. Indeed, the purpose of the above automatic scripts (and this online repository) is to make this a one-click process for me so that I can do it quickly.

Contributions of other code
---------------------------

Nothing of unusual significance here. All of the above also applies to new code—it's also licensed under the MIT License, and should be submitted in a pull request as usual. The main purpose of this page was to provide a guide for people who don't have an extensive coding background. 🙂

You can delete all the text in the pull request template if you're submitting other code. The pre-filled text in pull requests is mainly to help people who are submitting a new debate format (and so that they can't miss the part about the MIT License).
