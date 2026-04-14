import { useState, useRef } from "react";

// ── Design tokens ──
const T = {
  bg: "#FAFAFA",
  card: "#FFFFFF",
  primary: "#4F46E5",
  primaryLight: "#EEF2FF",
  accent: "#10B981",
  warn: "#F59E0B",
  error: "#EF4444",
  text: "#1E293B",
  textSec: "#64748B",
  textTer: "#94A3B8",
  border: "#E2E8F0",
  radius: "12px",
  shadow: "0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04)",
};

// ── Grading data — Image 1: student worksheet, 6/10 ──
const IMG_DOC_V1 = {
  title: "英語 関係代名詞① テスト",
  totalPoints: 10,
  score: 6,
  feedbackEn:
    "Good understanding of relative clauses. Q1① and Q1② were left blank — review fill-in-the-blank with 'who + verb'. Q2③, Q2④ and Q3⑤ were answered correctly.",
  feedbackJa:
    "関係代名詞の理解は良好です。問1①②が未記入でした —「who＋動詞」の穴埋め問題を復習しましょう。問2③④・問3⑤は正解でした。",
  questions: [
    { id: "問1①", ok: false, marks: "0/2" },
    { id: "問1②", ok: false, marks: "0/2" },
    { id: "問2③", ok: true,  marks: "2/2" },
    { id: "問2④", ok: true,  marks: "2/2" },
    { id: "問3⑤", ok: true,  marks: "2/2" },
  ],
};

// ── Grading data — Image 2: model answer sheet, 10/10 ──
const IMG_DOC = {
  title: "英語 文法テスト #4",
  totalPoints: 10,
  score: 10,
  feedbackEn:
    "Perfect score! Excellent command of relative clauses with 'who'. All 5 questions answered correctly — full marks across every section.",
  feedbackJa:
    "満点！関係代名詞「who」の使い方が完璧です。全5問正解 — すべてのセクションで満点を獲得しました。",
  questions: [
    { id: "問1①", ok: true, marks: "2/2" },
    { id: "問1②", ok: true, marks: "2/2" },
    { id: "問2③", ok: true, marks: "2/2" },
    { id: "問2④", ok: true, marks: "2/2" },
    { id: "問3⑤", ok: true, marks: "2/2" },
  ],
};

// ── Translations ──
const i18n = {
  en: {
    appTitle: "AI Grading",
    myClasses: "My Classes",
    addClass: "Add Class",
    scanQR: "Scan a Class QR Code",
    uploadQR: "Upload QR Code",
    classJoined: "Class Joined!",
    classJoinedDesc: "You've successfully joined",
    redirecting: "Redirecting...",
    testsAssignments: "Tests & Assignments",
    assignmentDetails: "Assignment Details",
    results: "Results",
    currentClass: "Current Class",
    switchClass: "Switch",
    all: "All",
    filterNew: "New",
    filterSubmitted: "Submitted",
    filterMarked: "Marked",
    statusNew: "New",
    statusSubmitted: "Submitted",
    statusMarked: "Marked",
    due: "Due",
    questions: "questions",
    submitWork: "Submit Your Work",
    submitDesc: "Take a photo of your worksheet",
    takePhoto: "📷 Take Photo",
    retake: "↺ Retake",
    captured: "Captured",
    confirmAnalyse: "Confirm & Analyse",
    analysingTitle: "Analysing Your Work...",
    analysingDesc: "AI marking engine is processing your submission",
    aiScore: "AI Analysis Score",
    aiMarked: "AI Marked",
    questionBreakdown: "Question Breakdown",
    reviewAIMarking: "Review AI marking?",
    reviewDesc: "You can override scores before submitting to your teacher.",
    submitToTeacher: "Submit to Teacher →",
    successTitle: "Successfully Submitted!",
    successDesc: "Your self-assessment has been submitted.\nYour teacher will review it soon!",
    yourScore: "Your Score",
    markedByTeacher: "Marked by Teacher",
    correct: "○",
    partial: "△",
    mistake: "×",
    langToggle: "🇯🇵 日本語",
    noAssignments: "No assignments found",
    mathematics: "Mathematics",
    english: "English",
    chemistry: "Chemistry",
    history: "History",
    biology: "Biology",
    physics: "Physics",
  },
  ja: {
    appTitle: "AI採点",
    myClasses: "クラス一覧",
    addClass: "クラスを追加",
    scanQR: "クラスQRコードをスキャン",
    uploadQR: "QRコードをアップロード",
    classJoined: "クラスに参加しました！",
    classJoinedDesc: "参加しました",
    redirecting: "リダイレクト中...",
    testsAssignments: "テスト・課題",
    assignmentDetails: "課題の詳細",
    results: "結果",
    currentClass: "現在のクラス",
    switchClass: "切り替え",
    all: "すべて",
    filterNew: "新着",
    filterSubmitted: "提出済み",
    filterMarked: "採点済み",
    statusNew: "新着",
    statusSubmitted: "提出済み",
    statusMarked: "採点済み",
    due: "締切",
    questions: "問",
    submitWork: "解答を提出",
    submitDesc: "ワークシートの写真を撮ってください",
    takePhoto: "📷 写真を撮る",
    retake: "↺ 撮り直す",
    captured: "撮影済み",
    confirmAnalyse: "確認・分析する",
    analysingTitle: "採点中...",
    analysingDesc: "AI採点エンジンが提出物を処理しています",
    aiScore: "AI採点スコア",
    aiMarked: "AI採点済み",
    questionBreakdown: "問題別内訳",
    reviewAIMarking: "AI採点を確認しますか？",
    reviewDesc: "先生に提出する前にスコアを修正できます。",
    submitToTeacher: "先生に提出 →",
    successTitle: "提出完了！",
    successDesc: "自己採点を提出しました。\n先生がまもなく確認します！",
    yourScore: "あなたのスコア",
    markedByTeacher: "先生が採点済み",
    correct: "○",
    partial: "△",
    mistake: "×",
    langToggle: "🇺🇸 English",
    noAssignments: "課題が見つかりません",
    mathematics: "数学",
    english: "英語",
    chemistry: "化学",
    history: "歴史",
    biology: "生物",
    physics: "物理",
  },
};

