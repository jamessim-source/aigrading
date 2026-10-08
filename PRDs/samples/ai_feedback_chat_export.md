# AI Feedback chat export — CSV sample for developers

Sample of the file the **Export Chat** button on the AI Tutor Dashboard (T16, PRD C11.13 D6) writes.
Two samples with the same shape: `ai_feedback_chat_export_sample.csv` (Japanese content, what the Kindai
trial will produce) and `ai_feedback_chat_export_sample_en.csv` (the same rows in English, for reading).

## Columns (fixed, in this order — PM, 8 Oct)

| # | Header | Source | Notes |
|---|---|---|---|
| 1 | `User ID` | the student's username (`hanako.yamada`), as the Student Usages table shows it | not the internal UUID |
| 2 | `Student Name` | the student's display name | |
| 3 | `Class` | the AI Tutor class the snap belongs to (`class_name`) | the export is per class: the dashboard's filters decide which |
| 4 | `Title` | the AI Tutor Assignment's title the snap is tied to | **empty** when the feedback snap is a free snap, not tied to an assignment |
| 5 | `Subject` | the assignment's subject (or the class subject for a free snap) | |
| 6 | `Question` | the thread's `question_overview` — the AI-written summary of what the student submitted and asked | |
| 7 | `Chat` | the whole thread, every message in order, one per line: `[YYYY/MM/DD HH:MM] AI: …` / `[YYYY/MM/DD HH:MM] 生徒: …` (`Student:` in English) | the AI's feedback is the first message of the thread, so there is no separate Feedback column |

## Rows

- **One row per feedback thread** (one per feedback snap). A student who uploaded the same assignment twice
  has two rows, one per version, in the order they were created.
- Only **feedback snaps** (`AITutorgraphType.FEEDBACK`); Snap-to-ask threads are not in this file.
- Scope = the dashboard's current filters (class, lens, start and end date). The dialog does not repeat them.
- Sorted by Student Name, then by the thread's created time.

## File format

- UTF-8 **with BOM** and CRLF line endings, so Excel on Japanese Windows opens it without mojibake.
- Every field quoted (`"…"`). Quotes inside a field are doubled (`""`), as in row 6 of the sample.
- Multi-line cells: the Chat column contains line breaks inside the quotes. Excel, Google Sheets and
  Numbers handle this; a plain-text viewer will show the row spread over several lines, which is expected.
- File name: `ai_feedback_<class>_<YYYY-MM>.csv` (the sample: `ai_feedback_3A_2026-11.csv`).
- The header row is in the tenant's language (Japanese headers for a Japanese tenant: ユーザーID ・ 生徒名 ・
  クラス ・ タイトル ・ 科目 ・ 質問 ・ チャット). The sample files carry the English header so the columns
  can be read side by side with this note.
