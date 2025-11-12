# Phase 1: Figma Export Update Plan
**Date:** 2025-11-12
**Total Lines:** 21,233 lines across 3 files
**Status:** In Progress

## Objective
Update Figma JSON exports to match Front React design system from:
https://github.com/KOSA2025-FINAL-PROJECT-TEAM3/Front

---

## Color Mapping Strategy

### Current Figma Colors → Front React Design Tokens

| Current Color | RGB | Usage | Front React Replacement | New RGB | New Hex |
|--------------|-----|-------|------------------------|---------|---------|
| Primary Green | rgb(76, 176, 79) | Logo, success, accents | Success | rgb(34, 197, 94) | #22c55e |
| Primary Blue | rgb(0, 122, 255) | Buttons, links | Primary | rgb(37, 99, 235) | #2563eb |
| Primary Button | rgb(79, 70, 229) | Buttons | Primary (indigo-600) | rgb(79, 70, 229) | #4f46e5 |
| Danger Red | rgb(245, 66, 54) | Errors, alerts | Danger | rgb(239, 68, 68) | #ef4444 |
| Warning Orange | rgb(255, 153, 0) | Warnings | Warning | rgb(249, 115, 22) | #f97316 |
| Caregiver Accent | N/A | New | Caregiver | rgb(165, 180, 252) | #a5b4fc |
| Senior Accent | N/A | New | Senior | rgb(249, 168, 212) | #f9a8d4 |
| OCR Background | N/A | New | OCR Background | rgb(15, 23, 42) | #0f172a |
| OCR Accent | N/A | New | OCR Accent | rgb(34, 211, 238) | #22d3ee |

### Gray Scale (Keep consistent)
| Color | RGB | Usage |
|-------|-----|-------|
| Text Primary | rgb(31, 41, 55) | Primary text (gray-900) |
| Text Secondary | rgb(107, 114, 128) | Secondary text (gray-500) |
| Border | rgb(229, 231, 235) | Borders (gray-200) |
| Background | rgb(249, 250, 251) | Backgrounds (gray-50) |

### Border Radius
- **Card:** 12px (0.75rem) ✓ Already correct
- **Button/Control:** 8px (0.5rem) ✓ Already correct

---

## Text Replacements

### Branding Change: "실버케어" → "뭐냑?" (AMApill)

**File 1: silvercare-part1-auth-dashboard.json (7,079 lines)**
- Line 3: Description field
- Lines 99-101: Login logo
- Lines 380-382: Signup logo
- Line 695: Terms text
- Lines 1480-1482: Dashboard header
- Lines 2984-2986: Schedule add header
- Lines 4966-4968: Admin header
**Total: 7 instances**

**File 2: silvercare-part2-medication-chat.json (7,909 lines)**
- Line 3: Description field
- Line 69: Header navigation
- Lines 3056-3058: Header logo
**Total: 3 instances**

**File 3: silvercare-part3-disease-report.json (6,245 lines)**
- Line 3: Description field
**Total: 1 instance**

---

## Update Strategy

### Phase 1 Tasks (Current)
1. ✅ Analyze all three JSON files
2. ✅ Map colors from current design to Front React tokens
3. ✅ Update silvercare-part1-auth-dashboard.json
   - Replace brand name text (7 instances) ✓
   - Update primary colors to match Front React ✓
   - Update button colors (primary, secondary, danger) ✓
   - Update text colors for consistency ✓
4. ✅ Update silvercare-part2-medication-chat.json
5. ✅ Update silvercare-part3-disease-report.json
6. ✅ Test and validate JSON structure
7. ✅ Commit and push changes

### Files to Update
- [x] silvercare-part1-auth-dashboard.json (7,079 lines) - ✅ COMPLETED
- [x] silvercare-part2-medication-chat.json (7,909 lines) - ✅ COMPLETED
- [x] silvercare-part3-disease-report.json (6,245 lines) - ✅ COMPLETED

---

## Color Update Details

### Primary Colors to Replace
```
OLD: {"r": 0.3, "g": 0.69, "b": 0.31}    // rgb(76, 176, 79) - Old Green
NEW: {"r": 0.133, "g": 0.773, "b": 0.369} // rgb(34, 197, 94) - Success #22c55e

OLD: {"r": 0, "g": 0.48, "b": 1}          // rgb(0, 122, 255) - Old Blue
NEW: {"r": 0.145, "g": 0.388, "b": 0.922} // rgb(37, 99, 235) - Primary #2563eb

OLD: {"r": 0.31, "g": 0.275, "b": 0.898}  // Keep for indigo-600 buttons
NEW: {"r": 0.31, "g": 0.275, "b": 0.898}  // Primary Button #4f46e5

OLD: {"r": 0.96, "g": 0.26, "b": 0.21}    // rgb(245, 66, 54) - Old Red
NEW: {"r": 0.937, "g": 0.267, "b": 0.267} // rgb(239, 68, 68) - Danger #ef4444

OLD: {"r": 1, "g": 0.6, "b": 0}            // rgb(255, 153, 0) - Old Orange
NEW: {"r": 0.976, "g": 0.451, "b": 0.086} // rgb(249, 115, 22) - Warning #f97316
```

---

## Notes for Next Phase

### Considerations:
- Glass morphism effects (opacity values) should be preserved
- Shadow system (rgba(0, 0, 0, 0.08)) should remain consistent
- Corner radius values are already correct (12px cards, 8px controls)
- Inter font family is correct
- Focus on updating brand colors while maintaining design system integrity

### Next Steps After Phase 1:
- Validate JSON syntax
- Check for any missed color references
- Update README.md to reflect new design tokens
- Create comparison screenshots if needed

---

## Phase 1 Completion Summary

### Updates Applied:
1. **Text Replacements:** All 11 instances of "실버케어" replaced with "뭐냑?"
2. **Color Updates:**
   - Primary Green (Logo/Success): rgb(76,176,79) → rgb(34,197,94) #22c55e
   - Primary Blue (Buttons/Links): rgb(0,122,255) → rgb(37,99,235) #2563eb
   - Updated across all three JSON files consistently
3. **JSON Validation:** All files validated successfully with Python json.tool

### Changes by File:
- **part1:** 7 text replacements + color updates
- **part2:** 3 text replacements + color updates
- **part3:** 1 text replacement + color updates

### Next Steps:
- Consider adding new colors for Caregiver (#a5b4fc) and Senior (#f9a8d4) accents in future phases
- Monitor for any additional UI components that need color updates
- Test Figma import with updated JSON files

---

**Phase 1 Start Time:** 2025-11-12
**Completion Time:** 2025-11-12
**Status:** ✅ COMPLETED