// ── Shared Components ──

const NavBar = ({ title, onBack, lang, onLangToggle, rightIcon }) => (
  <div style={{ background: "#fff", borderBottom: `1px solid ${T.border}`, flexShrink: 0 }}>
    <div
      style={{
        display: "flex",
        alignItems: "center",
        height: 52,
        padding: "0 8px",
        paddingTop: "env(safe-area-inset-top)",
      }}
    >
      {onBack ? (
        <button
          onClick={onBack}
          style={{
            background: "none",
            border: "none",
            padding: "8px 12px",
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            color: T.primary,
            flexShrink: 0,
          }}
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path
              d="M15 18L9 12L15 6"
              stroke={T.primary}
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </button>
      ) : (
        <div style={{ width: 20, flexShrink: 0 }} />
      )}

      <span
        style={{
          flex: 1,
          fontSize: 16,
          fontWeight: 600,
          color: T.text,
          textAlign: "center",
          overflow: "hidden",
          whiteSpace: "nowrap",
          textOverflow: "ellipsis",
          padding: "0 8px",
        }}
      >
        {title}
      </span>

      {rightIcon ?? (
        <button
          onClick={onLangToggle}
          style={{
            background: T.primaryLight,
            border: "none",
            borderRadius: 20,
            padding: "6px 11px",
            cursor: "pointer",
            fontSize: 12,
            fontWeight: 700,
            color: T.primary,
            flexShrink: 0,
            whiteSpace: "nowrap",
          }}
        >
          {i18n[lang].langToggle}
        </button>
      )}
    </div>
  </div>
);

const Card = ({ children, style, onClick }) => (
  <div
    onClick={onClick}
    style={{
      background: T.card,
      borderRadius: T.radius,
      boxShadow: T.shadow,
      padding: 16,
      ...style,
      cursor: onClick ? "pointer" : "default",
    }}
  >
    {children}
  </div>
);

const Badge = ({ children, color = T.primary }) => (
  <span
    style={{
      display: "inline-block",
      padding: "3px 8px",
      borderRadius: 10,
      fontSize: 11,
      fontWeight: 600,
      background: color + "18",
      color,
    }}
  >
    {children}
  </span>
);

const Pill = ({ children, active, onClick }) => (
  <button
    onClick={onClick}
    style={{
      padding: "7px 16px",
      borderRadius: 20,
      fontSize: 13,
      fontWeight: active ? 600 : 400,
      background: active ? T.primary : T.card,
      color: active ? "#fff" : T.textSec,
      border: active ? "none" : `1px solid ${T.border}`,
      cursor: "pointer",
      flexShrink: 0,
      whiteSpace: "nowrap",
    }}
  >
    {children}
  </button>
);

// ── Class data ──
const CLASS_COLORS = ["#4F46E5", "#10B981", "#F59E0B", "#EF4444", "#06B6D4", "#7C3AED", "#3B82F6", "#6366F1"];

const CLASSES = [
  { id: 1, name: "Class 10A", teacher: "Ms. Tanaka", subjectKey: "mathematics" },
  { id: 2, name: "Class 10B", teacher: "Ms. Tanaka", subjectKey: "english" },
  { id: 3, name: "Class 10C", teacher: "Ms. Tanaka", subjectKey: "english" },
  { id: 4, name: "Class 10D", teacher: "Ms. Tanaka", subjectKey: "chemistry" },
  { id: 5, name: "Class 10E", teacher: "Ms. Tanaka", subjectKey: "mathematics" },
  { id: 6, name: "Class 10F", teacher: "Ms. Tanaka", subjectKey: "history" },
  { id: 7, name: "Class 10G", teacher: "Ms. Tanaka", subjectKey: "biology" },
  { id: 8, name: "Class 10H", teacher: "Ms. Tanaka", subjectKey: "physics" },
];

// ── SCREENS ──

// ── ClassDocIcon — small document icon used in class tiles ──
const ClassDocIcon = ({ color }) => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
    <rect x="4" y="2" width="12" height="16" rx="2" fill="white" fillOpacity="0.9" />
    <path d="M7 7H13M7 10H13M7 13H11" stroke={color} strokeWidth="1.5" strokeLinecap="round" />
    <path d="M14 2L18 6V20H6" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
    <path d="M14 2V6H18" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const ClassSelectionScreen = ({ t, selectedClassId, onSelectClass, onAddClass, classes }) => (
  <div className="scrollable" style={{ flex: 1, background: T.bg }}>
    {/* Header row */}
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "16px 16px 8px",
      }}
    >
      <span style={{ fontSize: 17, fontWeight: 700, color: T.text }}>
        {t.myClasses} ({classes.length})
      </span>
      <button
        onClick={onAddClass}
        style={{
          width: 32,
          height: 32,
          borderRadius: "50%",
          background: T.primary,
          border: "none",
          cursor: "pointer",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "#fff",
          fontSize: 22,
          lineHeight: 1,
        }}
      >
        +
      </button>
    </div>

    {/* Class list */}
    <div style={{ padding: "4px 16px" }}>
      {classes.map((cls, i) => {
        const color = CLASS_COLORS[CLASSES.findIndex(c => c.id === cls.id) % CLASS_COLORS.length];
        const isSelected = cls.id === selectedClassId;
        return (
          <div
            key={cls.id}
            onClick={() => onSelectClass(cls)}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 14,
              background: T.card,
              borderRadius: T.radius,
              boxShadow: isSelected
                ? `0 0 0 2px ${T.primary}, ${T.shadow}`
                : T.shadow,
              padding: "12px 14px",
              marginBottom: 10,
              cursor: "pointer",
            }}
          >
            {/* Colored icon tile */}
            <div
              style={{
                width: 46,
                height: 46,
                borderRadius: 12,
                background: color,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                flexShrink: 0,
              }}
            >
              <ClassDocIcon color={color} />
            </div>

            {/* Text */}
            <div style={{ flex: 1, minWidth: 0 }}>
              <div
                style={{
                  fontSize: 15,
                  fontWeight: 700,
                  color: T.text,
                  overflow: "hidden",
                  whiteSpace: "nowrap",
                  textOverflow: "ellipsis",
                }}
              >
                {cls.name}
              </div>
              <div style={{ fontSize: 12, color: T.textSec, marginTop: 2 }}>
                {cls.teacher} · {t[cls.subjectKey]}
              </div>
            </div>

            {/* Selected checkmark */}
            {isSelected && (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" fill={T.primary} />
                <path d="M7 12L10.5 15.5L17 8.5" stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            )}
          </div>
        );
      })}
    </div>
    <div style={{ height: 20 }} />
  </div>
);

