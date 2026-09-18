# Weekly Reporter

[中文](README.md) · [English project page](https://aislowdown.github.io/weekly-reporter/en.html)

![Weekly Reporter illustrated cover (Chinese)](docs/images/weekly-reporter-cover.png)

**Weekly Reporter** is a Codex skill that turns computer activity records or your own work notes into clear, project-based academic weekly reports. It helps researchers explain what they worked on, how each project progressed, and what still needs attention.

### Key features

- **Organize by project:** Keep literature reviews, experiments, data analysis, code, papers, presentations, and administrative work connected to the projects they support.
- **Choose what to include:** Review candidate activities in the conversation before generating the report. Selection can use supported controls or numbered replies.
- **Review daily progress:** Produce daily activity summaries and retrospective Gantt-style views, with concrete task descriptions.
- **Visualize time spent:** When supported by records, show daily stacked bars, project totals, and percentage shares. Approximate durations are explicitly labeled as estimates.
- **Save your reports:** Generate HTML and Markdown, with optional archiving to an Obsidian vault you specify.

### Installation

Download the [weekly report skill package](dist/computer-history-weekly-report-public.zip), extract it, and place the `computer-history-weekly-report/` folder in your environment's skill directory, or follow its supported installation workflow.

Use a compatible Codex environment with Computer History and existing records, or provide your own activity logs. This skill does not include a recorder or enable recording automatically.

### Example request

> Use $computer-history-weekly-report to summarize my research activities from last week. First group the activities by project and let me choose what to include in this conversation. Then generate an HTML weekly report with daily activities and approximate time spent, ordered by total project time.

### Time estimates and privacy

Activity-window estimates are not exact working hours. Missing records do not mean no work was done. Reports distinguish observed activities, plans, and verified outcomes. Generating or saving a report does not publish it automatically.

The public skill package contains reusable instructions, not personal computer-history records. Preview names, projects, and durations are fictional; the current preview images are in Chinese, while reports can be generated in your preferred language.

[English project page](https://aislowdown.github.io/weekly-reporter/en.html) · [Chart guidelines](references/html-charts.md)

## Sample report

![Fictional weekly report sample in Chinese](docs/images/weekly-reporter-demo.png)
