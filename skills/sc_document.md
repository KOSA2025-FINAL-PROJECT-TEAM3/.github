---
name: sc:document
description: Generate focused documentation for components, functions, APIs, and features.
category: utility
complexity: basic
mcp_servers: []
personas: []
---

# Skill: sc:document

## Purpose
Generate focused documentation for a specific component, function, API, or feature.

## Inputs
- target: path, module, or component identifier
- type: inline | external | api | guide
- style: brief | detailed

## Outputs
- Inline comments or external documentation files aligned with existing project conventions

## Workflow
1. Analyze target structure, interfaces, and behavior.
2. Identify documentation scope and audience.
3. Generate content based on type and style.
4. Format for consistency and cross-references.
5. Integrate with existing documentation ecosystem.

## Tooling
- read: component analysis and existing docs review
- rg: reference extraction and pattern identification
- write: documentation file creation
- glob: multi-file documentation organization

## Patterns
- Inline documentation: code analysis -> JSDoc/docstring generation -> inline comments
- API documentation: interface extraction -> reference material -> usage examples
- User guides: feature analysis -> tutorial content -> implementation guidance
- External docs: component overview -> detailed specifications -> integration instructions

## Examples
```
/sc:document src/auth/login.js --type inline
```
Generates JSDoc comments with parameter and return descriptions.

```
/sc:document src/api --type api --style detailed
```
Creates comprehensive API documentation with endpoints, schemas, and usage examples.

```
/sc:document payment-module --type guide --style brief
```
Creates a user-focused guide with practical examples and common use cases.

```
/sc:document components/ --type external
```
Generates external documentation files with props, usage, and integration patterns.

## Boundaries
Will:
- Generate focused documentation for specific components and features.
- Create multiple documentation formats based on audience needs.
- Preserve project documentation conventions and structure.

Will not:
- Generate documentation without analyzing the target and context.
- Override existing documentation standards or project-specific conventions.
- Expose sensitive implementation details.
