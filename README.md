# Meeting Minutes Automation 🎙️📝

An AI-powered multi-agent system built with [crewAI](https://crewai.com) that automatically transcribes meeting audio, generates structured meeting minutes, and drafts email summaries — all in a single automated flow.

---

## Overview

This project uses a **crewAI Flow** to chain together three automated stages:

1. **Transcription** — Splits a `.wav` audio file into chunks and transcribes each chunk using OpenAI's Whisper model.
2. **Meeting Minutes Generation** — A crew of two AI agents processes the transcript to produce a summary, extract action items, and analyze sentiment, then compiles everything into a polished Markdown document.
3. **Gmail Draft** — A dedicated Gmail agent takes the finished meeting minutes and creates a draft email, ready to send to stakeholders.

### Example Output

The system produces three intermediate files in the `meeting_minutes/` directory before assembling the final document:

| File | Description |
|---|---|
| `summary.txt` | Concise paragraph summarizing the meeting |
| `action_items.txt` | Bullet-point list of follow-up tasks |
| `sentiment.txt` | Tone/sentiment analysis of the discussion |

---

## Project Structure

```
meeting_minutes/
├── src/
│   └── meeting_minutes/
│       ├── main.py                          # Entry point — defines the crewAI Flow
│       ├── EarningsCall.wav                 # Sample audio file for testing
│       ├── crews/
│       │   ├── meeting_minutes_crew/        # Summarizer + Writer agents
│       │   │   ├── meeting_minutes_crew.py
│       │   │   └── config/
│       │   │       ├── agents.yaml
│       │   │       └── tasks.yaml
│       │   └── gmailcrew/                   # Gmail draft agent
│       │       ├── gmailcrew.py
│       │       ├── tools/
│       │       │   ├── gmail_tool.py
│       │       │   └── gmail_utility.py
│       │       └── config/
│       │           ├── agents.yaml
│       │           └── tasks.yaml
│       └── tools/
│           └── custom_tool.py
├── meeting_minutes/                         # Generated output files
│   ├── summary.txt
│   ├── action_items.txt
│   └── sentiment.txt
├── pyproject.toml
├── .env
└── README.md
```

---

## Prerequisites

- Python `>=3.10` and `<3.14`
- [uv]— fast Python package manager
- An **OpenAI API key** (used for Whisper transcription and LLM agents)
- A **Gmail account** with API access configured (for the Gmail draft crew)

---

## Usage

Place your meeting audio file (`.wav` format) at:

```
src/meeting_minutes/EarningsCall.wav
```

Then run the full flow from the project root:

```bash
crewai run
```

This will:
1. Transcribe the audio file in 60-second chunks using Whisper.
2. Run the `MeetingMinutesCrew` to generate `summary.txt`, `action_items.txt`, and `sentiment.txt`.
3. Assemble a final Markdown meeting minutes document.
4. Trigger the `GmailCrew` to create a Gmail draft with the meeting minutes as the body.

You can also visualize the flow graph before running:

```bash
python -m meeting_minutes.main
```

---

## Agents

### MeetingMinutesCrew

| Agent | Role | Responsibility |
|---|---|---|
| `meeting_minutes_summarizer` | Summarizer | Reads the transcript, produces a summary, extracts action items, and analyzes sentiment — writing each to a separate file. |
| `meeting_minutes_writer` | Writer | Reads the three output files and compiles them into a well-formatted Markdown meeting minutes document. |

### GmailCrew

| Agent | Role | Responsibility |
|---|---|---|
| `gmail_draft_agent` | Gmail Draft Agent | Takes the meeting minutes body and creates a Gmail draft using the Gmail API tool. |

---

## Configuration

Agent goals and task descriptions are fully configurable via YAML files — no code changes needed for most customizations:

- `src/meeting_minutes/crews/meeting_minutes_crew/config/agents.yaml` — Define agent roles, goals, and backstories
- `src/meeting_minutes/crews/meeting_minutes_crew/config/tasks.yaml` — Define task descriptions and expected outputs
- `src/meeting_minutes/crews/gmailcrew/config/agents.yaml` — Configure the Gmail agent
- `src/meeting_minutes/crews/gmailcrew/config/tasks.yaml` — Configure the Gmail drafting task

The meeting minutes document is currently configured to use:
- **Company:** NewAI
- **Organizer:** Harshit
- **Location:** Zoom

To change these defaults, edit the `meeting_minutes_writing_task` description in `tasks.yaml`.

---

## Dependencies

| Package | Purpose |
|---|---|
| `crewai[tools]==1.3.0` | Multi-agent orchestration framework |
| `openai` | Whisper transcription + LLM backbone |
| `pydub` | Audio file chunking |
| `python-dotenv` | Environment variable management |

---


