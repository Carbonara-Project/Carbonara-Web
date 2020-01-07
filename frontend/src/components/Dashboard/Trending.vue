<template>
    <div>
        <div class="row">
          <div class="col s12 m6 offset-m3">
            <h2 id="cyan-darken3">
              Trending binaries
            </h2>
          </div>
        <div class="col s12 m3 offset-m3">
          <div class="card large">
            <div class="card-image binary-image">
              <img src="https://images.everyeye.it/img-articoli/wannacry-petya-ransomware-che-minacciano-mondo-speciale-v6-34053-1280x16.jpg">
              <span class="card-title">WannaCry</span>
            </div>
            <div class="card-content">
              <p>WannaCry was a ransomware cryptoworm, which targeted computers running the 
                  Microsoft Windows operating system by encrypting data and demanding ransom payments in the Bitcoin cryptocurrency.</p>
            </div>
            <div class="card-action">
              <a id="notransform" href="/#/binary/84c82835a5d21bbcf75a61706d8ab549">Analyze</a>
            </div>
          </div>
        </div>

        <div class="col s12 m3">
          <div class="card large">
            <div class="card-image binary-image">
              <img src="https://d1srlirzdlmpew.cloudfront.net/wp-content/uploads/sites/89/2014/11/06000512/Stuxnet.png">
              <span class="card-title">Duqu-Stuxnet</span>
            </div>
            <div class="card-content">
              <p>
                Duqu is a collection of computer malware discovered on 1 September 2011, thought to be related to the Stuxnet worm and to have been created by Unit 8200.
                 The Laboratory of Cryptography and System Security (CrySyS Lab) of the Budapest University of Technology and Economics in Hungary discovered the threat, analysed the malware, and wrote a 60-page report naming the threat Duqu
              </p>
            </div>
            <div class="card-action">
              <a id="notransform" href="/#/binary/c9a31ea148232b201fe7cb7db5c75f5e">Analyze</a>
            </div>
          </div>
        </div>

      </div>
    </div>
</template>
<script>
import api from "../../api/api";
export default {
  name: "trending",
  computed: {

  },
  methods: {

  },
  mounted() {
      
  }
};
</script>
<style lang="scss" scoped>
.binary-image {
  height: 40%;
  img {
    height: 100%;
  }
}
#notransform {
  text-transform: none !important;
}
</style>

