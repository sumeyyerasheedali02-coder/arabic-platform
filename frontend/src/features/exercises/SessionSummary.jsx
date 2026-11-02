/** Summary belongs to this saved session; replaying feedback does not award points. */
export default function SessionSummary({ total, correctCount, pct, totalPoints, isGuest, onRestart, onMistakes, onBack, busy }) {
  return (
    <section className="practice-summary">
      <div className="practice-summary-mark" aria-hidden="true">✓</div>
      <span className="practice-eyebrow">اكتملت جلسة التدريب</span>
      <h2>{correctCount === total ? 'أحسنت، كل الإجابات صحيحة' : 'خطوة أخرى في تعلّمك'}</h2>
      <p>يمكنك مراجعة أخطائك أو اختيار تدريب آخر.</p>
      <div className="practice-summary-stats">
        <div><strong>{total}</strong><span>سؤال</span></div>
        <div><strong>{correctCount}</strong><span>إجابة صحيحة</span></div>
        <div><strong dir="ltr">{pct}%</strong><span>نسبة النجاح</span></div>
      </div>
      {!isGuest && <p>نقاط هذه الجلسة: <strong>{totalPoints}</strong></p>}
      <div className="practice-summary-actions">
        {correctCount < total && <button className="practice-button practice-primary" onClick={onMistakes} disabled={busy}>إعادة الأخطاء فقط</button>}
        <button className="practice-button practice-secondary" onClick={onRestart} disabled={busy}>البدء من البداية</button>
        <button className="practice-text-button" onClick={onBack} disabled={busy}>اختيار تدريب آخر</button>
      </div>
    </section>
  )
}
