/** @type {import('tailwindcss').Config} */
export default {
  content: [],
  theme: {
    extend: {
      fontFamily: {
        'paratype': ['Paratype Biform', 'sans-serif'],
      },
      colors: {
        'custom-yellow': '#FD9968',
        'custom-blue': '#989BFE',
        'custom-card': '#2B3442'
      },
      backgroundImage: {
        'custom-gradient': 'linear-gradient(to right, #FD9968, #989BFE)'
      },
    },
  },
  plugins: [],
} 