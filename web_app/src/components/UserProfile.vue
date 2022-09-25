<template>
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-3xl">
        <div class="bg-white">
            <!-- ---------------------------------- -->
            <div class="mx-auto max-w-7xl py-12 px-4 text-center sm:px-6 lg:py-16 lg:px-8">
                <h2 class="text-2xl font-bold tracking-tight text-green-500 sm:text-4xl">
                    <span class="block">Welcome, {{u_fullname}}</span>
                </h2>
                
                <div class="mt-8">
                    <h4>{{u_email}}</h4>
                    <h4>ID : {{uid}}</h4>
                </div>
                <!-- ------image----------- -->
                <div class=" m-5 text-center justify-center">
                  <img class=" m-auto rounded-lg object-cover shadow-lg" v-bind:src="u_image_url" alt="" />
                </div>
                <!-- -------------Show QR----------------- -->
                <!-- <div>
                    <vue-qrcode 
                    v-bind:value="uid"
                    v-bind:scale="qrScale"/>
                </div> -->
                <!-- ------------------------------ -->
                <button v-on:click='log_ou_fun' type="button" class=" mt-10 inline-flex items-center rounded-full border border-transparent bg-green-500 px-6 py-3 text-base font-medium text-white shadow-sm hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2">LogOut</button>
            </div><!---Container End--->
        </div>
    </div>
  </div>
</template>

<script>
// import VueQrcode from 'vue-qrcode'
export default {

  components:{
  //  VueQrcode
  },
  data(){
    return{
      uid : 'null',
      u_fullname : 'null' ,
      u_email : 'null',
      u_image_url:'null' , 
      qrScale: 15,
    }
  },
  methods:{
    log_ou_fun(){
        console.log('log_ou_fun')
        localStorage.removeItem('uid')
        localStorage.removeItem('u_fullname')
        localStorage.removeItem('u_email')

        this.$emit('user_profile' , {
          'request_type' : 'logout' 
        })

    },
  },
  created(){
    if (localStorage.uid) {
      this.uid = localStorage.uid;
      this.u_fullname = localStorage.u_fullname
      this.u_email = localStorage.u_email
      this.u_image_url = localStorage.u_image_url
    }else{console.log("user is not found")}
  }

}
</script>

<style>

</style>