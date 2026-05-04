import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

const API = "http://localhost:8003";

export default function LessonDetail() {
  const { lessonId } = useParams();
  const navigate = useNavigate();
  const [lesson, setLesson] = useState(null);
  const [activeTab, setActiveTab] = useState("vocabulary");
  const [loading, setLoading] = useState(true);
  const [playingWord, setPlayingWord] = useState(null);
  const token = localStorage.getItem("token");

  useEffect(() => {
    fetch(`${API}/lessons/${lessonId}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(r => r.json())
      .then(data => { setLesson(data); setLoading(false); })
      .catch(() => setLoading(false));
  }, [lessonId]);

  const speakArabic = (text) => {
    if (!window.speechSynthesis) return;
    setPlayingWord(text);
    const utt = new SpeechSynthesisUtterance(text);
    utt.lang = "ar-SA"; utt.rate = 0.85;
    utt.onend = () => setPlayingWord(null);
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utt);
  };

  if (loading) return (
    <div style={{display:"flex",alignItems:"center",justifyContent:"center",height:"60vh",color:"#888",fontFamily:"sans-serif"}}>
      جارٍ تحميل الدرس...
    </div>
  );

  if (!lesson) return (
    <div style={{display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center",height:"60vh",gap:"1rem"}}>
      <p style={{color:"#c0392b"}}>تعذّر تحميل الدرس</p>
      <button onClick={() => navigate(-1)} style={{padding:"0.5rem 1rem",cursor:"pointer"}}>← العودة</button>
    </div>
  );

  return (
    <div style={{minHeight:"100vh",background:"#F5F0E8",fontFamily:"'Segoe UI','Noto Sans Arabic',sans-serif",direction:"rtl"}}>
      <header style={{background:"#1a2744",color:"#F5F0E8",padding:"1rem 1.5rem",display:"flex",alignItems:"center",gap:"1rem",borderBottom:"2px solid #C9A84C"}}>
        <button onClick={() => navigate(-1)} style={{background:"rgba(255,255,255,0.1)",border:"1px solid rgba(255,255,255,0.2)",color:"#F5F0E8",borderRadius:"8px",padding:"0.5rem 1rem",cursor:"pointer",fontSize:"14px"}}>
          ← العودة
        </button>
        <div style={{flex:1,textAlign:"center"}}>
          <span style={{fontSize:"11px",letterSpacing:"1px",color:"#C9A84C",display:"block"}}>{lesson.unit_title}</span>
          <h1 style={{margin:0,fontSize:"22px",fontFamily:"'Amiri',serif",color:"#F5F0E8"}}>{lesson.title}</h1>
          {lesson.title_tr && <p style={{margin:"2px 0 0",fontSize:"12px",color:"rgba(245,240,232,0.6)"}}>{lesson.title_tr}</p>}
        </div>
      </header>

      <div style={{display:"flex",background:"#fff",borderBottom:"1px solid #e0d8cc",padding:"0 1.5rem"}}>
        {[{key:"vocabulary",label:"المفردات"},{key:"content",label:"الدرس"},{key:"exercises",label:"التمارين"}].map(tab => (
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
            {!(lesson.vocabulary||[]).length && <p style={{textAlign:"center",color:"#aaa",padding:"2rem"}}>لا توجد مفردات</p>}
            {(lesson.vocabulary||[]).map((w,i) => (
              <div key={i} style={{background:"#fff",borderRadius:"12px",padding:"0.875rem 1.25rem",display:"flex",justifyContent:"space-between",alignItems:"center",border:"1px solid #e8e0d0"}}>
                <div style={{display:"flex",alignItems:"center",gap:"0.75rem"}}>
                  <button onClick={() => speakArabic(w.arabic)} style={{
                    background:playingWord===w.arabic?"#1a2744":"none",
                    border:"1px solid #d0c5b0",borderRadius:"50%",width:"32px",height:"32px",
                    cursor:"pointer",fontSize:"13px",color:playingWord===w.arabic?"#C9A84C":"#888"
                  }}>{playingWord===w.arabic?"🔊":"▶"}</button>
                  <span style={{fontSize:"22px",color:"#1a2744",fontFamily:"'Amiri',serif"}}>{w.arabic}</span>
                </div>
                <div style={{display:"flex",flexDirection:"column",alignItems:"flex-end",gap:"2px"}}>
                  <span style={{fontSize:"15px",color:"#444"}}>{w.turkish}</span>
                  {w.english && <span style={{fontSize:"12px",color:"#999"}}>{w.english}</span>}
                </div>
              </div>
            ))}
          </div>
        )}
        {activeTab==="content" && (
          <div style={{background:"#fff",borderRadius:"14px",padding:"1.5rem",border:"1px solid #e8e0d0",lineHeight:"1.8",fontSize:"16px",color:"#333"}}
            dangerouslySetInnerHTML={{__html:lesson.content||"<p style='color:#aaa;text-align:center'>لا يوجد محتوى</p>"}} />
        )}
        {activeTab==="exercises" && (
          <div style={{textAlign:"center",padding:"3rem",color:"#aaa"}}>
            <div style={{fontSize:"40px"}}>🚧</div>
            <p>التمارين قيد التطوير</p>
          </div>
        )}
      </main>
    </div>
  );
}