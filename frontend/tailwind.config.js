/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'risk-low': '#3F7A4D',
        'risk-low-bg': '#E7F0E8',
        'risk-medium': '#B5760C',
        'risk-medium-bg': '#FBEEDA',
        'risk-high': '#B33A2E',
        'risk-high-bg': '#FBE6E2',
        'needs-review': '#5B4FBA',
        'needs-review-bg': '#EDE8F5',
      },
      fontFamily: {
        'document': ['Source Serif 4', 'Georgia', 'serif'],
        'ui': ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}