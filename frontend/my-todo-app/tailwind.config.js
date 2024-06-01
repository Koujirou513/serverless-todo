/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      screens: {
        'lg': '1540',
      },
      colors: {
        'gray': '#D9D9D9',
        'title-gray': '#6C6C6C',
        'blue': '#1DA0D9',
        'btn_green': '#1DD9A0',
        'red': '#E20E0E',
        'white': '#FFFFFF',
        'pink': '#F26060',
        'green': '#4D9902',
        'yellow': '#D9BB1D',
        'smoke': '#F0F0F0',
        'black': '#000000',
        
      },
      fontFamily: {
        'Georgia': 'Georgia',
        'life': 'Love Ya Like Sister'
      }
    },
  },
  plugins: [],
}

