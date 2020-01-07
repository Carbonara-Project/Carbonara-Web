<template>
<div class="row">
    <div class="col s12">
        <h4 class="category">Pending analyses</h4>
        <ul class="collection pending">
            <li class="collection-item" v-for="(t, _, index) in mPendingTransactions" :key="index">
                 <i class="material-icons left">autorenew</i>
                 <span class="filename">{{ t.filename }}</span>
                 <span class="new badge custom" data-badge-caption="">MD5:</span>
                 <span class="md5"> {{ t.md5 }} </span>
            </li>
            <li v-if="mPendingTransactions.length == 0">No analysis pending</li>
        </ul>

        <h4 class="category">Completed analyses</h4>
        <ul class="collection completed">
            <li class="collection-item" v-for="(t, _, index) in mCompletedTransactions" :key="index">
                 <i class="material-icons left">done</i>
                 <span class="filename">{{ t.filename }}</span>
                 <span class="new badge custom" data-badge-caption="">MD5:</span>
                 <span class="md5">
                     <router-link :to="'/binary/' + t.md5"> {{ t.md5 }}</router-link>
                 </span>
            </li>
            <li v-if="mCompletedTransactions.length == 0">No analysis completed</li>
        </ul>

        <h4 class="category">Failed analyses</h4>
        <ul class="collection failed">
            <li class="collection-item" v-for="(t, _, index) in mFailedTransactions" :key="index">
                 <i class="material-icons left">clear</i>
                 <span class="filename">{{ t.filename }}</span>
                 <span class="new badge custom" data-badge-caption="">MD5:</span>
                 <span class="md5"> {{ t.md5 }} </span>
            </li>
            <li v-if="mFailedTransactions.length == 0">No analysis failed</li>
        </ul>
    </div>
</div>
</template>

<script>

    import utils from '../../utils'

    var LIMIT = 8;

    export default {
        name: 'transactions',
        props: ['transactions'],
        computed: {
            mPendingTransactions() {
                let placeholder = []
                if (this.transactions != undefined) {
                    let pendingTransactions = this.transactions.filter(t => t.completed === false);
                    return utils.uniqueTransactions(pendingTransactions, LIMIT);
                }
                else 
                    return placeholder
            },
            mCompletedTransactions() {
                let placeholder = []
                if (this.transactions != undefined) {
                    let completedTransactions = this.transactions.filter(t => t.completed === true && t.failed === false);
                    return utils.uniqueTransactions(completedTransactions, LIMIT);
                }
                else 
                    return placeholder
            },
            mFailedTransactions() {
                let placeholder = []
                if (this.transactions != undefined) {
                    let failedTransactions = this.transactions.filter(t => t.failed === true);
                    return utils.uniqueTransactions(failedTransactions, LIMIT);
                }
                else 
                    return placeholder
            }
        }
    }
</script>

<style lang="scss" scoped>

.custom {
    background-color: #efefef !important;
    color: #000000 !important;
}

.category{
    color: #00838f;
}

.collection {
    &.completed{
        i { color: green; }
    }
    &.failed {
        i { color: red; }
    }

    .collection-item {
        display: flex;
        align-items: center;
        
        .filename {
            margin-left: 8px;
            width: 150px;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .md5 {
            margin-left: 8px;
        }
    }
}
</style>
