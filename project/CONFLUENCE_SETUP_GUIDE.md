# Confluence Setup Guide: Page Hierarchy + TOC

This guide walks you through creating a professional Confluence space with the same appearance and navigation as your HTML documentation.

---

## 📋 Step 1: Create Your Confluence Space

1. Go to your Confluence instance
2. Click **Spaces** → **Create space**
3. Select **Create a blank space**
4. Fill in:
   - **Space name:** Healthcare AI Contact Center Platform
   - **Space key:** HCCP (or your preference)
   - **Visibility:** Open (or Private)
5. Click **Create**

---

## 🏗️ Step 2: Create the Parent Page

This is your main documentation hub.

### Create Parent Page
1. Click **Create** → **Blank page**
2. **Title:** `Healthcare AI Contact Center Platform`
3. **Add this content:**

```
h1. Healthcare AI Contact Center Platform

*Solution & Technical Design Document — Agentic Call Workflow Engine — LangGraph + Azure*

Version 1.0 | 2026

h2. Welcome

This documentation provides a complete technical design for the Healthcare AI Contact Center Platform, an intelligent agentic system for automating healthcare contact center interactions.

h2. Documentation Structure

{page-tree:root=@self}

h2. Quick Navigation

* [Business Context|Business Context] — Industry challenges and platform goals
* [Architecture|Architecture] — System design and technology choices
* [Workflow|Workflow] — End-to-end call processing pipeline
* [Component Design|Component Design] — Specialist agents and tools
* [State Management|State Management] — Multi-turn conversation state
* [Human-in-the-Loop|Human-in-the-Loop] — HITL safety gates
* [Infrastructure|Infrastructure] — Azure services and observability
* [Security & Compliance|Security & Compliance] — HIPAA alignment
* [API Reference|API Reference] — Endpoint specifications
* [Deployment|Deployment] — Kubernetes deployment design
* [Design Decisions|Design Decisions] — Trade-offs and rationale
* [Roadmap|Roadmap] — Future enhancements
* [Glossary|Glossary] — Terminology reference

h2. Key Sections

{toc}
```

4. Click **Publish**

---

## 📑 Step 3: Create Child Pages (Sections)

Create these 13 main section pages as **child pages** of the parent.

### How to Create Child Pages:
1. From the parent page, click **⋯** (three dots) → **Create child page**
2. Or go to parent → **Create** → **Child page**

### Section Pages to Create:

| Section | Type | Content |
|---------|------|---------|
| Business Context | Parent | Overview page with sub-pages |
| Architecture | Parent | Overview page with sub-pages |
| Workflow | Parent | Overview page with sub-pages |
| Component Design | Parent | Overview page with sub-pages |
| State Management | Parent | Overview page with sub-pages |
| Human-in-the-Loop | Parent | Overview page with sub-pages |
| Infrastructure | Parent | Overview page with sub-pages |
| Security & Compliance | Parent | Overview page with sub-pages |
| API Reference | Single | Complete API documentation |
| Deployment | Single | Deployment instructions |
| Design Decisions | Single | Design rationale |
| Roadmap | Single | Future roadmap |
| Glossary | Single | Terminology |

---

## 🌳 Step 4: Create the Full Hierarchy

### Business Context (Parent)
**Child pages:**
- Industry Challenges and Business Impact
- Problem Statement
- Design Inputs
- Platform Goals

### Architecture (Parent)
**Child pages:**
- Solution Options
- Competitive Differentiation
- High-Level Architecture
- Runtime Architecture
- Graph Design

### Workflow (Parent)
**Child pages:**
- End-to-End Workflow
- Step-by-Step Breakdown

### Component Design (Parent)
**Child pages:**
- Coordinator Node
- Claims Agent
- Benefits Agent
- Appointment Scheduler
- General Responder

### State Management (Parent)
**Child pages:**
- State Schema
- Checkpointing

### Human-in-the-Loop (Parent)
**Child pages:**
- HITL Design
- Trigger Conditions

### Infrastructure (Parent)
**Child pages:**
- Azure Services
- Observability

### Security & Compliance (Parent)
**Child pages:**
- Security Overview
- HIPAA Alignment

### Single-Page Sections:
- API Reference
- Deployment
- Design Decisions
- Roadmap
- Glossary

---

## 📝 Step 5: Add Content to Each Page

### For Parent Section Pages (e.g., "Business Context"):

Use this template:

```
h1. Business Context

h2. Overview

[Add overview paragraph from your documentation]

h2. Child Pages

{page-tree:root=@self}

h2. In This Section

* [Industry Challenges and Business Impact|Industry Challenges and Business Impact]
* [Problem Statement|Problem Statement]
* [Design Inputs|Design Inputs]
* [Platform Goals|Platform Goals]

{toc}
```

### For Child Pages:

Copy content directly from your markdown files:

```
h1. Industry Challenges and Business Impact

[Paste the full content from your documentation]

{toc}
```

---

## 🎨 Step 6: Add Navigation Macros

### Add Table of Contents (TOC) to Every Page

