# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

This repository uses the **Speckit framework** for feature development. The workflow follows:
1. `speckit-specify`: Create/update feature specification from natural language
2. `speckit-plan`: Generate implementation plan using plan template
3. `speckit-tasks`: Create dependency-ordered tasks.md
4. `speckit-implement`: Execute implementation plan

Key directories:
- `.specify/`: Contains workflow templates and extensions
  - `.specify/templates/`: Feature spec, plan, and tasks templates
  - `.specify/extensions/git/`: Git workflow automation
- `.claude/skills/`: Speckit command implementations

## Development Commands

### Feature Development
- Start new feature: `bash .specify/scripts/bash/create-new-feature.sh`
- Setup plan files: `bash .specify/scripts/bash/setup-plan.sh`
- Check prerequisites: `bash .specify/scripts/bash/check-prerequisites.sh`

### Git Automation
- Auto-commit changes: `bash .specify/extensions/git/scripts/bash/auto-commit.sh`
- Create feature branch: `speckit-git-feature`
- Validate branch naming: `speckit-git-validate`

### Speckit Skills
Available via `/` commands:
- `/speckit-specify` - Generate feature specification
- `/speckit-plan` - Create implementation plan
- `/speckit-tasks` - Generate task list
- `/speckit-implement` - Execute implementation
- `/speckit-analyze` - Verify consistency across spec, plan, tasks

## Workflow Notes
1. Always follow the Speckit workflow (specify → plan → tasks → implement)
2. Feature branches should follow naming conventions enforced by `speckit-git-validate`
3. Auto-commit scripts run after Speckit commands to maintain clean history