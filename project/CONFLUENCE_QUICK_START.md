# Confluence Setup - Quick Start (Option 1: Page Hierarchy + TOC)

## ⚡ 5-Minute Setup Overview

This option creates a professional Confluence space with a left-aligned page tree and table of contents, matching your HTML documentation structure.

---

## 📋 What You'll Get

✅ **Professional appearance** similar to your HTML docs  
✅ **Left sidebar navigation** with page tree  
✅ **Table of contents** on every page  
✅ **Full Confluence functionality** (search, comments, versioning)  
✅ **Easy content management** native to Confluence  

---

## 🚀 Step-by-Step Quick Setup

### Phase 1: Create Space (2 minutes)

```
1. Confluence Home → Spaces → Create space
2. Blank space
3. Space name: "Healthcare AI Contact Center Platform"
4. Space key: "HCCP" (or preference)
5. Visibility: Open
6. Create
```

### Phase 2: Create Parent Page (3 minutes)

```
1. Click Create → Blank page
2. Title: "Healthcare AI Contact Center Platform"
3. Copy content from CONFLUENCE_PAGE_TEMPLATES.md → PARENT PAGE section
4. Publish
```

### Phase 3: Create Section Pages (10 minutes)

For each of these 8 sections, **create as child pages of parent**:

1. **Business Context**
   - Copy template from CONFLUENCE_PAGE_TEMPLATES.md
   - Add child pages underneath (See Phase 4)

2. **Architecture**
   - Copy template
   - Add child pages underneath

3. **Workflow**
   - Copy template
   - Add child pages underneath

4. **Component Design**
   - Copy template
   - Add child pages underneath

5. **State Management**
   - Copy template
   - Add child pages underneath

6. **Human-in-the-Loop**
   - Copy template
   - Add child pages underneath

7. **Infrastructure**
   - Copy template
   - Add child pages underneath

8. **Security & Compliance**
   - Copy template
   - Add child pages underneath

### Phase 4: Create Child Pages (15 minutes)

**Under Business Context:**
- Industry Challenges and Business Impact
- Problem Statement
- Design Inputs
- Platform Goals

**Under Architecture:**
- Solution Options
- Competitive Differentiation
- High-Level Architecture
- Runtime Architecture
- Graph Design

**Under Workflow:**
- End-to-End Workflow
- Step-by-Step Breakdown

**Under Component Design:**
- Coordinator Node
- Claims Agent
- Benefits Agent
- Appointment Scheduler
- General Responder

**Under State Management:**
- State Schema
- Checkpointing

**Under Human-in-the-Loop:**
- HITL Design
- Trigger Conditions

**Under Infrastructure:**
- Azure Services
- Observability

**Under Security & Compliance:**
- Security Overview
- HIPAA Alignment

### Phase 5: Create Single Pages (5 minutes)

Create these as **children of parent page**:
- API Reference
- Deployment
- Design Decisions
- Roadmap
- Glossary

### Phase 6: Add Content (Parallel - 20 minutes)

For each page:
```
1. Open CONFLUENCE_PAGE_TEMPLATES.md
2. Find your page template
3. Copy content
4. Paste into Confluence page
5. Add child pages reference (for parent pages)
6. Add TOC macro
7. Publish
```

---

## 📁 File References

| File | Purpose |
|------|---------|
| `CONFLUENCE_SETUP_GUIDE.md` | **Detailed step-by-step guide** (READ THIS FIRST) |
| `CONFLUENCE_PAGE_TEMPLATES.md` | **Ready-to-paste content** for every page |
| `CONFLUENCE_QUICK_START.md` | This file — quick reference |

---

## 🎨 Key Macros to Use

### Table of Contents (Every Page)
```
Insert → Other Macros → Table of Contents
```

### Page Tree (Parent Pages Only)
```
Insert → Other Macros → Page Tree
```

### Code Blocks
```
{code:python}
your code here
{code}
```

### Info Boxes
```
{info}
Important information
{info}

{note}
A note
{note}

{warning}
A warning
{warning}

{tip}
A helpful tip
{tip}
```

---

## 📝 Markdown to Confluence Conversion

| Markdown | Confluence |
|----------|-----------|
| `# Title` | `h1. Title` |
| `## Section` | `h2. Section` |
| `### Subsection` | `h3. Subsection` |
| `**bold**` | `*bold*` |
| `*italic*` | `_italic_` |
| `` `code` `` | `{{code}}` |
| `[Text](url)` | `[Text\|url]` |
| `[Text](Page)` | `[Text\|Page]` |
| Lists (auto) | Lists (auto) |

