main_app.directive('resultItem', ()=>{
    return {
        'restrict': 'E',
        'scope': {
            'item_title': '=itemTitle',
            'item_url': '=itemUrl',
        },
        'template': `
            <div class='result-item normal-item'>
                <span class='title'>{{ item_title }}</span>
                <a class='link' target='_blank' href='{{ item_url }}'>{{ item_url }}</a>
            </div>`,
        'replace': true
    };
})

