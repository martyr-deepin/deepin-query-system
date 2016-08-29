// parse JSON data for angular http service
export function parse_resp(resp){
    return resp.data;
}

export function clipboard(text){
    const ta = document.createElement('textarea');

    // out of sreen
    ta.style.top = '111vh';
    ta.style.left = '111vw';

    ta.style.width = '2em';
    ta.style.height = '2em';

    ta.value = text;
    document.body.appendChild(ta);
    ta.select();

    try{
        document.execCommand('copy');
    } catch(e){
        console.log('unable to copy --');
        return false;
    }

    document.body.removeChild(ta);

    return true;
}
