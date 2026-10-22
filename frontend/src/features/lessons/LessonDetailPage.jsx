import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../../api/client";
import { useApiData } from "../../api/useApiData";
import { useUnits } from "../units/useUnits";
import { useAuth } from "../../auth/useAuth";
import { DialogueScript } from "./DialogueViews";
import GrammarRules from "./GrammarRules";
import { useLessonActivity } from '../activity/useLessonActivity';

const TABS = [{key:"vocabulary",label:"المفردات"},{key:"content",label:"الدرس"},{key:"exercises",label:"التمارين"}];

// A lesson plus what belongs to it: its words (the vocabulary endpoint is per
// unit) and its dialogues.
async function loadLesson(lessonId) {
  const lesson = (await api.get(`/lessons/${lessonId}`)).data;
  const [vocabulary, dialogues] = await Promise.all([
    api.get(`/units/${lesson.unit_id}/vocabulary`),
    api.get(`/lessons/${lessonId}/dialogues`),
  ]);
  return {
    lesson,
    words: vocabulary.data.filter(word => word.lesson_id === lesson.id),
    dialogues: dialogues.data,
  };
}

/** Stand-alone page for one lesson (/lessons/:lessonId), with browser text-to-speech. */
export default function LessonDetailPage() {
  const { lessonId } = useParams();
  const navigate = useNavigate();
  const { student } = useAuth();
  const { units, selectUnit } = useUnits();
  const { data, loading } = useApiData(`lesson:${lessonId}`, () => loadLesson(lessonId));
  useLessonActivity(data?.lesson.id);
  const [activeTab, setActiveTab] = useState("vocabulary");
  const [playingWord, setPlayingWord] = useState(null);

  const speakArabic = (text) => {
    if (!window.speechSynthesis) return;
    setPlayingWord(text);
    const utt = new SpeechSynthesisUtterance(text);
    utt.lang = "ar-SA"; utt.rate = 0.85;
    utt.onend = () => setPlayingWord(null);
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utt);
  };

  // Back always leads to the lessons of this lesson's unit, also when the page
  // was opened from a link and there is no history to go back to.
  const unit = data ? units.find(u => u.id === data.lesson.unit_id) : null;
  const goBack = () => { if (unit) selectUnit(unit); navigate(
    student?.is_teacher || student?.is_admin ? "/content" : "/lessons"); };

  if (loading) return (
    <div style={{display:"flex",alignItems:"center",justifyContent:"center",height:"60vh",color:"#888",fontFamily:"sans-serif"}}>
      جارٍ تحميل الدرس...
    </div>
  );

  if (!data) return (
    <div style={{display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center",height:"60vh",gap:"1rem"}}>
      <p style={{color:"#c0392b"}}>تعذّر تحميل الدرس</p>
      <button onClick={goBack} style={{padding:"0.5rem 1rem",cursor:"pointer"}}>← العودة</button>
    </div>
  );

  const { lesson, words, dialogues } = data;
  const hasContent = lesson.content_ar || lesson.grammar_focus || dialogues.length > 0;

  return (
    <div style={{minHeight:"100vh",background:"#F5F0E8",fontFamily:"'Segoe UI','Noto Sans Arabic',sans-serif",direction:"rtl"}}>
      <header style={{background:"#1a2744",color:"#F5F0E8",padding:"1rem 1.5rem",display:"flex",alignItems:"center",gap:"1rem",borderBottom:"2px solid #C9A84C"}}>
        <button onClick={goBack} style={{background:"rgba(255,255,255,0.1)",border:"1px solid rgba(255,255,255,0.2)",color:"#F5F0E8",borderRadius:"8px",padding:"0.5rem 1rem",cursor:"pointer",fontSize:"14px"}}>
          ← العودة
        </button>
        <div style={{flex:1,textAlign:"center"}}>
          <span style={{fontSize:"11px",letterSpacing:"1px",color:"#C9A84C",display:"block"}}>{unit?.title_ar}</span>
          <h1 style={{margin:0,fontSize:"22px",fontFamily:"'Amiri',serif",color:"#F5F0E8"}}>{lesson.title_ar}</h1>
          {lesson.title_tr && <p style={{margin:"2px 0 0",fontSize:"12px",color:"rgba(245,240,232,0.6)"}}>{lesson.title_tr}</p>}
        </div>
      </header>

      <div style={{display:"flex",background:"#fff",borderBottom:"1px solid #e0d8cc",padding:"0 1.5rem"}}>
        {TABS.map(tab => (
          <button key={tab.key} onClick={() => setActiveTab(tab.key)} style={{
            background:"none",border:"none",padding:"0.875rem 1.25rem",fontSize:"15px",cursor:"pointer",
            borderBottom:activeTab===tab.key?"3px solid #C9A84C":"3px solid transparent",
            color:activeTab===tab.key?"#1a2744":"#888",
            fontWeight:activeTab===tab.key?"700":"400",fontFamily:"inherit"
          }}>{tab.label}</button>
        ))}
      </div>

      <main style={{padding:"1.5rem",maxWidth:"900px",margin:"0 auto"}}>
        {activeTab==="vocabulary" && (
          <div style={{display:"flex",flexDirection:"column",gap:"0.5rem"}}>
            {!words.length && <p style={{textAlign:"center",color:"#aaa",padding:"2rem"}}>لا توجد مفردات</p>}
            {words.map(w => (
              <div key={w.id} style={{background:"#fff",borderRadius:"12px",padding:"0.875rem 1.25rem",display:"flex",justifyContent:"space-between",alignItems:"center",border:"1px solid #e8e0d0"}}>
                <div style={{display:"flex",alignItems:"center",gap:"0.75rem"}}>
                  <button onClick={() => speakArabic(w.word_ar)} style={{
                    background:playingWord===w.word_ar?"#1a2744":"none",
                    border:"1px solid #d0c5b0",borderRadius:"50%",width:"32px",height:"32px",
                    cursor:"pointer",fontSize:"13px",color:playingWord===w.word_ar?"#C9A84C":"#888"
                  }}>{playingWord===w.word_ar?"🔊":"▶"}</button>
                  <span style={{fontSize:"22px",color:"#1a2744",fontFamily:"'Amiri',serif"}}>{w.word_ar}</span>
                </div>
                <div style={{display:"flex",flexDirection:"column",alignItems:"flex-end",gap:"2px"}}>
                  <span style={{fontSize:"15px",color:"#444"}}>{w.translation_tr}</span>
                  {w.translation_en && <span style={{fontSize:"12px",color:"#999"}}>{w.translation_en}</span>}
                </div>
              </div>
            ))}
          </div>
        )}
        {activeTab==="content" && (
          <div style={{background:"#fff",borderRadius:"14px",padding:"1.5rem",border:"1px solid #e8e0d0",lineHeight:"1.8",fontSize:"16px",color:"#333"}}>
            {!hasContent && <p style={{color:"#aaa",textAlign:"center"}}>لا يوجد محتوى</p>}
            {/* Shown as plain text: lesson text is never interpreted as HTML */}
            {lesson.content_ar && <p style={{whiteSpace:"pre-wrap",marginBottom:"1rem"}}>{lesson.content_ar}</p>}
            {lesson.grammar_focus && <GrammarRules grammarFocus={lesson.grammar_focus} />}
            {dialogues.length > 0 && <DialogueScript dialogues={dialogues} unitNumber={unit?.unit_number} />}
          </div>
        )}
        {activeTab==="exercises" && (
          <div style={{textAlign:"center",padding:"3rem",color:"#aaa"}}>
            {student?.is_teacher || student?.is_admin ? <button
              onClick={() => { if (unit) selectUnit(unit); navigate("/content?tab=exercises"); }}
              style={{padding:"10px 18px",borderRadius:8,border:"1px solid #e8e0d0",background:"#fff",color:"#1a2744",cursor:"pointer"}}>
              معاينة تمارين الوحدة
            </button> : <><div style={{fontSize:"40px"}}>🚧</div><p>التمارين قيد التطوير</p></>}
          </div>
        )}
      </main>
    </div>
  );
}
