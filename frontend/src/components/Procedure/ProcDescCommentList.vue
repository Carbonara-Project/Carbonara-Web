<template>
  <div class="row">
      <ul class="col s12" v-if="comments.length > 0">
        <li class="collection-item col s12 card comment-li" v-for="(comment, _, i) in comments" :key="i">
            <router-link class="user-comment" :to="'/user/' + comment.user">
                {{ comment.user }}
            </router-link>
            <div style="margin-top:5px" class="divider"></div>
            <p>{{ comment.comment }}</p>
        </li>
      </ul>
      <div class="own-comment-container col s12">
          <form @submit="sendComment" class="row">
              <i class="col s1 edit-button material-icons tiny" 
                v-if="ownComment && !editing" 
                @click="activateEditing"
              >edit</i>
              <p class="card col s11" v-if="ownComment && !editing">{{ ownComment }}</p>
              
              <textarea v-if="editing || !ownComment" v-model="comment" class="materialize-textarea col s9"></textarea>
              <button v-if="editing || !ownComment" class="col s3 btn-flat waves-effect waves-light valign-wrapper" type="submit" name="action">Comment</button>
          </form>
      </div>
  </div>
</template>
<script>
import api from '../../api/api'

export default {
    name: 'proc-desc-comment-list',
    props: ['procDescID', 'isSelected'],
    data() {
        return {
            comment: "",
            editing: false
        }
    },
    computed: {
        comments() {
            // Filter out user's own comment
            if (this.$store.state.ProcDescCommentList == undefined) return []
            
            let commentList = []
            for (let i = 0; i < this.$store.state.ProcDescCommentList.length; i++) {
                const element = this.$store.state.ProcDescCommentList[i];
                if (element.user !== this.$store.state.User.username)
                    commentList.push(element)
            }
            return commentList
        },
        ownComment() {
            if (!this.isSelected) return
            let commentList = this.$store.state.ProcDescCommentList
            // Filter out user's own comment
            if (commentList == undefined) return {}
            for (let i in commentList) {
                if (commentList[i].user == this.$store.state.User.username) {
                    return commentList[i].comment
                }
            }
            return undefined
        }
    },
    methods: {
        activateEditing() { 
            this.comment = this.ownComment || ""
            this.editing = true 
        },
        sendComment(event) {
            event.preventDefault();
            let _this = this
            api.sendProcedureDescComment(this.procDescID, this.comment)
            .then(function(res) {
                console.debug(res)
                _this.editing = false
                _this.$store.commit('updateOwnComment', {
                    comment: _this.comment,
                    procedure_desc: _this.procDescID
                })
            })
            .catch(function(err) {
                console.log(err)
                console.log(err.response)
            })
        }
    }
}
</script>
<style lang="scss" scoped>
.collection {
    padding: 0;

    border: 1px solid #BDBDBD;
  .collection-item {
      border-color: #BDBDBD;
      background-color: rgb(247, 249, 248);
      p {
          white-space: pre-line;
      }
  }
}

.comment-li{
        padding-top:5px;
}

.user-comment{
    font-weight: lighter;
}

.collection-item>a{
    color:#26a69a;
}

.own-comment-container { 
    padding: 0 .75rem;
    
    form {
        display: flex;
        align-items: center;
        margin-top: 32px;

        .edit-button {
            cursor: pointer;
        }

        p {
            margin-top: 0;
            padding: 4px;
            white-space: pre-line;
        }
        
        button {
            margin-left: 3px;
        }
    }
}

</style>