const AddClassScreen = ({ t, onClassJoined }) => (
  <div className="scrollable" style={{ flex: 1, background: T.bg, display: "flex", flexDirection: "column", alignItems: "center" }}>
    {/* QR icon header */}
    <div style={{ marginTop: 32, marginBottom: 16, textAlign: "center" }}>
      <div
        style={{
          width: 72,
          height: 72,
          borderRadius: 20,
          background: "#EDE9FE",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          margin: "0 auto 14px",
        }}
      >
        <svg width="34" height="34" viewBox="0 0 24 24" fill="none">
          <rect x="2" y="2" width="8" height="8" rx="1.5" stroke="#7C3AED" strokeWidth="1.8" />
          <rect x="14" y="2" width="8" height="8" rx="1.5" stroke="#7C3AED" strokeWidth="1.8" />
          <rect x="2" y="14" width="8" height="8" rx="1.5" stroke="#7C3AED" strokeWidth="1.8" />
          <rect x="4.5" y="4.5" width="3" height="3" fill="#7C3AED" />
          <rect x="16.5" y="4.5" width="3" height="3" fill="#7C3AED" />
          <rect x="4.5" y="16.5" width="3" height="3" fill="#7C3AED" />
          <path d="M14 14H16M18 14H22M14 16V18M14 20V22M16 22H18M20 20H22M20 22H22" stroke="#7C3AED" strokeWidth="1.8" strokeLinecap="round" />
        </svg>
      </div>
      <div style={{ fontSize: 17, fontWeight: 700, color: T.text }}>{t.scanQR}</div>
    </div>

    {/* Camera viewfinder */}
    <div style={{ position: "relative", width: "80%", maxWidth: 300, aspectRatio: "1 / 1", margin: "0 auto" }}>
      {/* Background with sample QR code */}
      <div style={{ width: "100%", height: "100%", background: "#000", borderRadius: 4, display: "flex", alignItems: "center", justifyContent: "center" }}>
        {/* Sample QR code */}
        <svg xmlns="http://www.w3.org/2000/svg" width="72%" height="72%" viewBox="0 0 296 296" fill="white">
          <path d="M32,236v-28h56v56H32V236L32,236z M80,236v-20H40v40h40V236L80,236z M48,236v-12h24v24H48V236L48,236z M104,260v-4h-8v-16h8v-24h8v-8H96v-8H64v-8h8v-8H56v16h-8v-8H32v-8h16v-16h-8v8h-8v-16h16v8h8v8h8v-8h8v8h16v-8h-8v-8H56v-8h24v-8H56v-8h-8v8H32v-24h8v8h48v-8h-8v-8H64v8h-8v-8H40V96h16v16h8v-8h16v-8h8v8h-8v8h8v8h8v-16h8v-8h-8V72h16v8h8v8h-8v8h8v48h-16v-8h-8v8h-8v8h-8v8h8v8h8v8h16v-8h-8v-8h-8v-8h16v16h8v-16h8v16h8v-24h8v-8h8v8h-8v8h8v8h24v-8h-8v-8h-8v-16h-8v-8h8v-8h8v-8h-8v-8h-8v16h-8v-8h-8v8h-8v-8h8v-8h-8V72h-8v-8h8v8h8V40h8v16h16v-8h-8V32h16v8h-8v8h16v-8h8v-8h16v24h-16v-8h-8v16h8v24h8v-8h8v40h16v-8h-8V96h16v24h16v-8h-8V96h8v16h8v-8h16v16h-8v-8h-8v8h-8v24h8v8h-8v8h-16v8h-8v8h-16v-8h-8v-8h-8v16h8v8h24v8h16v-8h-8v-8h8v-8h8v8h8v8h8v-16h-8v-8h16v24h-8v16h8v16h-8v24h8v8h-24v16h-24v-8h16v-8h-16v-16h-8v16h-8v8h8v8h-16v-24h-8v16h-8v-8h-8v-32h8v24h8v-24h8v-16h-8v-8h-8v-8h8v-8h-8v-8h-8v32h8v8h-16v16h-8v16h8v8h-8v8h16v8h-16v-8h-8v-8h-8v16h-32V260L104,260z M128,248v-8h8v-24h-16v8h8v8h-16v8h-8v8h8v8h16V248L128,248z M240,240v-8h8v-16h8v-8h-8v-24h-8v24h8v8h-8v8h-8v24h8V240L240,240z M200,236v-4h-8v8h8V236L200,236z M152,220v-4h-8v8h8V220L152,220z M224,212v-12h-24v24h24V212L224,212z M208,212v-4h8v8h-8V212L208,212z M144,204v-4h16v-8h-16v-8h-8v8h8v8h-16v-8h-8v8h-8v-8h-8v-8h-8v-8h-8v8h-8v8h8v-8h8v8h8v8h8v8h32V204L144,204z M120,180v-4h-8v8h8V180L120,180z M160,176v-8h-16v8h8v8h8V176L160,176z M208,164v-4h-8v8h8V164L208,164z M224,156v-4h8v-24h-8v8h-8v8h-8v-8h-16v-8h-8v-8h8V96h-8v-8h-8v-8h-8v8h-8V64h8v8h8v-8h-8v-8h-8v8h-8v24h8v8h8v-8h8v24h-8v8h-8v8h8v16h8v-8h16v8h8v8h16v8h8V156L224,156z M216,148v-4h8v8h-8V148L216,148z M88,140v-4h8v-8h-8v8h-8v8h8V140L88,140z M112,124v-4h-8v8h8V124L112,124z M112,84v-4h-8v8h8V84L112,84z M144,80v-8h-8v16h8V80L144,80z M192,44v-4h-8v8h8V44L192,44z M256,260v-4h8v8h-8V260L256,260z M256,144v-8h-8v-8h8v8h8v16h-8V144L256,144z M32,60V32h56v56H32V60L32,60zM80,60V40H40v40h40V60L80,60z M48,60V48h24v24H48V60L48,60z M208,60V32h56v56h-56V60L208,60z M256,60V40h-40v40h40V60L256,60zM224,60V48h24v24h-24V60L224,60z M96,60v-4h8v8h-8V60L96,60z M112,52v-4h-8V32h8v8h8v-8h8v8h-8v16h-8V52L112,52z"/>
        </svg>
      </div>
      {/* Corner brackets */}
      {[
        { top: -3, left: -3, borderTop: `3px solid #A5B4FC`, borderLeft: `3px solid #A5B4FC` },
        { top: -3, right: -3, borderTop: `3px solid #A5B4FC`, borderRight: `3px solid #A5B4FC` },
        { bottom: -3, left: -3, borderBottom: `3px solid #A5B4FC`, borderLeft: `3px solid #A5B4FC` },
        { bottom: -3, right: -3, borderBottom: `3px solid #A5B4FC`, borderRight: `3px solid #A5B4FC` },
      ].map((style, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            width: 24,
            height: 24,
            ...style,
          }}
        />
      ))}
    </div>

    {/* Divider */}
    <div style={{ display: "flex", alignItems: "center", gap: 12, margin: "20px 0", width: "80%" }}>
      <div style={{ flex: 1, height: 1, background: T.border, borderStyle: "dashed" }} />
      <span style={{ fontSize: 13, color: T.textSec }}>or</span>
      <div style={{ flex: 1, height: 1, background: T.border, borderStyle: "dashed" }} />
    </div>

    {/* Upload button */}
    <button
      onClick={() => onClassJoined && onClassJoined(CLASSES[0])}
      style={{
        padding: "12px 32px",
        borderRadius: 24,
        border: `1.5px solid ${T.primary}`,
        background: "transparent",
        color: T.primary,
        fontSize: 14,
        fontWeight: 600,
        cursor: "pointer",
      }}
    >
      {t.uploadQR}
    </button>
  </div>
);

