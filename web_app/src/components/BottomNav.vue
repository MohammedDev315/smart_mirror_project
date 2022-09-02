<template>
  <div>
  <span class="isolate inline-flex rounded-md shadow-sm w-full h-16">
    <button v-on:click="go_to_page('training')" type="button" class="w-full relative inline-flex items-center border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-50 focus:z-20"><div class=" m-auto ">Training</div></button>
    <button v-on:click="go_to_page('/')" type="button" class="w-full relative inline-flex items-center border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-50 focus:z-20"><div class=" m-auto ">Home</div></button>
    <button v-on:click="go_to_page('setting')" type="button" class="w-full relative inline-flex items-center border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-50 focus:z-20"><div class=" m-auto ">Setting</div></button>
  </span>
  </div>
</template>


<script>
import router from "@/router";
export default {
  methods:{
    go_to_page(slected_page){
      router.push(slected_page)
    }
  }
}
</script>

<style>

</style>