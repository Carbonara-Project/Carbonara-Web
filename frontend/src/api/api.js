import qs from 'query-string'

import axiosClients from './axiosClients'
import store from '../store'
import router from '../router'
import utils from '../utils'

const normalAxios = axiosClients.normalAxios
const anonymousAxios = axiosClients.anonymousAxios

function programInfo(md5) {
  normalAxios({
    method: 'GET',
    url: '/api/program/',
    params: {
      md5: md5,
      type: 'info'
    }
  })
  .then(function(res) {
    store.commit('loadBinary', res.data)
  })
  .catch(function(err) {
    console.log(err)
    console.log(err.response)
  })
}

function searchProgramBy(query, by) {
  normalAxios({
    method: 'GET',
    url: '/api/program/',
    params: {
      query: query,
      by: by,
      type: 'search'
    }
  })
  .then(function(res) {
      if (by === 'md5')
        store.commit('loadMD5SearchResult', res.data);
      else 
        store.commit('loadNameSearchResult', res.data);
  })
  .catch(function(err) {
    console.log(err)
    console.log(err.response)
  })
}

function sendProgramComment(md5, comment) {
  return normalAxios({
    method: 'POST',
    url: '/api/program/' + md5 + '/comments/',
    data: {
      md5: md5,
      text: comment
    }
  })
}

function removeProgramComment(md5) {
  return normalAxios({
    method: 'DELETE',
    url: '/api/program/' + md5 + '/comments/',
  })
}

function programCommentList(md5) {
  normalAxios({
    method: 'GET',
    url: '/api/program/' + md5 + '/comments/',
  })
  .then(function(res) {
    console.log(res)
    store.commit('loadBinaryCommentList', res.data.comments)
  })
  .catch(function(err) {
    console.log(err)
    console.log(err.response)
  })
}

function procedureDescs(md5, offset) {
  normalAxios({
    method: 'GET',
    url: '/api/procedure/',
    params: {
      md5: md5,
      offset: offset
    }
  })
  .then(function(res) {
    store.commit('loadProcDescList', res.data)
    store.commit('updateSelectedProcDesc', res.data[0])
    procedureSimilar(md5, offset, res.data[0].id)
  })
  .catch(function(err) {
    console.log(err)
    console.log(err.response)
  })
}

function sendProcedureDescComment(procDescID, comment) {
  let req = qs.stringify({
    procedure_desc: procDescID,
    comment: comment
  })
  return normalAxios({
    method: 'POST',
    url: '/api/comment/',
    data: req
  })
}

function procedureDescCommentList(procDescID) {
  normalAxios({
    method: 'GET',
    url: '/api/comment/',
    params: {
      procedure_desc: procDescID
    }
  })
  .then(function(res) {
    store.commit('loadProcDescCommentList', res.data.comments)
  })
  .catch(function(err) {
    console.log(err)
    console.log(err.response)
  })
}

function procedureSimilar(md5, offset, desc_id) {
  normalAxios({
    method: 'GET',
    url: '/api/proc-similar/',
    params: {
      md5: md5,
      offset: offset,
      desc_id: desc_id
    }
  })
  .then(function(res) {
    store.commit('loadProcSimilar', res.data)
  })
  .catch(function(err) {
    console.log(err)
    console.log(err.response)
  })
}

function pendingTransactions() {
  normalAxios({
    method: 'GET',
    url: '/users/transactions/'
  })
  .then(function(res) {
    store.commit('loadUserTransactions', res.data)
  })
  .catch(function(err) {
    console.log(err)
    console.log(err.response)
  })
}

function makeVote(procDescID, vote_type) {
  normalAxios({
    method: 'POST',
    url: '/api/procedure/' + procDescID + '/vote/',
    data: {'vote_type': vote_type}
  })
  .then(function(res) {
    console.log(res)
  })
  .catch(function(err) {
    console.log(err)
    console.log(err.response)    
  })
}

function removeOwnVote(procDescID, vote_type) {
  normalAxios({
    method: 'DELETE',
    url: '/api/procedure/' + procDescID + '/vote/',
    data: {'vote_type': vote_type}
  })
  .then(function(res) {
    console.log(res)
  })
  .catch(function(err) {
    console.log(err)
    console.log(err.response)    
  })
}

export default {
  programInfo,
  programCommentList,
  sendProgramComment,
  removeProgramComment,
  searchProgramBy,
  procedureDescs,
  sendProcedureDescComment,
  procedureDescCommentList,
  procedureSimilar,
  pendingTransactions,
  makeVote,
  removeOwnVote
}