const ClassJoinedScreen = ({ t, className }) => (
  <div
    style={{
      flex: 1,
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      background: T.bg,
      gap: 12,
      padding: "0 40px",
      textAlign: "center",
    }}
  >
    {/* Green doc icon */}
    <div
      style={{
        width: 72,
        height: 72,
        borderRadius: 20,
        background: "#10B981",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        marginBottom: 8,
      }}
    >
      <svg width="38" height="38" viewBox="0 0 24 24" fill="none">
        <rect x="4" y="2" width="12" height="18" rx="2" fill="white" fillOpacity="0.9" />
        <path d="M7 8H13M7 11H13M7 14H10" stroke="#10B981" strokeWidth="1.5" strokeLinecap="round" />
        <path d="M15 2L19 6" stroke="white" strokeWidth="1.5" strokeLinecap="round" />
        {/* pencil */}
        <path d="M17 13L20 10L22 12L19 15Z" fill="white" />
        <path d="M17 13L16 16L19 15Z" fill="white" />
      </svg>
    </div>
    <div style={{ fontSize: 22, fontWeight: 800, color: T.text }}>{t.classJoined}</div>
    <div style={{ fontSize: 14, color: T.textSec, lineHeight: 1.6 }}>
      {t.classJoinedDesc}
      <br />
      <span style={{ fontWeight: 700, color: T.text }}>{className}</span>
    </div>
    <div style={{ fontSize: 13, color: T.textTer, marginTop: 12 }}>{t.redirecting}</div>
  </div>
);

