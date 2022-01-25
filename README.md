# USDA Application Rationalization Challenge

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Expected Input](#expected-input)
  * [SCCM](#sccm)
  * [Tanium](#tanium)
- [Execution](#execution)
- [Reports for `agency_ids.py`](#reports-for-agency_idspy)
  * [Report 1: Matching classification report (`matching_raw.xlsx`)](#report-1-matching-classification-report-matching_rawxlsx)
  * [Report 2: Mismatch classification report (`mismatch_raw.xlsx`)](#report-2-mismatch-classification-report-mismatch_rawxlsx)
  * [Report 3: SCCM-grouped mismatching classification report(`mismatching_sccm_grouped.xlsx`)](#report-3-sccm-grouped-mismatching-classification-report-mismatching_sccm_groupedxlsx)
  * [Report 4: Tanium-grouped mismatching classification report (`mismatching_tanium_grouped.xlsx`)](#report-4-tanium-grouped-mismatching-classification-report-mismatching_tanium_groupedxlsx)
  * [Report 5: SCCM-only workstations report (`sccm_only.xlsx`)](#report-5-sccm-only-workstations-report-sccm_onlyxlsx)
  * [Report 6: Tanium-only workstations report (`tanium_only.xlsx`)](#report-6-tanium-only-workstations-report-tanium_onlyxlsx)
  * [Report 7: Workstation coverage statistics (`coverage_statistics.xlsx`)](#report-7-workstation-coverage-statistics-coverage_statisticsxlsx)
- [Reports for `usages.py`](#reports-for-usagespy)
  * [Usage reports as bar graphs and pie charts](#usage-reports-as-bar-graphs-and-pie-charts)
  * [Usage reports as Excel datasets](#usage-reports-as-excel-datasets)

## Overview

The USDA CEC Team partnered with Harvard Computer Society's Tech for Social Good (T4SG) to explore application installation data gathered using SCCM and Tanium. The algorithms that T4SG developed are made available in the Python scripts `agency_ids.py` and `usages.py`. 

`agency_ids.py` generates reports analyzing the Agency IDs that SCCM and Tanium report for each workstation. The algorithm details situations where Agency ID classifications match and differ, as well as coverage of each tool for individual agencies.

`usages.py` generates reports and visualizations on application usage levels within each agency and mission area. These reports are based on the data reported by Tanium.

## Installation

Install [Python 3.9](https://www.python.org/downloads/) (or latest version).

Use `pip` (built-in Python package management system) to install the following libraries:

- Matplotlib: run `pip install matplotlib`, see https://matplotlib.org/stable/users/installing/index.html.
- Numpy: run `pip install numpy`, see https://numpy.org/install/.
- OpenPyXL: run `pip install openpyxl`, see https://openpyxl.readthedocs.io/en/stable/#installation.
- Pandas: run `pip install pandas`, see https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html.

## Expected Input

### SCCM

See below the expected structure of the SCCM dataset, which should be placed in the project directory, as well as where in the Python scripts these expected names can be modified.

| Description | Expected name | `agency_ids.py` |
|---|---|---|
| SCCM dataset Excel filename | `sccm.xlsx` | [line 28](agency_ids.py#L28) |
| Workstation identifier column* | `Encrypted Workstation Name` | [line 7](agency_ids.py#L7) |
| SCCM Agency ID column | `Agency` | [line 13](agency_ids.py#L13) |

\* The workstation identifier column name must be the same for both the SCCM and Tanium datasets.

All Agency IDs are expected to have the following schema: `XXX`, where `XXX` is the alphabetical agency identification of any length.

### Tanium

See below the expected structure of the Tanium dataset, which should be placed in the project directory, as well as where in the Python scripts these expected names can be modified.

| Description | Expected name | `agency_ids.py` | `usages.py` |
|---|---|---|---|
| Tanium dataset Excel filename | `tanium.xlsx` | [line 29](agency_ids.py#L29) | [line 24](usages.py#L24) |
| Workstation identifier column* | `Encrypted Workstation Name` | [line 7](agency_ids.py#L7) |  |
| Tanium application name column | `Name` |  | [line 7](usages.py#L7) |
| Tanium operating system column | `Operating System` | [line 9](agency_ids.py#L9) |  |
| Tanium usage level column | `Usage` | [line 11](agency_ids.py#L11) | [line 9](usages.py#L9) |
| Tanium Agency ID columns | <ul><li>`Asset - Custom Tags.2.1`</li><li>`Asset - Custom Tags.2.2.1`</li><li>`Asset - Custom Tags.2.2.2.1`</li><li>`Asset - Custom Tags.2.2.2.2.1`</li><li>`Asset - Custom Tags.2.2.2.2.2.1`</li><li>`Asset - Custom Tags.2.2.2.2.2.2.1`</li><li>`Asset - Custom Tags.2.2.2.2.2.2.2.1`</li><li>`Asset - Custom Tags.2.2.2.2.2.2.2.2.2.1`</li></ul> | [lines 15-24](agency_ids.py#L15-L24) | [lines 11-20](usages.py#L11-L20) |

\* The workstation identifier column name must be the same for both the SCCM and Tanium datasets.

All Tanium Agency IDs are expected to have the following schema: `AgencyID-XXX`, where `XXX` is the alphabetical agency identification of any length. `agency_ids.py` will ignore any tag that does not have the prefix `AgencyID-`. `usages.py` will create datasets and visualizations for all tags, including those not prefixed by `AgencyID-`.

## Execution
Once the required packages are installed, go to the Terminal and navigate to the project directory where both scripts are held.

To generate reports 1 - 7, run `python agency_ids.py` in the Terminal.

To generate Tanium usage reports and figures by Agency IDs and Mission Areas, run `python usages.py` into the Terminal.

The executed script will run, output its progress, and generate its respective reports. Note that importing and exporting Excel files are resource intensive processes. If an algorithm appears to not progress, it may just be that an Excel file is being read or written.

## Reports for `agency_ids.py`
The report files generated by this script are stored in the `data/` folder of the project directory by default. To change this behavior, update both the folder creation in [line 13](agency_ids.py#L33) of `agency_ids.py` as well as the specific output filepath of each report.

For all reports, `Tanium Agency IDs` are all Tanium reported Agency IDs for a workstation (filtered for only tags with the `AgencyID-` prefix) concatenated in the format `XXX-YYY-...`.

### Report 1: Matching classification report (`matching_raw.xlsx`)
This report compiles encrypted workstations present in both SCCM and Tanium datasets where all Agency ID tags match between datasets.

The schema of this file is as follows:
- `Encrypted Workstation Name`
- `Operating System`
- `SCCM Agency ID`
- `Tanium Agency IDs`

The script will output the resulting Excel file to `data/matching_raw.xlsx`.

### Report 2: Mismatch classification report (`mismatch_raw.xlsx`)
This report compiles encrypted workstations present in both SCCM and Tanium datasets that have at least one non-matching Agency ID tag.

The schema of this file is as follows:
- `Encrypted Workstation Name`
- `Operating System`
- `SCCM Agency ID`
- `Tanium Agency IDs`

The script will output the resulting Excel file to `data/mismatch_raw.xlsx`.

### Report 3: SCCM-grouped mismatching classification report (`mismatching_sccm_grouped.xlsx`)
This report groups encrypted workstations present in both SCCM and Tanium datasets that have at least one non-matching Agency ID by SCCM Agency ID. It reveals the most common mismatched Tanium workstation classifications for each particular SCCM classificiation.

The schema of this file is as follows:
- `SCCM Agency ID`
- `Tanium Agency IDs`
- `Count`

The script will output the resulting Excel file to `data/mismatching_sccm_grouped.xlsx`.

### Report 4: Tanium-grouped mismatching classification report (`mismatching_tanium_grouped.xlsx`)
This report groups Encrypted Workstations present in both SCCM and Tanium datasets that have at least one non-matching classification by Tanium Agency IDs. It reveals the most common mismatched SCCM workstation classifications for each particular Tanium classification.

The schema of this file is as follows:
- `Tanium Agency IDs`
- `SCCM Agency ID`
- `Count`

The script will output the resulting Excel file to `data/mismatching_tanium_grouped.xlsx`.

### Report 5: SCCM-only workstations report (`sccm_only.xlsx`)
This report generates the encrypted workstations and Agency IDs of workstations that only appear in the SCCM dataset and not the Tanium dataset.

The schema of this file is as follows:
- `Encrypted Workstation Name`
- `Agency`

The script will output the resulting Excel file to `data/sccm_only.xlsx`.

### Report 6: Tanium-only workstations report (`tanium_only.xlsx`)
This report generates the encrypted workstation name, operating system, and Agency IDs of workstations that only appear in the Tanium dataset and not the SCCM dataset.

The schema of this file is as follows:
- `Encrypted Workstation Name`
- `Operating System`
- `Tanium Agency IDs`

The script will output the resulting Excel file to `data/tanium_only.xlsx`.

### Report 7: Workstation coverage statistics (`coverage_statistics.xlsx`)
This report gives an overview of the number of workstations within each Agency ID that are included in only the SCCM dataset, only the Tanium dataset, or are in both datasets. It reveals if datasets are underreporting any given Agency ID, as well as which Agency IDs are consistently covered by one tool and not the other.

The schema of the output file is as follows: 
- `Agency ID`
- `Total Workstations`
- `SCCM Workstations`
- `SCCM Workstations Proportion`
- `Tanium Workstations`
- `Tanium Workstations Proportion`
- `Shared Workstations`
- `Shared Workstations Proportion`

The script will output the resulting Excel file to `data/coverage_statistics.xlsx`.

## Reports for `usages.py`

`usages.py` generates Excel files stored in the `usage_data/` folder as well as bar and pie graphs stored in the `figures/` folder of the project directory. These destinations can be changed to a directory of choice by updating the folder creations in [lines 49 and 50](usages.py#L49-L50) and respective output filepaths in [lines 106](usages.py#L106), [115](usages.py#L115) and [120](usages.py#L120) of `usages.py`.


### Usage reports as bar graphs and pie charts
This report generates a pair of PNGs for every Mission Area and Agency ID in the Tanium dataset. One PNG features application usage data as bar graphs. The other illustrates the same data as pie charts. Each PNG pictures a bar graph or pie chart for each software used by the Agency ID or Mission Area at hand. Usage level is aggregated by color.

The legend of each visualization is as follows: 
- `Usage not detected` (red)
- `Limited` (orange)
- `Normal` (yellow)
- `High` (green)

The script will output the resulting visualizations to `figures/' `+` tag `+`'_bar.png` and `figures/' `+` tag `+`'_pie.png`.

### Usage reports as Excel datasets
These reports are generated for each Agency ID and Mission Area tag. Each report lists all the softwares used by the Mission Area or Agency ID, as reported by Tanium, alongside the software's usage frequency (`Usage not determined`, `Limited`, `Normal`, and `High`).

The schema of the output file is as follows: 
- `Name`
- `Usage not detected`
- `Limited`
- `Normal`
- `High`

The script will output the resulting Excel file to `usage_data/' `+` tag `+`'_usage.xlsx`.