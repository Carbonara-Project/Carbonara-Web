<template>
<div class="row">
    <div class="col s12 m6">
        <h4>Descriptions</h4>
        <ul id="proc-desc-list-accordion" class="collapsible" data-collapsible="accordion">
            <li v-for="(desc, i) in mProcDescs" v-bind:key="i" 
                :data-id="desc.id" 
                @click="procDescSelection(desc.id)">
                <div class="collapsible-header row">
                         <div class="col s2">
                             <div class="upvotes-container">
                                 <span class="upvotes-counter">{{ desc.upvotes }}</span>
                                  <i :class="{active: hasOwnUpvote(desc.id)}" @click="sendUpvote(desc.id, $event)" class="material-icons">arrow_upward</i>
                             </div>
                             <div class="downvotes-container">
                                 <span class="downvotes-counter">{{ desc.downvotes }}</span>
                                  <i :class="{active: hasOwnDownvote(desc.id)}" @click="sendDownvote(desc.id, $event)" class="material-icons">arrow_downward</i>
                             </div>
                         </div>
                         <div class="row col s10">
                            <div class="col s12"><user-badge :email="desc.user"></user-badge></div>
                            <div class="col s12">
                                <p class="description">
                                    {{ desc.description }}
                                </p>
                            </div>
                         </div>
                </div>
                <div class="collapsible-body">
                    <div class="comments">
                        <h5>Comments</h5>
                        <proc-desc-comment-list
                            class="proc-desc-comment-list"
                            :procDescID="desc.id"
                            :isSelected="selectedProcDescID == desc.id"
                        >                        
                        </proc-desc-comment-list>
                    </div>
                </div>
            </li>
        </ul>
    </div>
</div>  
</template>
<script>
import api from '../../api/api'
import ProcDescCommentList from './ProcDescCommentList'
import UserBadge from '../User/UserBadge'

export default {
    name: 'proc-desc-list',
    components: {
        ProcDescCommentList,
        UserBadge
    },
    props: ['procDescs'],
    data() {
        return {
            selectedProcDescID: -1,
            isOpenAccordion: false
        }
    },
    computed: {
        mProcDescs() {
            return this.procDescs || []
        }
    },
    methods: {
        isFirst(i) { return !i },
        procDescSelection(id) {
            this.selectedProcDescID = id
            this.$emit('procDescSelection', this.selectedProcDescID)
            api.procedureDescCommentList(this.selectedProcDescID)
        },
        hasOwnUpvote(procDescID) {
            for (let i = 0; i < this.$store.state.ProcDescs.length; i++) {
                const e = this.$store.state.ProcDescs[i];
                if (e.id == procDescID) return e.ownVote === 'upvote'
            }
            return false
        },
        hasOwnDownvote(procDescID) {
            for (let i = 0; i < this.$store.state.ProcDescs.length; i++) {
                const e = this.$store.state.ProcDescs[i];
                if (e.id == procDescID) return e.ownVote === 'downvote'
            }
            return false
        },
        sendUpvote(procDescID, event) {
            event.stopPropagation()
            let hasOwnUpvote = this.hasOwnUpvote(procDescID)
            if (hasOwnUpvote) {
                this.$store.commit('removeOwnUpvote', { procDescID: procDescID })
                api.removeOwnVote(procDescID, 'upvote')
            } else {
                this.$store.commit('makeUpvote', { procDescID: procDescID })
                api.makeVote(procDescID, 'upvote')
            }
        },
        sendDownvote(procDescID, event) {
            event.stopPropagation()
            let hasOwnDownvote = this.hasOwnDownvote(procDescID)
            if (hasOwnDownvote) {
                this.$store.commit('removeOwnDownvote', { procDescID: procDescID })
                api.removeOwnVote(procDescID, 'downvote')
            } else {
                this.$store.commit('makeDownvote', { procDescID: procDescID })
                api.makeVote(procDescID, 'downvote')
            }
        }
    },
    mounted() {
        $('#proc-desc-list-accordion').collapsible();
    }
}
</script>
<style lang="scss" scoped>
#proc-desc-list-accordion {
    .collapsible-header {
        margin: 0;
        padding-top: 1.5rem;
        transition: background-color .3s ease-in-out,
                    color .3s ease-in-out;

        p.description {
            font-size: 1.2em;
            line-height: 1.2;
        }

        .upvotes-container,
        .downvotes-container {
            display: flex;
            justify-content: space-evenly;
            align-content: center;
            padding-top: 8px;
            padding-bottom: 8px;
        }
        // To be aligned with user-badge
        .upvotes-container { padding-top: 0; }
        .upvotes-container i.active,
        .downvotes-container i.active {
            font-weight: bold;
        }
        .upvotes-container i { color: #8BC34A; }
        .downvotes-container i { color: #FF5722; }
    }
}
.comments {
    h5 {
        font-size: 1.5em;
    }

    .proc-desc-comment-list {
        margin-left: 32px;
    }
}
</style>
