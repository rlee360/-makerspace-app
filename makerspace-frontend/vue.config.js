module.exports = {
    pages: {
        'request': {
            entry: './src/pages/request/main.js',
            template: 'src/pages/request/request.html',
            filename: 'request.html',
            title: 'Makerspace Request Form',
            chunks: ['chunk-vendors', 'chunk-common', 'request']
        },
        'operator': {
            entry: './src/pages/operator/main.js',
            template: 'src/pages/operator/operator.html',
            filename: 'operator.html',
            title: 'Operator View',
            chunks: ['chunk-vendors', 'chunk-common', 'operator']
        },
    }
}

