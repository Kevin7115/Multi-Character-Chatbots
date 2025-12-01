import Cookie from 'universal-cookie';

export async function getTokenOrRefresh() {
    const cookie = new Cookie();
    try {
        const res = await fetch("/api/speech/get_token_object");            
        const data = await res.json();
        const token = data.token;
        const region = data.region;
        cookie.set('speech-token', region + ':' + token, {maxAge: 540, path: '/'});

        console.log('Token fetched from back-end: ' + token);
        return { authToken: token, region: region };
    } catch (err) {
        console.log(err.response.data);
        return { authToken: null, error: err.response.data };
    }
}