const GradingListScreen = ({ onNav, onSwitchClass, selectedClass, t }) => {
  const [filter, setFilter] = useState("all");

  const assignments = [
    { title: "英語 文法テスト #4",      date: "Apr 8",  score: "10/10", status: "marked",   doc: IMG_DOC },
    { title: "英語 関係代名詞① テスト", date: "Apr 9",  score: null,    status: "new",      doc: IMG_DOC_V1 },
    { title: "数学 小テスト #7",        date: "Apr 5",  score: null,    status: "new",      doc: null },
    { title: "英語 Reading #2",         date: "Apr 3",  score: null,    status: "submitted", doc: null },
    { title: "数学 小テスト #6",        date: "Mar 28", score: "4/5",   status: "marked",   doc: null },
    { title: "英語 文法テスト #3",      date: "Mar 25", score: "3/5",   status: "marked",   doc: null },
  ];

  const statusMeta = {
    new:       { color: T.primary, label: t.statusNew },
    submitted: { color: T.warn,    label: t.statusSubmitted },
    marked:    { color: T.accent,  label: t.statusMarked },
  };

  const filters = [
    ["all",       t.all],
    ["new",       t.filterNew],
    ["submitted", t.filterSubmitted],
    ["marked",    t.filterMarked],
  ];

  const visible =
    filter === "all" ? assignments : assignments.filter((a) => a.status === filter);

  return (
    <div className="scrollable" style={{ flex: 1, background: T.bg }}>
      <div style={{ padding: "12px 16px 0" }}>
        <Card style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <div>
            <div style={{ fontSize: 11, color: T.textSec }}>{t.currentClass}</div>
            <div style={{ fontSize: 15, fontWeight: 700, color: T.text }}>
              {selectedClass ? `${selectedClass.teacher} • ${selectedClass.name} · ${t[selectedClass.subjectKey]}` : "Tanaka先生 • Class A"}
            </div>
          </div>
          <button
            onClick={onSwitchClass}
            style={{
              padding: "8px 14px",
              borderRadius: 8,
              background: T.primaryLight,
              color: T.primary,
              fontSize: 13,
              fontWeight: 600,
              border: "none",
              cursor: "pointer",
            }}
          >
            {t.switchClass}
          </button>
        </Card>
      </div>

      <div style={{ display: "flex", gap: 8, padding: "12px 16px", overflowX: "auto" }}>
        {filters.map(([key, label]) => (
          <Pill key={key} active={filter === key} onClick={() => setFilter(key)}>
            {label}
          </Pill>
        ))}
      </div>

      <div style={{ padding: "0 16px" }}>
        {visible.length === 0 ? (
          <div style={{ textAlign: "center", padding: "40px 16px", color: T.textTer, fontSize: 14 }}>
            {t.noAssignments}
          </div>
        ) : (
          visible.map((item, i) => {
            const meta = statusMeta[item.status];
            return (
              <Card
                key={i}
                onClick={() =>
                  onNav(item.status === "marked" ? "grading_result" : "grading_test", item.doc)
                }
                style={{ marginBottom: 8, display: "flex", alignItems: "center", gap: 12 }}
              >
                <div
                  style={{
                    width: 42,
                    height: 42,
                    borderRadius: 10,
                    background: meta.color + "15",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    flexShrink: 0,
                  }}
                >
                  {item.status === "marked" ? (
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                      <path d="M9 12L11 14L15 10" stroke={T.accent} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                      <circle cx="12" cy="12" r="9" stroke={T.accent} strokeWidth="2" />
                    </svg>
                  ) : (
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                      <rect x="3" y="3" width="18" height="18" rx="2" stroke={meta.color} strokeWidth="2" />
                      <path d="M7 12L10 15L17 9" stroke={meta.color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  )}
                </div>

                <div style={{ flex: 1, minWidth: 0 }}>
                  <div
                    style={{
                      fontSize: 14,
                      fontWeight: 600,
                      color: T.text,
                      overflow: "hidden",
                      whiteSpace: "nowrap",
                      textOverflow: "ellipsis",
                    }}
                  >
                    {item.title}
                  </div>
                  <div style={{ fontSize: 12, color: T.textSec, marginTop: 2 }}>{item.date}</div>
                </div>

                <div style={{ textAlign: "right", flexShrink: 0 }}>
                  <Badge color={meta.color}>{meta.label}</Badge>
                  {item.score && (
                    <div style={{ fontSize: 14, fontWeight: 700, color: T.accent, marginTop: 4 }}>
                      {item.score}
                    </div>
                  )}
                </div>
              </Card>
            );
          })
        )}
      </div>
      <div style={{ height: 16 }} />
    </div>
  );
};

const GradingTestScreen = ({ t, doc }) => {
  const [phase, setPhase] = useState("submit"); // submit | analysing | results | success
  const [hasPhoto, setHasPhoto] = useState(false);
  const [capturedImageUrl, setCapturedImageUrl] = useState(null);
  const fileInputRef = useRef(null);
  // Editable scores: initialised from AI result, user can adjust before submitting
  const [editedScores, setEditedScores] = useState(() =>
    doc.questions.map((q) => parseInt(q.marks.split("/")[0], 10))
  );

  const maxScores = doc.questions.map((q) => parseInt(q.marks.split("/")[1], 10));
  const editedTotal = editedScores.reduce((a, b) => a + b, 0);

  const adjustScore = (idx, delta) => {
    setEditedScores((prev) =>
      prev.map((s, i) => i === idx ? Math.max(0, Math.min(maxScores[i], s + delta)) : s)
    );
  };

  const handleTakePhoto = () => {
    fileInputRef.current?.click();
  };

  const handleFileSelect = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    if (capturedImageUrl) URL.revokeObjectURL(capturedImageUrl);
    const url = URL.createObjectURL(file);
    setCapturedImageUrl(url);
    setHasPhoto(true);
    e.target.value = "";
  };

  const handleRetake = () => {
    if (capturedImageUrl) URL.revokeObjectURL(capturedImageUrl);
    setCapturedImageUrl(null);
    setHasPhoto(false);
  };

  const handleConfirm = () => {
    setPhase("analysing");
    setTimeout(() => setPhase("results"), 2800);
  };

  // ── Analysing ──
  if (phase === "analysing") {
    return (
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          gap: 16,
          background: T.bg,
          padding: "0 32px",
        }}
      >
        <div style={{ fontSize: 52 }}>🔍</div>
        <div style={{ fontSize: 18, fontWeight: 700, color: T.text, textAlign: "center" }}>
          {t.analysingTitle}
        </div>
        <div style={{ fontSize: 13, color: T.textSec, textAlign: "center", lineHeight: 1.6 }}>
          {t.analysingDesc}
        </div>
        <div style={{ display: "flex", gap: 6, marginTop: 4 }}>
          {[0, 1, 2].map((i) => (
            <div
              key={i}
              style={{
                width: 10,
                height: 10,
                borderRadius: "50%",
                background: T.primary,
                animation: `pulse 1.2s ${i * 0.2}s infinite`,
              }}
            />
          ))}
        </div>
        <style>{`@keyframes pulse{0%,80%,100%{transform:translateY(0);opacity:0.4}40%{transform:translateY(-10px);opacity:1}}`}</style>
      </div>
    );
  }

  // ── AI Results ──
  if (phase === "results") {
    const perfect = editedTotal === doc.totalPoints;
    const scoreColor = perfect ? T.accent : T.warn;
    const scoreBg = perfect
      ? "linear-gradient(135deg, #F0FDF4, #ECFDF5)"
      : "linear-gradient(135deg, #FFF7ED, #FFFBEB)";
    const scoreBorder = perfect ? "#BBF7D0" : "#FDE68A";

    return (
      <div className="scrollable" style={{ flex: 1, background: T.bg }}>
        <div style={{ padding: "12px 16px" }}>
          {/* Score card */}
          <Card
            style={{
              textAlign: "center",
              background: scoreBg,
              border: `1px solid ${scoreBorder}`,
              marginBottom: 12,
            }}
          >
            <div style={{ fontSize: 13, color: T.textSec, marginBottom: 6 }}>{t.aiScore}</div>
            <div style={{ fontSize: 52, fontWeight: 800, color: scoreColor, lineHeight: 1 }}>
              {editedTotal}
              <span style={{ fontSize: 22, color: T.textSec }}>/{doc.totalPoints}</span>
            </div>
            {perfect && <div style={{ fontSize: 20, marginTop: 4 }}>🎉</div>}
            <div style={{ marginTop: 8 }}>
              <Badge color={scoreColor}>{t.aiMarked}</Badge>
            </div>
          </Card>

          {/* Question breakdown — editable */}
          <div
            style={{
              fontSize: 13,
              fontWeight: 700,
              color: T.textSec,
              textTransform: "uppercase",
              letterSpacing: 0.5,
              margin: "4px 0 8px",
            }}
          >
            {t.questionBreakdown}
          </div>

          {doc.questions.map((q, i) => {
            const es = editedScores[i];
            const mx = maxScores[i];
            const qColor = es === mx ? T.accent : es === 0 ? T.error : T.warn;
            const qLabel = es === mx ? t.correct : es === 0 ? t.mistake : t.partial;
            return (
              <Card
                key={i}
                style={{
                  marginBottom: 8,
                  borderLeft: `3px solid ${qColor}`,
                  padding: "12px 14px",
                }}
              >
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                  <span style={{ fontSize: 13, fontWeight: 700, color: T.text }}>{q.id}</span>
                  <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                    <span style={{ fontSize: 12, fontWeight: 600, color: qColor }}>{qLabel}</span>
                    {/* Stepper */}
                    <div style={{ display: "flex", alignItems: "center", gap: 0 }}>
                      <button
                        onClick={() => adjustScore(i, -1)}
                        disabled={es === 0}
                        style={{
                          width: 30, height: 30,
                          borderRadius: "8px 0 0 8px",
                          border: `1px solid ${T.border}`,
                          borderRight: "none",
                          background: es === 0 ? T.bg : "#fff",
                          color: es === 0 ? T.textTer : T.text,
                          fontSize: 16,
                          fontWeight: 700,
                          cursor: es === 0 ? "default" : "pointer",
                          display: "flex", alignItems: "center", justifyContent: "center",
                        }}
                      >
                        −
                      </button>
                      <div
                        style={{
                          minWidth: 44,
                          height: 30,
                          border: `1px solid ${T.border}`,
                          background: "#fff",
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "center",
                          fontSize: 13,
                          fontWeight: 700,
                          color: qColor,
                        }}
                      >
                        {es}/{mx}
                      </div>
                      <button
                        onClick={() => adjustScore(i, 1)}
                        disabled={es === mx}
                        style={{
                          width: 30, height: 30,
                          borderRadius: "0 8px 8px 0",
                          border: `1px solid ${T.border}`,
                          borderLeft: "none",
                          background: es === mx ? T.bg : "#fff",
                          color: es === mx ? T.textTer : T.text,
                          fontSize: 16,
                          fontWeight: 700,
                          cursor: es === mx ? "default" : "pointer",
                          display: "flex", alignItems: "center", justifyContent: "center",
                        }}
                      >
                        +
                      </button>
                    </div>
                  </div>
                </div>
              </Card>
            );
          })}

          <button
            onClick={() => setPhase("success")}
            style={{
              width: "100%",
              padding: 16,
              borderRadius: 12,
              marginTop: 16,
              background: T.primary,
              color: "#fff",
              fontSize: 15,
              fontWeight: 700,
              border: "none",
              cursor: "pointer",
            }}
          >
            {t.submitToTeacher}
          </button>
        </div>
        <div style={{ height: 16 }} />
      </div>
    );
  }

  // ── Success ──
  if (phase === "success") {
    const perfect = editedTotal === doc.totalPoints;
    const scoreColor = perfect ? T.accent : T.warn;
    return (
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          background: T.bg,
          padding: "0 32px",
          gap: 16,
          textAlign: "center",
        }}
      >
        {/* Green checkmark circle */}
        <div
          style={{
            width: 80,
            height: 80,
            borderRadius: "50%",
            background: "#DCFCE7",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            marginBottom: 4,
          }}
        >
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none">
            <path
              d="M5 13L9 17L19 7"
              stroke="#16A34A"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </div>

        {/* Title */}
        <div style={{ fontSize: 20, fontWeight: 800, color: T.text }}>
          {t.successTitle}
        </div>

        {/* Subtitle */}
        <div style={{ fontSize: 13, color: T.textSec, lineHeight: 1.7, whiteSpace: "pre-line" }}>
          {t.successDesc}
        </div>

        {/* Score */}
        <div
          style={{
            marginTop: 8,
            padding: "18px 40px",
            background: T.card,
            borderRadius: T.radius,
            boxShadow: T.shadow,
          }}
        >
          <div style={{ fontSize: 11, color: T.textSec, marginBottom: 4, textTransform: "uppercase", letterSpacing: 0.5 }}>
            {t.yourScore}
          </div>
          <div style={{ fontSize: 48, fontWeight: 800, color: scoreColor, lineHeight: 1 }}>
            {editedTotal}
            <span style={{ fontSize: 20, color: T.textSec }}>/{doc.totalPoints}</span>
          </div>
          {perfect && <div style={{ fontSize: 20, marginTop: 6 }}>🎉</div>}
        </div>
      </div>
    );
  }

  // ── Submit ──
  return (
    <div className="scrollable" style={{ flex: 1, background: T.bg }}>
      <div style={{ padding: "12px 16px" }}>
        {/* Assignment info */}
        <Card>
          <div style={{ fontSize: 16, fontWeight: 700, color: T.text, marginBottom: 4 }}>
            {doc?.title ?? ""}
          </div>
          <div style={{ fontSize: 12, color: T.textSec }}>
            Tanaka先生 • {t.due} Apr 10 • 5 {t.questions}
          </div>
        </Card>

        {/* Hidden file input */}
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          style={{ display: "none" }}
          onChange={handleFileSelect}
        />

        {/* Capture area */}
        {!hasPhoto ? (
          <Card
            style={{
              marginTop: 12,
              border: `2px dashed ${T.border}`,
              textAlign: "center",
              padding: "28px 20px",
            }}
          >
            <svg
              width="44"
              height="44"
              viewBox="0 0 24 24"
              fill="none"
              style={{ margin: "0 auto 12px", display: "block" }}
            >
              <rect x="2" y="6" width="20" height="14" rx="2" stroke={T.textTer} strokeWidth="1.5" />
              <circle cx="12" cy="13" r="3" stroke={T.textTer} strokeWidth="1.5" />
              <path d="M8 6L9.5 3H14.5L16 6" stroke={T.textTer} strokeWidth="1.5" />
            </svg>
            <div style={{ fontSize: 15, fontWeight: 600, color: T.text, marginBottom: 6 }}>
              {t.submitWork}
            </div>
            <div style={{ fontSize: 12, color: T.textSec, marginBottom: 20, lineHeight: 1.5 }}>
              {t.submitDesc}
            </div>
            <button
              onClick={handleTakePhoto}
              style={{
                padding: "12px 28px",
                borderRadius: 10,
                background: T.primary,
                color: "#fff",
                fontSize: 14,
                fontWeight: 600,
                border: "none",
                cursor: "pointer",
              }}
            >
              {t.takePhoto}
            </button>
          </Card>
        ) : (
          <Card style={{ marginTop: 12, padding: 0, overflow: "hidden", border: `1.5px solid ${T.accent}` }}>
            {/* Captured image */}
            <img
              src={capturedImageUrl}
              alt="captured worksheet"
              style={{
                width: "100%",
                display: "block",
                maxHeight: 380,
                objectFit: "contain",
                background: "#F1F5F9",
              }}
            />
            {/* Footer */}
            <div
              style={{
                padding: "10px 14px",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                borderTop: `1px solid ${T.border}`,
              }}
            >
              <Badge color={T.accent}>{t.captured}</Badge>
              <button
                onClick={handleRetake}
                style={{
                  background: "none",
                  border: "none",
                  fontSize: 12,
                  color: T.textSec,
                  cursor: "pointer",
                  padding: 0,
                }}
              >
                {t.retake}
              </button>
            </div>
          </Card>
        )}

        {/* Confirm CTA */}
        <button
          onClick={hasPhoto ? handleConfirm : undefined}
          style={{
            width: "100%",
            padding: 16,
            borderRadius: 12,
            marginTop: 16,
            background: T.primary,
            color: "#fff",
            fontSize: 15,
            fontWeight: 700,
            border: "none",
            cursor: hasPhoto ? "pointer" : "default",
            opacity: hasPhoto ? 1 : 0.4,
            transition: "opacity 0.2s",
          }}
        >
          {t.confirmAnalyse}
        </button>
      </div>
      <div style={{ height: 16 }} />
    </div>
  );
};

