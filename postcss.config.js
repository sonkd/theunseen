module.exports = {
    plugins: [
        require('postcss-import')({
            path: ['css'], // Add directories where PostCSS should look for imports
        }),
        require('tailwindcss'),
        require('autoprefixer'),
        require('cssnano')({
            preset: 'default',
        }),
        ...(process.env.JEKYLL_ENV == "production"
            ? [require('cssnano')({ preset: 'default' })]
            : [])
    ],
};