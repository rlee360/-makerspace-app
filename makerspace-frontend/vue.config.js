module.exports = {
    pages: {
        'index': {
            entry: 'public/main.js',
            template: 'public/index.html',
            filename: process.env.NODE_ENV === 'production' ? 'build/path/index.html' : 'index.html',
            title: 'Makerspace Management Tool',
            chunks: ['chunk-vendors', 'chunk-common', 'index']
        },
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
        'job': {
            entry: './src/pages/job/main.js',
            template: 'src/pages/job/job.html',
            filename: 'job.html',
            title: 'Job View',
            chunks: ['chunk-vendors', 'chunk-common', 'job']
        },
        'material': {
            entry: './src/pages/material/main.js',
            template: 'src/pages/material/material.html',
            filename: 'material.html',
            title: 'Material View',
            chunks: ['chunk-vendors', 'chunk-common', 'material']
        },
        'testing': {
            entry: './src/pages/testing/main.js',
            template: 'src/pages/testing/testing.html',
            filename: 'testing.html',
            title: 'Testing View',
            chunks: ['chunk-vendors', 'chunk-common', 'testing']
        },
    }
}

