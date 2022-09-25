<template>
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pb-44">
    <div class="mx-auto max-w-3xl">

      <!-- ----------------------- -->
        <div v-if="exercise_plan_data['exr1'] != null ">
          <dl class="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-3">
            <div :class="  exercise_plan_data['done1'] ? 'bg-green-100' : 'bg-red-100' "   class="overflow-hidden rounded-lg  px-4 py-5 shadow sm:p-6">
              <img v-bind:src="exercise_plan_data['exr1'].image">
              <dd class="mt-1 text-2xl font-semibold tracking-tight text-gray-900">{{exercise_plan_data['exr1'].name}}</dd>
              <dt class="truncate text-s font-medium text-gray-500">5 Round</dt>
            </div>
          </dl>
        </div>
      <!-- ----------------------- -->
        <div v-if="exercise_plan_data['exr2'] != null ">
          <dl class="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-3">
            <div :class="  exercise_plan_data['done2'] ? 'bg-green-100' : 'bg-red-100' "   class="overflow-hidden rounded-lg  px-4 py-5 shadow sm:p-6">
              <img v-bind:src="exercise_plan_data['exr2'].image">
              <dd class="mt-1 text-2xl font-semibold tracking-tight text-gray-900">{{exercise_plan_data['exr2'].name}}</dd>
              <dt class="truncate text-s font-medium text-gray-500">5 Round</dt>
            </div>
          </dl>
        </div>
      <!-- ----------------------- -->
        <div v-if="exercise_plan_data['exr3'] != null ">
          <dl class="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-3">
            <div :class="  exercise_plan_data['done3'] ? 'bg-green-100' : 'bg-red-100' "   class="overflow-hidden rounded-lg  px-4 py-5 shadow sm:p-6">
              <img v-bind:src="exercise_plan_data['exr3'].image">
              <dd class="mt-1 text-2xl font-semibold tracking-tight text-gray-900">{{exercise_plan_data['exr3'].name}}</dd>
              <dt class="truncate text-s font-medium text-gray-500">5 Round</dt>
            </div>
          </dl>
        </div>
      <!-- ----------------------- -->
        <div v-if="exercise_plan_data['exr4'] != null ">
          <dl class="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-3">
            <div :class="  exercise_plan_data['done4'] ? 'bg-green-100' : 'bg-red-100' "   class="overflow-hidden rounded-lg  px-4 py-5 shadow sm:p-6">
              <img v-bind:src="exercise_plan_data['exr4'].image">
              <dd class="mt-1 text-2xl font-semibold tracking-tight text-gray-900">{{exercise_plan_data['exr4'].name}}</dd>
              <dt class="truncate text-s font-medium text-gray-500">5 Round</dt>
            </div>
          </dl>
        </div>
      <!-- ----------------------- -->


    </div>
  </div>




</template>




<script>
const axios = require('axios');
export default {
  data(){
    return{
      exercise_plan_data :'WWW',

    }
  },
  methods:{

// this.exercise_plan_data = res.data
// Get exercise data that related to a user
    get_exercise_data(){
      if (localStorage.uid){
        console.log('AAA')
        // Start getting data from database
        const user_id = {
          "uid": localStorage.uid
        }
        axios.post('http://192.168.8.181:5006/get_excercise_plan' , user_id)
        .then((res)=> this.exercise_plan_data = res.data.data  )
        .catch((err) => console.log(err) )

      }//Endif of localstorage
      console.log("Get data ")
    }//End get_exercise_fun

  },//MethodEnd
  created(){
    this.get_exercise_data()
  },

}
</script>

<style>

</style>