# 🛡️ SafeSandbox

**An offline file triage and Windows event-log analysis workspace.**

Inspect suspicious files, parse EVTX logs, extract indicators, run YARA rules,
and review unfamiliar content without uploading evidence or executing it.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/Desktop-PyQt6-41CD52?style=flat&logo=qt&logoColor=white)
![Offline](https://img.shields.io/badge/Analysis-100%25%20Offline-5138EE)
![Platform](https://img.shields.io/badge/Platform-Windows-blue)

---

## ⚡ Why This Exists

Initial file triage often means switching between viewers, event-log tools,
hash utilities, string extractors, IOC parsers, and rule scanners.

**SafeSandbox** brings that first-pass analysis into one local workspace:

- Drop in a file, folder, archive, or Windows event log
- Detect content even when the filename has no extension
- Review hashes, metadata, strings, indicators, and embedded content
- Parse large EVTX files into a searchable investigation timeline
- Run bundled YARA rules without sending the sample anywhere
- Export useful findings for reporting or deeper investigation

---

## 🖥️ Feature Overview

### 🪟 Windows Event Log Analyzer

- Parse Windows `.evtx` files into a structured event table
- Review timestamp, event ID, level, provider, channel, and computer
- Build a visual histogram across the event timeline
- Stack activity by event ID for faster pattern recognition
- Search and filter large event collections
- Add suspicious indicators during an investigation
- Export timeline and event data to CSV
- Load multiple eligible sources into the same timeline

### 🔍 Static File Triage

- Calculate MD5, SHA-1, and SHA-256 hashes
- Detect file type using extension, magic bytes, and content inspection
- Review file size, timestamps, entropy, and available metadata
- Extract readable text and inspect raw hexadecimal data
- Preview supported documents, images, email, scripts, and structured data
- Inspect source content without opening the file in its native application
- Identify embedded files, archive members, and nested content

### 📡 IOC Extraction

- Extract URLs, domains, IP addresses, email addresses, and other indicators
- Group findings by type and severity
- Copy individual indicators directly from the findings panel
- Filter findings during investigation
- Highlight indicators inside supported views
- Include relevant findings in the copied analysis summary

### 📐 YARA Rule Library

- Bundled library containing hundreds of local YARA rules
- Search rules by file type, category, severity, or free text
- Validate rule syntax before scanning
- Run selected rules against the active file
- Review matched rule names, descriptions, tags, and severity
- No external rule service or network lookup required

### 📦 Archive & Embedded Content Review

- Inspect common archive and package formats
- Browse contained files without manually extracting everything first
- Open supported members directly inside the same workspace
- Move through nested content using the investigation breadcrumb
- Return to the parent file without starting a new case

### 🕵️ Extensionless File Detection

- File picker accepts filenames with or without an extension
- Magic-byte inspection identifies formats such as PDF, archives, and binaries
- Text sniffing recognizes readable content when no signature is available
- Useful for evidence renamed to `sample`, `attachment`, or `report`

### 📊 Search, Summary & Export

- Search inside the active document or rendered content
- Navigate between search matches
- Copy a compact investigation summary to the clipboard
- Export supported analysis and timeline views
- Zoom document content without changing the original file

---

## 🎨 UI Highlights

- **Investigation dashboard** — clean start screen for files, logs, rules, and archives
- **Case-based workflow** — open evidence, investigate, then use **Close case** to reset
- **Automatic findings panel** — appears when analysis results are available
- **Help + Themes** — keyboard reference and multiple light/dark appearances
- **Native desktop window** — PyQt6 WebEngine shell with no browser address bar
- **Animated launch card** — matching SafeSandbox startup experience
- **Fullscreen by default** — maximized workspace on launch

---

## 🚀 Quick Start

### 1. Keep the application files together

```text
SafeSandbox/
├── SafeSandbox_v2.pyw
└── SafeSandbox_v2.html
```

### 2. Install dependencies

```bash
pip install PyQt6 PyQt6-WebEngine
```

### 3. Run the desktop application

```bash
pythonw SafeSandbox_v2.pyw
```

> On Windows, use `pythonw` instead of `python` to suppress the console window.  
> You can also double-click `SafeSandbox_v2.pyw`.

### Browser-only option

Double-click `SafeSandbox_v2.html` to open the same workspace directly in a
modern browser. Python is not required for the browser-only option.

---

## 🧭 Basic Workflow

1. Start SafeSandbox.
2. Click **New investigation**, drag evidence onto the dashboard, or open a
   folder.
3. Wait for the local parser and security checks to complete.
4. Review the content view, event timeline, findings, and YARA matches.
5. Search, filter, copy indicators, or export relevant results.
6. Click **Close case** to clear the investigation and return to the dashboard.

---

## 📁 Supported Content

| Category | Examples |
|----------|----------|
| Event logs | EVTX, CSV, TSV, structured logs |
| Documents | PDF, DOCX, XLSX, PPTX, RTF, ODT |
| Scripts | PowerShell, JavaScript, VBScript, Batch, HTA |
| Executables | PE, DLL, SYS, ELF, Mach-O |
| Archives | ZIP, TAR, GZIP, 7Z, RAR, CAB, JAR |
| Email & shortcuts | EML, MSG, LNK, URL, Webloc |
| Data | JSON, XML, YAML, SQLite, Registry files |
| Images & certificates | PNG, JPEG, SVG, PEM, DER, PFX |
| Extensionless evidence | Files identified through magic bytes or text sniffing |

> Support varies by format. Some files provide a full preview; others provide
> metadata, extracted text, structural information, hexadecimal data, or
> security findings.

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Y` | Open the YARA rule library |
| `T` | Open themes |
| `?` or `H` | Open Help |
| `F` | Focus content search |
| `Ctrl+Enter` | Copy the investigation summary |
| `Ctrl+C` | Copy raw content when no text is selected |
| `Ctrl+V` | Inspect a file copied to the clipboard |
| `Esc` | Close a dialog or clear search |

---

## 🔐 Safety Model

- Files are analyzed locally
- Evidence is read but never executed
- Macros and scripts are displayed, not run
- Documents are not launched in their native applications
- No detonation, emulation, or behavioral execution is performed
- A strict Content Security Policy blocks network requests from the local page
- No file content is intentionally uploaded by SafeSandbox

> SafeSandbox is a static-analysis tool. For known malware or hostile samples,
> continue using an isolated virtual machine and your organization’s handling
> procedures.

---

## 🗂️ File Structure

```text
SafeSandbox/
├── SafeSandbox_v2.pyw     # Native desktop launcher
├── SafeSandbox_v2.html    # Analysis engine and interface
└── README.md              # Setup and usage guide
```

The `.pyw` and `.html` files must remain in the same folder.

---

## 👤 Author

**Barath A C**  
SOC Analyst II  
[LinkedIn](https://linkedin.com/in/barath07) · [GitHub](https://github.com/Barath711)

---

*SafeSandbox is inspired by [Loupe](https://github.com/Loupe-tools/Loupe).*
