---
title: Settings & Configuration
type: guide
ui: tk
description: Configure MBASIC behavior
keywords: [settings, configuration, variables, keywords, case]
---

# Settings & Configuration

Control MBASIC behavior using the settings system.

## Variable Case Handling

Control how variable name case is handled:

```basic
' View current setting
SHOW SETTINGS "variables.case_conflict"

' Change policy
SET "variables.case_conflict" "first_wins"   ' Default
SET "variables.case_conflict" "error"        ' Catch typos!
SET "variables.case_conflict" "prefer_upper"
SET "variables.case_conflict" "prefer_lower"
SET "variables.case_conflict" "prefer_mixed"
```

**Example - Error mode catches typos:**
```basic
SET "variables.case_conflict" "error"
10 TotalCount = 0
20 TotalCont = 1  ' ERROR: Typo detected!
```

## Keyword Case Handling

Control how keywords are displayed:

```basic
' View setting
SHOW SETTINGS "keywords.case_style"

' Change style
SET "keywords.case_style" "force_lower"      ' print, for (default)
SET "keywords.case_style" "force_upper"      ' PRINT, FOR
SET "keywords.case_style" "force_capitalize" ' Print, For (modern)
SET "keywords.case_style" "first_wins"
SET "keywords.case_style" "preserve"
```

## View All Settings

```basic
' Show all settings
SHOW SETTINGS

' Show category
SHOW SETTINGS "variables"
SHOW SETTINGS "keywords"
SHOW SETTINGS "editor"
```

## Get Help on Settings

```basic
HELP SET "variables.case_conflict"
```

Shows full documentation for that specific setting.

[← Back to Tk GUI Help](index.md)
