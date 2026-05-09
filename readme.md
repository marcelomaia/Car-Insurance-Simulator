# Car Insurance Premium Simulator

## Description

As a product owner, I want a backend service that calculates car insurance premiums based on a car's age, value, deductible percentage and a broker's fee. This ensures users receive an accurate and configurable insurance premium calculation. The service must be implemented using **FastAPI**, containerized with **Docker**, and designed following **Domain-Driven Design (DDD), S.O.L.I.D., and Clean Architecture** principles. The domain model should clearly distinguish between **value objects, entities, aggregates, services, and events**.

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