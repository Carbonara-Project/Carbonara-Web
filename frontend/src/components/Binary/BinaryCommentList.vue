<template>
  <div class="row">
      <ul class="col s12" v-if="comments.length > 0">
        <li class="collection-item col s12 card comment-li" v-for="(comment, _, i) in comments" :key="i">
            <router-link class="user-comment" :to="'/user/' + comment.user">
                <b>{{ comment.user }}</b>
            </router-link>
            <div style="margin-top:5px" class="divider"></div>
            <p>{{ comment.text }}</p>
        </li>
      </ul>
      <div class="own-comment-container col s12">
          <form @submit="sendComment" class="row">
              <div class="orange darken-3 btn btn-floating fixmargin" v-if="ownComment && !editing" 
                @click="activateEditing" title="Edit">
              <i class="material-icons tiny" 
                
              >edit</i></div>
              <div class="red darken-4 btn btn-floating fixmargin" v-if="ownComment && !editing" 
                @click="removeComment" title="Remove">
              <i class="material-icons tiny" 
                
              >delete</i></div>
              <p class="card col s11" v-if="ownComment && !editing"><em>{{ ownComment }}</em></p>
              
              <textarea v-if="editing || !ownComment" v-model="comment" class="materialize-textarea col s9 fixmargin"></textarea>
              <button v-if="editing || !ownComment" class="col s3 btn-flat custom-grey waves-effect waves-light valign-wrapper notransform" type="submit" name="action">Leave comment
                  <i class="material-icons right">send</i>
              </button>
          </form>
      </div>
  </div>
</template>
<script>
import api from "../../api/api";

export default {
  name: "binary-comment-list",
  props: ["binaryId", "isSelected"],
  data() {
    return {
      comment: "",
      editing: false
    };
  },
  computed: {
    comments() {
      // Filter out user's own comment
      if (this.$store.state.BinaryCommentList == undefined) return [];

      let commentList = [];
      for (let i = 0; i < this.$store.state.BinaryCommentList.length; i++) {
        const element = this.$store.state.BinaryCommentList[i];
        if (element.user !== this.$store.state.User.username)
          commentList.push(element);
      }
      return commentList;
    },
    ownComment() {
      if (!this.isSelected) return;
      let commentList = this.$store.state.BinaryCommentList;
      // Filter out user's own comment
      if (commentList == undefined) return {};
      for (let i in commentList) {
        if (commentList[i].user === this.$store.state.User.username) {
          return commentList[i].text;
        }
      }
      return undefined;
    }
  },
  methods: {
    activateEditing() {
      this.comment = this.ownComment || "";
      this.editing = true;
    },
    removeComment(event) {
      event.preventDefault();
      this.comment = "";
      this.editing = true;
      let _this = this;
      api.removeProgramComment(this.binaryId)
      .then(function(res) {
        console.log(res)
        _this.editing = false;
        _this.$store.commit("removeOwnBinaryComment", {
          md5: _this.binaryId
        });
      })
      .catch(function(err) {
        console.log(err);
        console.log(err.response);
      })
    },
    sendComment(event) {
      event.preventDefault();
      let _this = this;
      api.sendProgramComment(this.binaryId, this.comment)
        .then(function(res) {
          console.debug(res);
          _this.editing = false;
          _this.$store.commit("updateOwnBinaryComment", {
            text: _this.comment,
            md5: _this.binaryId
          });
        })
        .catch(function(err) {
          console.log(err);
          console.log(err.response);
        });
    }
  }
};
</script>
<style lang="scss" scoped>
.collection {
  padding: 0;

  border: 1px solid #bdbdbd;
  .collection-item {
    border-color: #bdbdbd;
    background-color: rgb(247, 249, 248);
    p {
      white-space: pre-line;
    }
  }
}

.custom-grey {
  background-color: rgb(230, 230, 230) !important; 
}

.fixmargin {
  margin-right: 10px !important;
}

.notransform {
  text-transform: none !important;
}

.comment-li {
  padding-top: 5px;
}

.user-comment {
  font-weight: lighter;
}

.collection-item > a {
  color: #26a69a;
}

.own-comment-container {
  padding: 0;

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
