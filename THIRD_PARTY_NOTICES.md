# Third-party notices

Files under `synced/` are generated from the upstream projects recorded in
`sources.yaml`. Local generation adds the `jl-` namespace, rewrites declared
JL dependency references, and adds Codex UI metadata. Upstream copyrights and
licenses remain with their respective owners.

| Project | Copyright | License copy |
| --- | --- | --- |
| [obra/superpowers](https://github.com/obra/superpowers) | Copyright © 2025 Jesse Vincent | [`licenses/superpowers-MIT.txt`](licenses/superpowers-MIT.txt) |
| [github/awesome-copilot](https://github.com/github/awesome-copilot) | Copyright GitHub, Inc. | [`licenses/awesome-copilot-MIT.txt`](licenses/awesome-copilot-MIT.txt) |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | Copyright © 2026 Affaan Mustafa | [`licenses/ecc-MIT.txt`](licenses/ecc-MIT.txt) |
| [ccheney/robust-skills](https://github.com/ccheney/robust-skills) | Copyright © 2026 robust-skills contributors | [`licenses/robust-skills-MIT.txt`](licenses/robust-skills-MIT.txt) |
| [blader/humanizer](https://github.com/blader/humanizer) | Copyright © 2025 Siqi Chen | [`licenses/humanizer-MIT.txt`](licenses/humanizer-MIT.txt) |
| [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | Copyright © 2026 Julius Brussee | [Apache-2.0](licenses/caveman-Apache-2.0.txt), [NOTICE](licenses/caveman-NOTICE.txt), [retained MIT notice](licenses/caveman-MIT.txt) |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | Copyright © 2026 DietrichGebert | [`licenses/ponytail-MIT.txt`](licenses/ponytail-MIT.txt) |
| [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) | Copyright © 2026 Ayoub Ghriss | [`licenses/i-have-adhd-MIT.txt`](licenses/i-have-adhd-MIT.txt) |
| [mattpocock/skills](https://github.com/mattpocock/skills) | Copyright © 2026 Matt Pocock | [`licenses/mattpocock-skills-MIT.txt`](licenses/mattpocock-skills-MIT.txt) |

The Caveman, Ultracave, and Megacave skill copies use upstream's Apache-2.0
release. The upstream `LICENSE`, `NOTICE`, and retained `LICENSE-MIT` are copied
under the names linked above; the MIT notice preserves attribution for earlier
contributions. This repository imports the three voice skills, without the
upstream CLI, proxy, hooks, or runtime. Their declared namespace and Codex
frontmatter transformations remain recorded in `sources.yaml` and the sync script.
