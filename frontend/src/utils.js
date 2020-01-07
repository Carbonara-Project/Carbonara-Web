import qs from 'query-string'

function objectToList(object){
    let l = [];
    for (let key in object) {
        let value = object[key];
        let tmp = {md5: key, name: value}
        l.push(tmp)
    }
    return l;
}

function uniqueTransactions(transactions, maxLength) {
    let unique = [];
    let keys = [];
    for (let index in transactions) {
        let transaction = transactions[transactions.length - index - 1];
        if (keys.indexOf(transaction.md5) === -1 && unique.length < maxLength) {
            unique.push(transaction);
            keys.push(transaction.md5);
        }
    }
    return unique;
}

function createLinkForVote(msg) {
    return '/binary/' + msg.binary_md5 + '/' + msg.procedure_offset
}

function createContentForVote(msg) {
    return `${msg.by} ${msg.action}d your description`
}

export default {
    objectToList,
    uniqueTransactions,
    createLinkForVote,
    createContentForVote
}