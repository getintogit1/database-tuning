# Tuning Principle

## Applied Tuning Principle
The tuning principle we applied follows the concept of **"Start-Up Costs Are High; Running Costs Are Low"**. Our goal was to optimize query execution by minimizing redundant parsing and optimization steps while improving overall efficiency.

## Improvements
- The tuned approach is based on the principle from the slides: **Start-Up Costs Are High; Running Costs Are Low**.
- We **parse and optimize the query only once** and cache the execution plan.
- The query can be executed multiple times **with different parameters** without repeating the parsing and optimization steps.
- We avoid committing after every statement, **instead committing once for both table loadings**.

## Portability & Implementation
### Key Changes in SQL:
We made specific improvements to enhance performance:
- **Commit Frequency:** Previously, each statement was committed separately. Now, we use **a single commit** after inserting all data into both tables.
- **Statement Parsing & Optimization:** Instead of parsing and optimizing every statement individually, we now **prepare the statement once** and reuse it with different parameters.
- **Batching:**  We implemented batch execution to further enhance performance.

## How to Test the Performance Improvement

### To see the results, clone the repository and execute the following scripts in order:

```sh
git clone https://github.com/getintogit1/database-tuning.git
cd database-tuning
python TableCreations.py
python TimeMeasurements.py
```sh
These scripts will demonstrate the performance improvements made through our tuning approach.
By applying these optimizations, we significantly reduce the overhead of repeated query parsing, improve execution speed, and optimize database interactions efficiently.
