---
category: file-management
description: To delete a file from disk
keywords: ['command', 'data', 'error', 'file', 'for', 'if', 'kill', 'open', 'program', 'read']
syntax: KILL <filename>
title: KILL
type: statement
---

# KILL

## Syntax

```basic
KILL <filename>
```

**Versions:** Disk

## Purpose

To delete a file from disk.

## Remarks

If a KILL statement is given for a file that is currently OPEN, a RFile already open R error occurs. KILL is used for all types of disk files: program files, random data files and sequential data files.

## Example

```basic
200 KILL RDATA1R
              See also Appendix B.
```

## See Also
- [LOAD](load.md) - To load a file from disk into memory
- [MERGE](merge.md) - To merge a specified disk file into the      program currently in memory
- [NAME](name.md) - To change the name of a disk file
- [SAVE](save.md) - To save a program file on disk
