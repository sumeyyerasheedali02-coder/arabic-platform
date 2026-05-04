/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        amiri:  ['Amiri', 'serif'],
        dm:     ['DM Sans', 'sans-serif'],
      },
      colors: {
        navy:  {
          DEFAULT: '#0F2044',
          2:       '#162a55',
          3:       '#1e3a6e',
        },
        gold:  {
          DEFAULT: '#C9A84C',
          2:       '#e2c06a',
          light:   '#FAEEDA',
        },
        cream: {
          DEFAULT: '#F8F6F1',
          2:       '#EFECe4',
          border:  '#e5e0d5',
        },
        unit: {
          1: '#1D9E75',
          2: '#185FA5',
          3: '#854F0B',
          4: '#712B13',
          5: '#3C3489',
        },
      },
      animation: {
        'fade-in':  'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
      keyframes: {
        fadeIn:  { from: { opacity: '0' },                               to: { opacity: '1' } },
        slideUp: { from: { opacity: '0', transform: 'translateY(12px)' }, to: { opacity: '1', transform: 'translateY(0)' } },
      },
    },
  },
  plugins: [],
}