const GradingResultScreen = ({ t, doc }) => {
  const perfect = doc.score === doc.totalPoints;
  const scoreColor = perfect ? T.accent : T.warn;
  const scoreBg = perfect
    ? "linear-gradient(135deg, #F0FDF4, #ECFDF5)"
    : "linear-gradient(135deg, #FFF7ED, #FFFBEB)";
  const scoreBorder = perfect ? "#BBF7D0" : "#FDE68A";

  return (
    <div className="scrollable" style={{ flex: 1, background: T.bg }}>
      <div style={{ padding: "12px 16px" }}>
        {/* Score */}
        <Card style={{ textAlign: "center", background: scoreBg, border: `1px solid ${scoreBorder}` }}>
          <div style={{ fontSize: 13, color: T.textSec, marginBottom: 6 }}>{t.yourScore}</div>
          <div style={{ fontSize: 52, fontWeight: 800, color: scoreColor, lineHeight: 1 }}>
            {doc.score}
            <span style={{ fontSize: 22, color: T.textSec }}>/{doc.totalPoints}</span>
          </div>
          {perfect && <div style={{ fontSize: 20, marginTop: 4 }}>🎉</div>}
          <div style={{ marginTop: 8 }}>
            <Badge color={scoreColor}>{t.markedByTeacher}</Badge>
          </div>
        </Card>

        {/* Question breakdown */}
        <div
          style={{
            fontSize: 13,
            fontWeight: 700,
            color: T.textSec,
            textTransform: "uppercase",
            letterSpacing: 0.5,
            margin: "12px 0 8px",
          }}
        >
          {t.questionBreakdown}
        </div>

        {doc.questions.map((q, i) => {
          const [qs, qm] = q.marks.split("/").map(Number);
          const qColor = qs === qm ? T.accent : qs === 0 ? T.error : T.warn;
          const qLabel = qs === qm ? t.correct : qs === 0 ? t.mistake : t.partial;
          return (
          <Card
            key={i}
            style={{
              marginBottom: 8,
              borderLeft: `3px solid ${qColor}`,
              padding: "12px 14px",
            }}
          >
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <span style={{ fontSize: 13, fontWeight: 700, color: T.text }}>{q.id}</span>
              <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                <span style={{ fontSize: 16, fontWeight: 700, color: qColor }}>
                  {qLabel}
                </span>
                <span style={{ fontSize: 14, fontWeight: 700, color: qColor }}>
                  {q.marks}
                </span>
              </div>
            </div>
          </Card>
          );
        })}
      </div>
      <div style={{ height: 16 }} />
    </div>
  );
};

