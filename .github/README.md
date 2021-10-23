Official Debatekeeper debate formats repository
===============================================

This repository contains the format files that will be available for download within Debatekeeper starting in version 1.3.

My motivation for moving this repository online is to make it much faster to make new formats available. Formats used to be shipped with the app, so new formats needed to wait for an app update. As I write this in 2021, there hasn't a Debatekeeper update since 2016, and there are 6 pending pull requests with new formats. One would be forgiven for thinking they'll never happen! I don't envisage updating Debatekeeper any more often in the future, so hopefully this online repository will make it simpler to make new and updated format files available.

The repository for the Debatekeeper app itself is at https://github.com/czlee/debatekeeper.

Submitting a new format file
----------------------------

First, write your XML file [according to these specifications](https://github.com/czlee/debatekeeper/wiki/Writing-your-own-custom-debate-format-file), and test it by importing it into your phone and running it through a few debates.

Then, to submit your file for inclusion in this repository:
1. **Fork** this repository (click the button in the top-right of this page).
2. **Add** your file to the "[v1/formats](https://github.com/czlee/debatekeeper-formats/tree/main/v1/formats)" directory.
3. Submit a **pull request** from your fork to this repository.

⚠️ **Note on licensing:** Code in this repository is [licensed](https://github.com/czlee/debatekeeper-formats/tree/main/LICENCE.md) under the [MIT License](https://choosealicense.com/licenses/mit/). Submitters of new contributions are taken to agree that their code may be licensed under the MIT License. [Learn more in our information for contributors](https://github.com/czlee/debatekeeper-formats/tree/main/.github/CONTRIBUTING.md).

➡️ _More detailed information is [available on this page](https://github.com/czlee/debatekeeper-formats/tree/main/.github/CONTRIBUTING.md)._

### Note on formats.json
A GitHub Action is configured to automatically update the formats.json file ([thanks to Frank Richter](https://github.com/czlee/debatekeeper-formats/pull/3)!), so you shouldn't need to. However, you can run the `update_list.py` script locally if you like.

How this is hosted
------------------

It's just a GitHub Pages site that hosts the files in this repository directly, hosted at the domain name formats.debatekeeper.czlee.nz. Don't go there—there's nothing there for humans to see! Okay, if you really want: https://formats.debatekeeper.czlee.nz/v1/formats.json. But it's literally just [the formats.json in this repository](https://github.com/czlee/debatekeeper-formats/blob/main/v1/formats.json).

Repository format
-----------------

If you'd like to start a new repository (_e.g._, because I've stopped updating this one), you just need to provide a JSON file of the same format as [formats.json](https://github.com/czlee/debatekeeper-formats/blob/main/v1/formats.json). The JSON should provide URLs to the format files available for download. Note, however, that your format files must be hosted at the same domain name as the formats file—that is, you can't link to files on other sites. (Debatekeeper checks this, and refuses to request files that aren't on the same host as the JSON file listing the available formats. There's no requirement for it to be in a "formats" directory, though.)
