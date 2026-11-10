# SoftPLC Attack Paths

A collection of practical security investigations exploring attack paths against Software Programmable Logic Controllers (SoftPLCs).

This repository documents how weaknesses in deployment architectures, management interfaces, host environments, and runtime components can expose software-based industrial control systems to compromise.

Each attack path focuses on a specific security scenario. Investigations combine technical analysis, controlled laboratory experiments, evidence collection, and reproducible proof-of-concept demonstrations.

## Attack Paths

| ID | Attack Path | Status |
|---|---|---|
| AP-01 | Unauthorized Control Logic Modification | ✅ Complete |
| AP-02 | TBD | ⚪ Planned |
| AP-03 | TBD | ⚪ Planned |

*Status reflects the progress of each investigation. New attack paths will be added as the research develops.*

## Repository Structure

Each attack path has its own directory containing the relevant research materials.

| Directory | Contents |
|---|---|
| `notes/` | Technical findings, investigation notes, and reproduction guides |
| `screenshots/` | Visual evidence captured during experiments |
| `scripts/` | Test programs, automation scripts, and proof-of-concept code |

## Research Approach

Investigations are conducted in isolated laboratory environments using software-defined industrial control systems.

Depending on the attack path, research may include:

- Examining deployment architectures and security boundaries.
- Mapping exposed services and management interfaces.
- Reproducing potential attack scenarios.
- Developing small proof-of-concept programs and automation.
- Verifying results through observable runtime behavior and protocol interactions.
- Documenting evidence, limitations, and reproduction steps.

Findings distinguish between demonstrated behavior, environmental assumptions, and theoretical attack scenarios.

## Disclaimer

**This repository is intended exclusively for educational purposes, defensive security research, and authorized laboratory testing.**

All experiments should be conducted in isolated environments or against systems for which explicit authorization has been obtained.

The proof-of-concept scripts and techniques documented here may modify control logic, restart runtime processes, interrupt services, or otherwise affect system behavior. 

Do not execute these experiments against production industrial control systems, operational technology networks, or equipment controlling physical processes.

The author assumes no responsibility for damage, disruption, unauthorized access, or misuse resulting from the application of the material provided in this repository. 

By using this material, you acknowledge responsibility for ensuring that your activities are lawful and authorized.