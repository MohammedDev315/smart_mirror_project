<template>
  <div>
    <vue-qrcode 
    v-bind:value="qrValue"
    v-bind:scale="qrScale"/>
  </div>
</template>
 
<script>
import VueQrcode from 'vue-qrcode'
export default {

  components:{
   VueQrcode
  },
  data(){
    return{
      qrValue : "Welcome to vue js",
      qrScale: 15
    }
  }
}
</script>