import os, sys
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"C:\Users\SD\Desktop\arabic_platform\frontend\src\pages")

content = open("Exercises.jsx", encoding="utf-8").read()

if "FILTER_OPTIONS" in content:
    print("Already updated!")
else:
    filter_code = """
const FILTER_OPTIONS = [
  { value: 'all',             label: '\u0627\u0644\u0643\u0644' },
  { value: 'multiple_choice', label: '\u0627\u062e\u062a\u064a\u0627\u0631 \u0645\u062a\u0639\u062f\u062f' },
  { value: 'fill_blank',      label: '\u0625\u0643\u0645\u0627\u0644 \u0641\u0631\u0627\u063a' },
  { value: 'true_false',      label: '\u0635\u062d \u0648\u062e\u0637\u0623' },
  { value: 'translate_ar_tr', label: '\u062a\u0631\u062c\u0645\u0629' },
  { value: 'match',           label: '\u0648\u0635\u0644' },
  { value: 'synonym',         label: '\u0645\u062a\u0631\u0627\u062f\u0641\u0627\u062a' },
  { value: 'antonym',         label: '\u0645\u062a\u0639\u0627\u0643\u0633\u0627\u062a' },
  { value: 'plural',          label: '\u0627\u0644\u062c\u0645\u0639' },
  { value: 'comprehension',   label: '\u0627\u0633\u062a\u064a\u0639\u0627\u0628 \u0642\u0631\u0627\u0626\u064a' },
  { value: 'word_order',      label: '\u062a\u0631\u062a\u064a\u0628 \u0643\u0644\u0645\u0627\u062a' },
]

function matchesFilter(exercise, filter) {
  if (filter === 'all') return true
  if (filter === 'synonym')      return exercise.hint_ar === '\u0645\u062a\u0631\u0627\u062f\u0641'
  if (filter === 'antonym')      return exercise.hint_ar === '\u0636\u062f / \u0645\u062a\u0639\u0627\u0643\u0633'
  if (filter === 'plural')       return exercise.hint_ar === '\u062c\u0645\u0639 \u0627\u0644\u0643\u0644\u0645\u0629'
  if (filter === 'comprehension') return exercise.hint_ar === '\u0627\u0633\u062a\u064a\u0639\u0627\u0628 \u0642\u0631\u0627\u0626\u064a'
  if (filter === 'word_order')   return exercise.question_ar && exercise.question_ar.includes('\u0631\u064e\u062a\u0651\u0650\u0628')
  return exercise.exercise_type === filter
}
"""
    content = content.replace("export default function Exercises()", filter_code + "\nexport default function Exercises()")
    open("Exercises.jsx", "w", encoding="utf-8").write(content)
    print("Done!")
