import pako from 'pako'

function inflate(data) {
    try {
        var result = pako.inflate(data);
        return result;
    } catch (error) {
        console.log(error);
    }
}