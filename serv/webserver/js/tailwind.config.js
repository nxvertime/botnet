/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
            "./src/**/*.{html,js}", 
            "../*.html"
            // Ajoutez d'autres types de fichiers si nécessaire
          ],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Poppins', 'sans-serif']
      }

    },
  },
  plugins: [

  ],
}