1. Click **Insert** → **Other macros**
2. Search for **Table of Contents**
3. Configure:
   - **Include children:** ✓ (for parent pages)
   - **Exclude first heading:** ✓
4. Click **Insert**

### Add Page Tree (Sidebar-like Navigation)

For the **main parent page only**, use the Page Tree macro:

1. Click **Insert** → **Other macros**
2. Search for **Page Tree**
3. Configure:
   - **Root page:** Healthcare AI Contact Center Platform
   - **Show indentation:** ✓
   - **Link titles:** ✓
4. Click **Insert**

---

## 🎯 Step 7: Final Structure

Your Confluence space will look like:

```
Healthcare AI Contact Center Platform (PARENT)
├── Business Context
│   ├── Industry Challenges and Business Impact
│   ├── Problem Statement
│   ├── Design Inputs
│   └── Platform Goals
├── Architecture
│   ├── Solution Options
│   ├── Competitive Differentiation
│   ├── High-Level Architecture
│   ├── Runtime Architecture
│   └── Graph Design
├── Workflow
│   ├── End-to-End Workflow
│   └── Step-by-Step Breakdown
├── Component Design
│   ├── Coordinator Node
│   ├── Claims Agent
│   ├── Benefits Agent
│   ├── Appointment Scheduler
│   └── General Responder
├── State Management
│   ├── State Schema
│   └── Checkpointing
├── Human-in-the-Loop
│   ├── HITL Design
│   └── Trigger Conditions
├── Infrastructure
│   ├── Azure Services
│   └── Observability
├── Security & Compliance
│   ├── Security Overview
│   └── HIPAA Alignment
├── API Reference
├── Deployment
├── Design Decisions
├── Roadmap
└── Glossary
```

---

## 🎨 Step 8: Confluence Formatting Tips

### Convert Markdown to Confluence:

| Markdown | Confluence |
|----------|-----------|
| `# Heading` | `h1. Heading` |
| `## Heading` | `h2. Heading` |
| `### Heading` | `h3. Heading` |
| `**bold**` | `*bold*` |
| `_italic_` | `_italic_` |
| `` `code` `` | `{{code}}` |
| `` ```python code``` `` | `{code:python}code{code}` |
| `[Link text](url)` | `[Link text\|url]` |
| `- bullet` | `* bullet` |
| `1. number` | `# number` |

### Code Blocks in Confluence:

```
{code:python}
def hello():
    print("Hello, World!")
{code}
```

### Tables:

Use Confluence's native table editor (Insert → Table)

### Info Boxes (Admonitions):

```
{info}
ℹ️ This is informational content
{info}

{note}
📝 This is a note
{note}

{warning}
⚠️ This is a warning
{warning}

{tip}
💡 This is a tip
{tip}
```

---

## 📲 Step 9: Make it Look Professional

### Customize the Space:

1. Go to **Space settings** → **Look and feel**
2. Upload your logo (optional)
3. Set theme colors to match your brand
4. Configure sidebar (optional)

### Add a Space Home Page:

1. Create a visually appealing home page with:
   - Welcome section
   - Quick links to main sections
   - Latest updates section
   - Contact/support information

---

## ✅ Step 10: Verification Checklist

- [ ] Parent page created: "Healthcare AI Contact Center Platform"
- [ ] 13 main section pages created
- [ ] Child pages organized under correct parents
- [ ] Table of Contents macro on each page
- [ ] Page Tree macro on parent page
- [ ] All content properly formatted
- [ ] Navigation links working
- [ ] Space is accessible to intended users
- [ ] Confluence URL bookmarked

---

## 🚀 Quick Content Migration Steps

To populate pages efficiently:

1. **Copy from MkDocs:** Read markdown files from your `docs/` folder
2. **Convert formatting:** Use the table in Step 8
3. **Paste into Confluence:** Use **Insert → Formatted code** for code blocks
4. **Add macros:** Insert TOC, Page Tree, and admonition boxes
5. **Publish:** Click **Publish** on each page

---

## 💡 Pro Tips

1. **Use Blueprints:** Create a page template for consistent formatting
2. **Enable comments:** Allow team feedback on pages
3. **Use labels:** Tag pages by topic (healthcare, architecture, security)
4. **Watch pages:** Click **Watch** to get notifications of changes
5. **Export to PDF:** Page → **⋯** → **Export to PDF**
6. **Version history:** Every page automatically tracks changes

---

## 🎬 Next Steps

1. Create the parent page
2. Create main section pages (one at a time)
3. Add child pages under each section
4. Copy and format content from your MkDocs documentation
5. Add navigation macros (TOC, Page Tree)
6. Share the space with your team

---

## 📞 Support

If you need help with Confluence:
- [Confluence Documentation](https://confluence.atlassian.com/doc/confluence-documentation-home-27654.html)
- [Confluence Cloud Macros](https://confluence.atlassian.com/doc/macros-139387.html)
- Your Confluence administrator

---

**Your Confluence space is now ready for professional healthcare documentation!** 🎉