---

## ✅ Final Checklist

- [ ] Confluence space created
- [ ] Parent page created: "Healthcare AI Contact Center Platform"
- [ ] 8 section parent pages created (Business Context, Architecture, etc.)
- [ ] All child pages created underneath sections
- [ ] Single pages created (API Reference, Deployment, etc.)
- [ ] Content added to all pages from templates
- [ ] TOC macro added to each page
- [ ] Page Tree macro added to parent page
- [ ] All links verified working
- [ ] Space shared with team
- [ ] Confluence URL bookmarked

---

## 🎯 Content Organization

```
Healthcare AI Contact Center Platform (PARENT)
├── Business Context (PARENT)
│   ├── Industry Challenges and Business Impact
│   ├── Problem Statement
│   ├── Design Inputs
│   └── Platform Goals
├── Architecture (PARENT)
│   ├── Solution Options
│   ├── Competitive Differentiation
│   ├── High-Level Architecture
│   ├── Runtime Architecture
│   └── Graph Design
├── Workflow (PARENT)
│   ├── End-to-End Workflow
│   └── Step-by-Step Breakdown
├── Component Design (PARENT)
│   ├── Coordinator Node
│   ├── Claims Agent
│   ├── Benefits Agent
│   ├── Appointment Scheduler
│   └── General Responder
├── State Management (PARENT)
│   ├── State Schema
│   └── Checkpointing
├── Human-in-the-Loop (PARENT)
│   ├── HITL Design
│   └── Trigger Conditions
├── Infrastructure (PARENT)
│   ├── Azure Services
│   └── Observability
├── Security & Compliance (PARENT)
│   ├── Security Overview
│   └── HIPAA Alignment
├── API Reference (SINGLE)
├── Deployment (SINGLE)
├── Design Decisions (SINGLE)
├── Roadmap (SINGLE)
└── Glossary (SINGLE)
```

---

## 💡 Pro Tips

1. **Create pages in sections** — Don't do them all at once. Do one section at a time.

2. **Reuse templates** — All parent sections follow the same template pattern.

3. **Copy from MkDocs** — Your markdown files have all the content already. Just convert the formatting.

4. **Use Confluence's editor** — The WYSIWYG editor is easier than markup. Click "Edit" to toggle between visual and source.

5. **Test TOC macro** — Insert at bottom: `{toc:style=none}`

6. **Link between pages** — Use `[Page Name]` (Confluence auto-suggests pages).

7. **Enable space permissions** — Share with your team after setup.

8. **Archive old pages** — Once migration is complete, you can hide or delete old documentation.

---

## ⏱️ Time Estimate

| Phase | Time | Notes |
|-------|------|-------|
| Create Space | 2 min | One-time setup |
| Create Parent Page | 3 min | Copy template |
| Create Section Pages | 10 min | 8 sections × 1-2 min each |
| Create Child Pages | 10 min | 20+ child pages |
| Create Single Pages | 5 min | 5 pages |
| Add Content | 20 min | Paste templates, add real content |
| **Total** | **~50 min** | Can be done in one sitting |

---

## 🎬 Right Now

1. Open `CONFLUENCE_SETUP_GUIDE.md` (detailed reference)
2. Open `CONFLUENCE_PAGE_TEMPLATES.md` (ready-to-paste content)
3. Go to your Confluence space
4. Start with Phase 1: Create Space

---

## 📞 Troubleshooting

**"Page won't link to another page?"**
→ Use square brackets: `[Page Name]` — Confluence will auto-complete

**"TOC macro not showing?"**
→ Insert → Other Macros → search "Table of Contents" (not TOC)

**"How do I make it look like the HTML?"**
→ TOC macro on left + Page Tree = similar structure
→ Professional styling through space theme settings

**"Want to add the parent page button?"**
→ Space Settings → Sidebar → Add custom navigation

**"Can I export to PDF?"**
→ Page menu (⋯) → Export to PDF ✓

---

## 📚 Next Steps After Setup

1. ✅ Get your space set up using this guide
2. 📤 Share with your team
3. 🔄 Set up documentation reviews/approvals
4. 📊 Enable page analytics (Space Settings → Analytics)
5. 🔐 Configure access controls (Space Settings → Permissions)
6. 🎨 Customize theme (Space Settings → Look and Feel)
7. 📱 Test on mobile (Confluence Cloud works on mobile)

---

## 🎉 You're Ready!

Start with **CONFLUENCE_SETUP_GUIDE.md** for detailed instructions.

Your professional Confluence documentation space will be live in less than an hour! 🚀
