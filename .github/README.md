<div align="center">

<img width="120" src="https://raw.githubusercontent.com/czlee/debatekeeper/master/misc/icon/overall.svg" />

Official Debatekeeper debate formats repository
===============================================

</div>

This repository contains the format files that are available for download within Debatekeeper, starting in version 1.3 (October 2021).

My motivation for moving this repository online is to make it much faster to make new formats available. Formats used to be shipped with the app, so new formats needed to wait for an app update. As I write this in 2021, there hasn't a Debatekeeper update since 2016, and there are 6 pending pull requests with new formats. One would be forgiven for thinking they'll never happen! I don't envisage doing any further updates to the Debatekeeper app in the future, so hopefully this online repository will make it simpler to make new and updated format files available.

The repository for the Debatekeeper app itself is at https://github.com/czlee/debatekeeper.

Submitting a new format file
----------------------------

First, write your XML file [according to these specifications](https://github.com/czlee/debatekeeper/wiki/Writing-your-own-custom-debate-format-file), and test it by importing it into your phone and running it through a few debates.

Then, to submit your file for inclusion in this repository:
1. **Go to** the "[v1/formats](https://github.com/czlee/debatekeeper-formats/tree/main/v1/formats)" directory.
2. Click the **Add file** button in the top right of that page (not this one). Either upload your file, or create one then copy-paste your file's contents. Please double-check that you're in the **v1/formats** directory.
3. Propose the file, and then submit your **pull request**.

(If you're familiar with GitHub forks, you can also fork and add as usual. Just be sure it's in the v1/formats directory.)

⚠️ **Note on licensing:** Code in this repository is [licensed](https://github.com/czlee/debatekeeper-formats/tree/main/LICENCE.md) under the [MIT License](https://choosealicense.com/licenses/mit/). Submitters of new contributions are taken to agree that their code may be licensed under the MIT License. [Learn more in our information for contributors](https://github.com/czlee/debatekeeper-formats/tree/main/.github/CONTRIBUTING.md).

➡️ _More detailed information, as well as guidance on conventions, is [available on this page](https://github.com/czlee/debatekeeper-formats/tree/main/.github/CONTRIBUTING.md)._

### Note on formats.json
A GitHub Action is configured to automatically update the formats.json file ([thanks to Frank Richter](https://github.com/czlee/debatekeeper-formats/pull/3)!), so you shouldn't need to. However, you can run the `update_list.py` script locally if you like.

### Note on some American styles
Debatekeeper can't properly support the public forum, Lincoln-Douglas or policy debate styles. This is because the app doesn't support preparation time between speeches distributed at teams' election. A discussion of this is in [issue #6 in the Debatekeeper app repository](https://github.com/czlee/debatekeeper/issues/6).

How this is hosted
------------------

It's just a GitHub Pages site that hosts the files in this repository directly, hosted at the domain name formats.debatekeeper.czlee.nz. Don't go there—there's nothing there for humans to see! Okay, if you really want: https://formats.debatekeeper.czlee.nz/v1/formats.json. But it's literally just [the formats.json in this repository](https://github.com/czlee/debatekeeper-formats/blob/main/v1/formats.json).

Repository format
-----------------

If you'd like to start a new repository (_e.g._, because I've stopped updating this one), you just need to provide a JSON file of the same format as [formats.json](https://github.com/czlee/debatekeeper-formats/blob/main/v1/formats.json). The JSON should provide URLs to the format files available for download. Note, however, that your format files must be hosted at the same domain name as the formats file—that is, you can't link to files on other sites. (Debatekeeper checks this, and refuses to request files that aren't on the same host as the JSON file listing the available formats. There's no requirement for it to be in a "formats" directory, though.)