// ── MAIN APP ──
export default function App() {
  const [screen, setScreen] = useState("class_selection");
  const [history, setHistory] = useState([]);
  const [lang, setLang] = useState("en");
  const [selectedDoc, setSelectedDoc] = useState(IMG_DOC);
  const [selectedClass, setSelectedClass] = useState(CLASSES[0]);
  const [joinedClassName, setJoinedClassName] = useState("");
  const [unlockedClassIds, setUnlockedClassIds] = useState(CLASSES.filter(c => c.id !== 1).map(c => c.id));

  const t = i18n[lang];
  const isJa = lang === "ja";

  const push = (s) => {
    setHistory((h) => [...h, screen]);
    setScreen(s);
  };
  const pop = () => {
    const h = [...history];
    const prev = h.pop() || "grading";
    setHistory(h);
    setScreen(prev);
  };

  const handleSelectClass = (cls) => {
    setSelectedClass(cls);
    setHistory(["class_selection"]);
    setScreen("grading");
  };

  const handleAddClass = () => push("add_class");

  // Simulate joining a class from the QR screen
  const handleClassJoined = (cls) => {
    setJoinedClassName(cls.name);
    setUnlockedClassIds((ids) => ids.includes(cls.id) ? ids : [...ids, cls.id]);
    push("class_joined");
    setTimeout(() => {
      setSelectedClass(cls);
      setHistory([]);
      setScreen("grading");
    }, 2000);
  };

  const titles = {
    class_selection: t.myClasses,
    add_class:       t.addClass,
    class_joined:    "",
    grading:         t.testsAssignments,
    grading_test:    t.assignmentDetails,
    grading_result:  t.results,
  };

  return (
    <div
      style={{
        width: "100vw",
        height: "100dvh",
        display: "flex",
        flexDirection: "column",
        background: T.bg,
        fontFamily: '-apple-system, BlinkMacSystemFont, "Hiragino Sans", "Noto Sans JP", sans-serif',
        overflow: "hidden",
        position: "fixed",
        top: 0,
        left: 0,
      }}
    >
      <NavBar
        title={titles[screen] || ""}
        onBack={screen !== "grading" && screen !== "class_selection" ? pop : null}
        lang={lang}
        onLangToggle={() => setLang((l) => (l === "en" ? "ja" : "en"))}
        rightIcon={screen === "add_class" ? (
          <button
            style={{
              background: "none",
              border: "none",
              cursor: "pointer",
              padding: "8px 10px",
              display: "flex",
              alignItems: "center",
              color: T.textSec,
            }}
          >
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
              <circle cx="8" cy="15" r="4" stroke={T.textSec} strokeWidth="1.8" />
              <path d="M12 11L18 5" stroke={T.textSec} strokeWidth="1.8" strokeLinecap="round" />
              <path d="M17 4L20 7" stroke={T.textSec} strokeWidth="1.8" strokeLinecap="round" />
              <path d="M15 9L18 6" stroke={T.textSec} strokeWidth="1.8" strokeLinecap="round" />
            </svg>
          </button>
        ) : null}
      />

      {screen === "class_selection" && (
        <ClassSelectionScreen
          t={t}
          selectedClassId={selectedClass?.id}
          onSelectClass={handleSelectClass}
          onAddClass={handleAddClass}
          classes={CLASSES.filter(c => unlockedClassIds.includes(c.id))}
        />
      )}
      {screen === "add_class" && (
        <AddClassScreen t={t} onClassJoined={handleClassJoined} />
      )}
      {screen === "class_joined" && (
        <ClassJoinedScreen t={t} className={joinedClassName} />
      )}
      {screen === "grading" && (
        <GradingListScreen
          onNav={(s, doc) => { setSelectedDoc(doc ?? IMG_DOC); push(s); }}
          onSwitchClass={() => push("class_selection")}
          selectedClass={selectedClass}
          t={t}
        />
      )}
      {screen === "grading_test" && (
        <GradingTestScreen
          t={t}
          doc={selectedDoc}
        />
      )}
      {screen === "grading_result" && (
        <GradingResultScreen t={t} isJa={isJa} doc={selectedDoc} />
      )}
    </div>
  );
}
