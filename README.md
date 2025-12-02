# Digital Asset Operational Readiness Benchmark
**Candidate Project for The Value Exchange**

**Author:** Omar Saleh

## Overview
This project simulates the end-to-end data workflow required for institutional benchmarking and market analysis. It demonstrates the ability to ingest raw, unstructured survey data, clean it using Python, and derive actionable industry benchmarks regarding Digital Asset adoption.
## The Approach
Instead of manual Excel processing, this project uses a Python pipeline to ensure reproducibility and scalability for large datasets.

### 1. Data Simulation
* **Dataset:** Simulated responses from 150 Financial Institutions (Asset Managers, Custodians, Brokers).
* **Variables:** Region, AUM, Adoption Stage, and Operational Barriers.
* **Challenge:** The raw data included inconsistent formatting (e.g., "$10B" vs "500M") to mimic real-world survey cleanup needs.

### 2. Methodology
* **Cleaning:** Automated normalization of AUM (Assets Under Management) to allow for peer-grouping by size.
* **Analysis:** Grouped data by Firm Type and Region to identify disparate trends.
* **Visualization:** Created stacked bar charts to highlight the "Legacy Tech" bottleneck.

### 3. Key Findings (Mock)
* **Legacy Technology** remains the single largest barrier to adoption for Custodian Banks, whereas **Regulatory Uncertainty** is the primary concern for Hedge Funds.
* **APAC respondents** are 20% more likely to be in the "Live Production" phase compared to North American peers.
* **Size Matters:** Large institutions (>$100B AUM) are significantly more likely to be in the "POC Phase" but slower to reach production than mid-tier firms.

## Technical Stack
* **Python (Pandas):** For data cleaning and aggregation.
* **Matplotlib/Seaborn:** For generating client-ready visuals.
* **Data Structure:** Structured to align with typical VX Benchmarking reports.
