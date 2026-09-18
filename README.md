# Weekly Reporter · 周报克星

![Weekly Reporter 牛牛封面](docs/images/weekly-reporter-cover.png)

[中文介绍页](https://aislowdown.github.io/weekly-reporter/) · [English landing page](https://aislowdown.github.io/weekly-reporter/en.html) · [English README](README.en.md)


## 样本预览

以下为虚构演示，姓名、项目及工时均为示例数据。

![Weekly Reporter 虚构周报样本](docs/images/weekly-reporter-demo.png)


名称：`computer-history-weekly-report`

## 功能

基于 Computer History 或用户提供的活动日志，按研究项目整理每天做了什么。支持对话内候选选择、学术周报、每日活动甘特图、粗略时长统计，以及 HTML、Markdown 和 Obsidian 归档。论文整理注明研究主题，审稿区分稿件与提交状态。

## 使用条件

- 推荐在具备 Computer History 技能、工具及已记录历史的 Codex 环境中使用；本包不包含采集器，也不会自行开启采集。
- 没有 Computer History 时，可提供活动日志或笔记作为替代来源。
- 交互选择取决于宿主能力；无原生多选时支持选择卡片或编号回复。
- Obsidian 归档需要本地知识库访问权限，并由使用者提供或确认位置。

## 安装

下载 [技能安装包](dist/computer-history-weekly-report-public.zip)，将解压后的 `computer-history-weekly-report/` 文件夹放入当前环境的技能目录，或按平台提供的技能安装流程操作。

压缩包包含 `SKILL.md`、`agents/openai.yaml` 和图表规范 `references/html-charts.md`。不包含真实周报、历史活动、姓名、账号、本地路径、未公开稿件、截图或估算台账。

## 调用示例

> 用 $computer-history-weekly-report 整理上周的科研活动，先按项目列候选，让我在对话中选择。

> 把已选项目做成 HTML 周报，附每日活动和大概投入时间，并按累计用时排序。


## 每日投入图表

支持按小时绘制每日堆积柱，柱内显示项目占当天的比例，图例显示项目占全周的比例。各天沿用统一项目顺序，颜色固定，提供红—橙—黄—绿—蓝—紫配色预设。仅调整柱图颜色时保持周报其他区域不变。详见 [图表规范](references/html-charts.md)。

---

## English overview

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

[English project page](https://aislowdown.github.io/weekly-reporter/en.html) · [Full English README](README.en.md) · [Chart guidelines](references/html-charts.md)
