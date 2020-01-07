import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

import pubnub from './pubnub'

const MAX_NOTIFICATIONS = 10

const store = new Vuex.Store({
    state: {
        // This refers to the visited user, all infos about current user are held in localStorage
        User: {
            username: ""
        },
        VisitedUser: {
            username: "",
            first_name: "",
            last_name: "",
            bio: "",
            profile_image: "",
        },
        breadcrumbs: [],
        Binary: {},
        BinaryCommentList: [],
        MD5SearchResult: [],
        NameSearchResult: [],
        ProcDescs: [],
        SelectedProcDesc: {},
        ProcDescCommentList: [],
        ProcSimilar: [],
        UserTransactions: [],
        NotificationList: [],
        NotificationAlerts: 0
    },
    mutations: {
        // User related commits
        login: (state, payload) => {
            state.User.username = payload.username
            localStorage.setItem('username', payload.username)

            localStorage.setItem('access_token', payload.access_token)
            localStorage.setItem('logged_in', true)

            pubnub.login(payload.username)
        },
        logout: (state) => {
            pubnub.logout(localStorage.getItem('username'))
            state.NotificationList = []

            state.User.username = ""
            localStorage.removeItem('username')

            localStorage.removeItem('access_token')
            localStorage.removeItem('logged_in')
        },

        loadUserInfo: (state, payload) => {
            state.VisitedUser = payload;
            state.VisitedUser.username = payload.email;
        },
        updateProfileInfo: (state, payload) =>{
            state.VisitedUser.first_name = payload.first_name;
            state.VisitedUser.last_name = payload.last_name;
            state.VisitedUser.bio = payload.bio;
        },
        updateProfileImage: (state, payload) =>{
            state.VisitedUser.profile_image = payload.profile_image;
        },
        

        // Breadcrumbs
        updateBreadcrumbs: (state, payload) => {
            state.breadcrumbs = payload.breadcrumbs;
        },

        // Binary
        loadBinary: (state, payload) => {
            state.Binary = payload
        },
        loadBinaryCommentList: (state, payload) => {
            state.BinaryCommentList = payload
        },
        updateOwnBinaryComment: (state, payload) => {
            if (state.BinaryCommentList.length == 0) {
                state.BinaryCommentList = [{
                    text: payload.text,
                    md5: payload.md5,
                    user: state.User.username
                }]
            } else {
                for (let i in state.BinaryCommentList) {
                    if (state.BinaryCommentList[i].user === state.User.username)
                        state.BinaryCommentList[i].text = payload.text
                }
            }
        },
        removeOwnBinaryComment: (state, payload) => {
            for (const i in state.BinaryCommentList) {
                const comment = state.BinaryCommentList[i];
                if (comment.user === state.User.username)
                    state.BinaryCommentList.splice(i, 1)
            }
        },
        loadMD5SearchResult: (state, payload) => {
            state.MD5SearchResult = payload
        },
        loadNameSearchResult: (state, payload) => {
            state.NameSearchResult = payload
        },

        // Procedures
        loadProcDescList: (state, payload) => {
            state.ProcDescs = payload
        },
        updateSelectedProcDesc: (state, payload) => {
            state.SelectedProcDesc = payload
        },
        loadProcDescCommentList: (state, payload) => {
            state.ProcDescCommentList = payload
        },
        updateOwnComment: (state, payload) => {
            if (state.ProcDescCommentList.length == 0) {
                state.ProcDescCommentList = [{
                    comment: payload.comment,
                    procedure_desc: payload.procedure_desc,
                    user: state.User.username
                }]
            } else {
                for (let i in state.ProcDescCommentList) {
                    if (state.ProcDescCommentList[i].user === state.User.username)
                        state.ProcDescCommentList[i].comment = payload.comment
                }
            }
        },

        // Votes
        makeUpvote: (state, payload) => {
            let procDescID = payload.procDescID
            for (let i = 0; i < state.ProcDescs.length; i++) {
                const e = state.ProcDescs[i];
                if (e.id == procDescID) {
                    if (e.ownVote === 'downvote')
                        e.downvotes -= 1

                    e.ownVote = 'upvote'
                    e.upvotes += 1
                }
            }
        },
        makeDownvote: (state, payload) => {
            let procDescID = payload.procDescID
            for (let i = 0; i < state.ProcDescs.length; i++) {
                const e = state.ProcDescs[i];
                if (e.id == procDescID) {
                    if (e.ownVote === 'upvote')
                        e.upvotes -= 1

                    e.ownVote = 'downvote'
                    e.downvotes += 1
                }
            }
        },
        removeOwnUpvote: (state, payload) => {
            let procDescID = payload.procDescID
            for (let i = 0; i < state.ProcDescs.length; i++) {
                const e = state.ProcDescs[i];
                if (e.id == procDescID) {
                    e.ownVote = ""
                    e.upvotes -= 1
                }
            }
        },
        removeOwnDownvote: (state, payload) => {
            let procDescID = payload.procDescID
            for (let i = 0; i < state.ProcDescs.length; i++) {
                const e = state.ProcDescs[i];
                if (e.id == procDescID) {
                    e.ownVote = ""
                    e.downvotes -= 1
                }
            }

        },

        loadProcSimilar: (state, payload) => {
            state.ProcSimilar = payload
        },

        // AnalysisTransactions
        loadUserTransactions: (state, payload) => {
            state.UserTransactions = payload
        },

        // Notifications
        loadNotificationList: (state, payload) => {
            state.NotificationList = state.NotificationList.concat(payload)
        },
        loadNotification: (state, payload) => {
            // if too much elements remove the first element pushed
            if (state.NotificationList.length > MAX_NOTIFICATIONS)
                state.NotificationList.shift()
            state.NotificationList.unshift(payload)

            // Increase NotificationAlerts counter
            state.NotificationAlerts++
        },
        removeNotification: (state, payload) => {
            state.NotificationList.remove(payload)
        },
        clearNotificationAlerts: (state, payload) => {
            state.NotificationAlerts = 0
        }
    }
})

export default store