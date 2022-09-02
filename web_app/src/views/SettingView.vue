<template>
  <login-form v-if = 'selected_page == "login" '  v-on:login_form_data_child = 'check_data_comming'></login-form>
  <register-from v-if  = 'selected_page == "registeration" '   v-on:registeration_form_data_child = 'check_data_comming'    ></register-from>
</template>

<script>
import LoginForm from '../components/LoginForm.vue'
import RegisterFrom from '../components/RegisterForm.vue'

export default {
    components:{
        LoginForm,
        RegisterFrom
    },
    data(){
        return{
            selected_page : 'login'
        }
    },
    methods:{
        //fuction for each page 
        login_function(data_in){
            console.log(data_in)
        },//End login
        registration_function(data_in){
            console.log(data_in)
        }, //End Registration
        call_saved_data_fuction(){}, //End call data



        // -------------------------------
        // Receve all type of request from three components(three children)
        // first if loging, call login function and pass necessary data
        // second registration...etc, third chick storage for current login
        // -------------------------------
        check_data_comming(value){
            console.log(value['request_type'])
            
            if (value['request_type'] == 'got_to_registeration'){
                this.selected_page = 'registeration'
                console.log('registeration')
            }//end registartion

            if (value['request_type'] == 'login'){
                console.log('log in')
                this.login_function(value)
            }//end login

            if (value['request_type'] == 'registeration'){
                console.log('registeration')
                this.registration_function(value)
            }//end login

            if (value['request_type'] == 'got_to_login'){
                console.log('log in')
                this.selected_page = 'login'
            }//end login




        }
    }

}
</script>

<style>

</style>