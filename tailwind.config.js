module.exports = {
    content: [
        './_drafts/**/*.{html,md,liquid}',
        './_includes/**/*.{html,md,liquid}',
        './_layouts/**/*.{html,md,liquid}',
        './my_collections/_posts/**/*.{html,md,liquid}', // Add this line
        './_posts/**/*.{html,md,liquid}',
        './_posts/*.html',
        './_pages/*.{html,md,liquid}',
        './_pages/**/*.{html,md,liquid}',
        './assets/css/**/*.js',
        './_data/**/*.yml',
        './*.{md,html,liquid}',
    ],
    theme: {
        extend: {},
        container: {
            center: true,
            // default breakpoints but with 40px removed
            screens: {
            sm: '640px',
            md: '768px',
            lg: '1024px',
            xl: '1024px',
            '2xl': '1024px',
            },
        },
    },
    variants: {
        extend: {},
    },
    plugins: [
    ],
}