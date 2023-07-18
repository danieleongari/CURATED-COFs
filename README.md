[![Build Status](https://github.com/danieleongari/CURATED-COFs/workflows/ci/badge.svg)](https://github.com/danieleongari/CURATED-COFs/actions)

# CURATED-COFs
Clean, Uniform and Refined with Automatic Tracking from Experimental Database (CURATED) COFs *from literature*.

This repository contains original structures from literature search, with git-tracked corrections. \
DFT-optimized frameworks with DDEC charges are available on [Materials Cloud](https://www.materialscloud.org/discover/curated-cofs). \
> NOTE: the crystal structures in this database may contain unnatural bond length and geometry, consistent with the CIF file reported in the original reference papers.
The DFT optimization should take care of these problems and correct for them (see optimized structures on Materials Cloud).
The CIF files in the present database are modified manually or programmatically only when the DFT optimization does not solve the problem and a trivial manual fix can be applied: in this case the `Modifications` are reported in `cof-frameworks.csv`. Don't hesitate [to report](https://forms.gle/gQpjcSEHjoJpqira8) any structure that is still problematic **after** the DFT optimization.

Files' structure:
* `cof-frameworks.csv` contains the list of COFs and the manual modifications
* `cof-discarded.csv` contains a list of COFs that have been discarded because of duplicate detection, unobserved AA/AB stacking variant, unobserved n-fold interpenetration, or other reasons reported in the document
* `cof-papers.csv` contains a list of the reference papers for the COFs in the database: for example, `p0701` is the reference of COFs `07010N3`, `07011N3`, `07012N3`, and `07013N3`
* `cifs/` contains all the crystallographic information files (CIFs) for the COFs listed in `cof-frameworks.csv` and `cof-discarded.csv`

The database builds on the work of [Tong et al.](https://doi.org/10.1021/acs.jpcc.8b04742), named [CoRE-COF-DT280-v2.0](https://github.com/core-cof/CoRE-COF-Database/tree/2c1419d1f3c0d6eccce4306728cfe151c6b2ee08).

### Structure labels
![Structure labels](images/figure1.gif)

### Cite as
* Original release: *D. Ongari, A. V. Yakutovich, L. Talirz and B. Smit, Building a consistent and reproducible database for adsorption evaluation in Covalent-Organic Frameworks, ACS Central Science 2019, 5, 10, 1663-1675* ([10.1021/acscentsci.9b00619](https://doi.org/10.1021/acscentsci.9b00619))

* Update: *D. Ongari, L. Talirz and B. Smit, Too Many Materials and Too Many Applications: An Experimental Problem Waiting for a Computational Solution, ACS Central Science 2020, 6, 11, 1890-1900* ([10.1021/acscentsci.0c00988](https://doi.org/10.1021/acscentsci.0c00988))

### Help us
Please report new COF structures or mistakes by using [this form](https://forms.gle/gQpjcSEHjoJpqira8). Thank you!

For bulk submissions, see [here](CONTRIBUTING.md).
