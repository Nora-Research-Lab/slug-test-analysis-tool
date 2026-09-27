![NORA logo](https://i.ibb.co/0VJCC9Gf/IMG-20260114-WA0008.jpg)
 
# Slug Test Analysis Tool
 
*For hydrogeologists and groundwater engineers: enter water-level displacement and time-recovery measurements to instantly compute hydraulic conductivity using the Hvorslev and Bouwer-Rice methods.*
 
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
 

## Overview
 
**Industry:** Hydrogeology / Groundwater
 
**Inputs:** (1) Well radius (r) in meters (or centimeters, with unit selector). (2) Screen length (L) in meters. (3) Initial displacement (H0) in meters. (4) A data table or CSV upload with two columns: time (seconds) and head ratio H(t)/H0 (dimensionless, value between 0 and 1). The user may paste or upload. 

**Core logic:** 
- Hvorslev method: Convert head ratios to natural logarithm ln(H(t)/H0). Perform linear regression of ln(H/H0) vs. time. The slope gives -1/T0, where T0 is the basic time lag. Then hydraulic conductivity K = (r^2 * ln(L/r)) / (2 * L * T0). 
- Bouwer-Rice method (for partially penetrating wells): Use the same T0 from regression. Effective radius Re is computed empirically as function of r, L, and aquifer thickness (user may provide aquifer thickness or assume large). Then K = (r^2 * ln(Re/r)) / (2 * L * T0). 
- Both methods return K in m/s. 

**UI layout:** 
- Top: title, brief instructions. 
- Left panel: input fields for r, L, H0, aquifer thickness (optional), and a data input area (text area for paste or file upload widget). 
- Right panel: output display showing K_Hvorslev (m/s), K_BouwerRice (m/s), and a matplotlib plot of ln(H/H0) vs. time with the regression line overlaid. Below the plot, a classification table mapping K range to material type (gravel, sand, silt, clay). 
- A 'Calculate' button triggers the computation. 
- Option to download a summary report as a text file. 

**AI/ML component:** None. Pure domain calculations.
 
## Run it
 
```bash
docker build -t slug-test-analysis-tool .
docker run -p 7860:7860 slug-test-analysis-tool
```
 
Then open http://localhost:7860 in your browser.
 
## About
 
This tool was generated and published automatically by the **NORA Earth Intelligence**
tool factory, an autonomous pipeline maintained by **NORA Research Lab** that turns
one idea per run into a small, working geoscience tool — end to end, with an
LLM writing and Docker-testing the code, and another model generating the
banner above.
 
- Platform: [https://noraearth.xyz](https://noraearth.xyz)
- Parent lab: [https://noraresearchlab.site](https://noraresearchlab.site)
 
Built 2026-09-27.
 
---
 
### Maintainer
 
**NORA Research Lab**
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
