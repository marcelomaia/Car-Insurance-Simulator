# Car Insurance Premium Simulator

[![Coverage](https://sonarqube.mmaia.site/api/project_badges/measure?project=marcelomaia_Car-Insurance-Simulator_120e9ae5-a590-42e0-bf0a-75d1371a173c&metric=coverage&token=sqb_43a5c44ae8f3dcf79401220a6ed608b774f6cb8d)](https://sonarqube.mmaia.site/dashboard?id=marcelomaia_Car-Insurance-Simulator_120e9ae5-a590-42e0-bf0a-75d1371a173c)
[![Duplicated Lines (%)](https://sonarqube.mmaia.site/api/project_badges/measure?project=marcelomaia_Car-Insurance-Simulator_120e9ae5-a590-42e0-bf0a-75d1371a173c&metric=duplicated_lines_density&token=sqb_43a5c44ae8f3dcf79401220a6ed608b774f6cb8d)](https://sonarqube.mmaia.site/dashboard?id=marcelomaia_Car-Insurance-Simulator_120e9ae5-a590-42e0-bf0a-75d1371a173c)
[![Quality Gate Status](https://sonarqube.mmaia.site/api/project_badges/measure?project=marcelomaia_Car-Insurance-Simulator_120e9ae5-a590-42e0-bf0a-75d1371a173c&metric=alert_status&token=sqb_43a5c44ae8f3dcf79401220a6ed608b774f6cb8d)](https://sonarqube.mmaia.site/dashboard?id=marcelomaia_Car-Insurance-Simulator_120e9ae5-a590-42e0-bf0a-75d1371a173c)
[![Security Hotspots](https://sonarqube.mmaia.site/api/project_badges/measure?project=marcelomaia_Car-Insurance-Simulator_120e9ae5-a590-42e0-bf0a-75d1371a173c&metric=security_hotspots&token=sqb_43a5c44ae8f3dcf79401220a6ed608b774f6cb8d)](https://sonarqube.mmaia.site/dashboard?id=marcelomaia_Car-Insurance-Simulator_120e9ae5-a590-42e0-bf0a-75d1371a173c)
[![Reliability Issues](https://sonarqube.mmaia.site/api/project_badges/measure?project=marcelomaia_Car-Insurance-Simulator_120e9ae5-a590-42e0-bf0a-75d1371a173c&metric=software_quality_reliability_issues&token=sqb_43a5c44ae8f3dcf79401220a6ed608b774f6cb8d)](https://sonarqube.mmaia.site/dashboard?id=marcelomaia_Car-Insurance-Simulator_120e9ae5-a590-42e0-bf0a-75d1371a173c)
[![Maintainability Issues](https://sonarqube.mmaia.site/api/project_badges/measure?project=marcelomaia_Car-Insurance-Simulator_120e9ae5-a590-42e0-bf0a-75d1371a173c&metric=software_quality_maintainability_issues&token=sqb_43a5c44ae8f3dcf79401220a6ed608b774f6cb8d)](https://sonarqube.mmaia.site/dashboard?id=marcelomaia_Car-Insurance-Simulator_120e9ae5-a590-42e0-bf0a-75d1371a173c)
[![Security Issues](https://sonarqube.mmaia.site/api/project_badges/measure?project=marcelomaia_Car-Insurance-Simulator_120e9ae5-a590-42e0-bf0a-75d1371a173c&metric=software_quality_security_issues&token=sqb_43a5c44ae8f3dcf79401220a6ed608b774f6cb8d)](https://sonarqube.mmaia.site/dashboard?id=marcelomaia_Car-Insurance-Simulator_120e9ae5-a590-42e0-bf0a-75d1371a173c)
[![Maintainability Rating](https://sonarqube.mmaia.site/api/project_badges/measure?project=marcelomaia_Car-Insurance-Simulator_120e9ae5-a590-42e0-bf0a-75d1371a173c&metric=software_quality_maintainability_rating&token=sqb_43a5c44ae8f3dcf79401220a6ed608b774f6cb8d)](https://sonarqube.mmaia.site/dashboard?id=marcelomaia_Car-Insurance-Simulator_120e9ae5-a590-42e0-bf0a-75d1371a173c)
[![Reliability Rating](https://sonarqube.mmaia.site/api/project_badges/measure?project=marcelomaia_Car-Insurance-Simulator_120e9ae5-a590-42e0-bf0a-75d1371a173c&metric=software_quality_reliability_rating&token=sqb_43a5c44ae8f3dcf79401220a6ed608b774f6cb8d)](https://sonarqube.mmaia.site/dashboard?id=marcelomaia_Car-Insurance-Simulator_120e9ae5-a590-42e0-bf0a-75d1371a173c)
[![Security Rating](https://sonarqube.mmaia.site/api/project_badges/measure?project=marcelomaia_Car-Insurance-Simulator_120e9ae5-a590-42e0-bf0a-75d1371a173c&metric=software_quality_security_rating&token=sqb_43a5c44ae8f3dcf79401220a6ed608b774f6cb8d)](https://sonarqube.mmaia.site/dashboard?id=marcelomaia_Car-Insurance-Simulator_120e9ae5-a590-42e0-bf0a-75d1371a173c)
[![Technical Debt](https://sonarqube.mmaia.site/api/project_badges/measure?project=marcelomaia_Car-Insurance-Simulator_120e9ae5-a590-42e0-bf0a-75d1371a173c&metric=software_quality_maintainability_remediation_effort&token=sqb_43a5c44ae8f3dcf79401220a6ed608b774f6cb8d)](https://sonarqube.mmaia.site/dashboard?id=marcelomaia_Car-Insurance-Simulator_120e9ae5-a590-42e0-bf0a-75d1371a173c)

## Description

As a product owner, I want a backend service that calculates car insurance premiums based on a car's age, value, deductible percentage and a broker's fee. This ensures users receive an accurate and configurable insurance premium calculation. The service must be implemented using **FastAPI**, containerized with **Docker**, and designed following **Domain-Driven Design (DDD), S.O.L.I.D., and Clean Architecture** principles. The domain model should clearly distinguish between **value objects, entities, aggregates, services, and events**.

Phased roadmap and progress checklist: [execution_plan.md](execution_plan.md).

---

## Core Requirements and Calculation Logic

Everything must be **parameterized** to allow future modifications in the configuration **without requiring code changes**. These values should be **configurable via environment variables or a configuration file**. If using a code generation tool, ensure that: All functions and parameters are written in alphabetical order.

### 1. **Dynamic Rate Calculation**

- For every year since the car was produced, **add 0.5% to the rate**.
- For every **$10,000 of the car’s value, add another 0.5%** to the rate.
- **Example:** A 10-year-old car valued at **$100,000** would have a rate of:
  - **5%** (from age) + **5%** (from value) = **10%** total rate.

### 2. **Premium Calculation**

- **Base Premium** = `car value * applied rate`
- **Deductible Discount** = `base premium * deductible percentage`
- **Final Premium** = `Base Premium - Deductible Discount + Broker’s Fee`

### 3. **Policy Limit Calculation**

- **Base Policy Limit** = `car value * coverage percentage (default 100%)`
- **Deductible Value** = `base policy limit * deductible percentage`
- **Final Policy Limit** = `base policy limit - deductible value`

### 4. [Optional Bonus Task] GIS Adjustment

If a **registration location** is provided, integrate with a **Geographic Information System (GIS)** to adjust the derived rate based on geographic risk factors.

- Suggested approach: Apply an additional rate variation between **-2% and +2%** depending on the risk associated with the location.

### 5. **MY COMMENT: Valid quote semantics (aligned with §§2–4)**

These rules refine the formulas above so outputs match real insurance semantics (premium payable by the customer, limits that stay coherent).

| Rule | Meaning |
|------|--------|
| **Deductible scale** | `deductible_percentage` is a **fraction in `[0, 1]`** everywhere it appears (premium §2 and policy limit §3). Example: **`0.10` = 10%**, not `10`. |
| **GIS combines additively** | First compute the **intrinsic rate** from §1 (age + value). If GIS applies (§4), add an adjustment **between −2% and +2%** (i.e. **−0.02 … +0.02** as a decimal rate). **`applied_rate = intrinsic_rate + gis_variation`**. |
| **When arithmetic produces nonsense** | With GIS at **−2%**, a **very small intrinsic rate** (e.g. new car, low value) can make **`applied_rate` negative** in pure math. **Premium** is **`car value × applied_rate`** (§2), so a negative rate would imply the insurer “pays” the customer. **Such combinations are not valid quotes:** the service **rejects** them instead of returning negative premiums or limits broken by impossible deductibles. |
| **Invalid deductible** | Any **`deductible_percentage` outside `[0, 1]`** is rejected (same fractional scale as in the input contract below). |

Successful API responses expose **`applied_rate`**, **`calculated_premium`**, **`policy_limit`**, and **`deductible_value`** only when these constraints pass.

## Interface Contracts

### **Input Interface**

- **Car Details:**
  - `make` _(string)_, e.g., `"Toyota"`
  - `model` _(string)_, e.g., `"Corolla"`
  - `year` _(integer)_, e.g., `2012`
  - `value` _(float)_, e.g., `100000.0`
- `deductible_percentage` _(float)_, e.g., `0.10` for **10%**
- `broker_fee` _(float)_, e.g., `50.0`
- `registration_location` _(optional, Address)_

### **Output Interface**

- **Car Details:** _(Echoed from input)_
- `applied_rate` _(Final calculated rate after adjustments)_
- `policy_limit` _(Final policy limit after deductible application)_
- `calculated_premium` _(Final premium after deductible and broker fee adjustments)_
- `deductible_value` _(Monetary value calculated from the original policy limit and deductible percentage)_