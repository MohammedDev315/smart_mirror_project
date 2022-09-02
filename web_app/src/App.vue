<template>

  <router-view/>
  <footer class="fixed inset-x-0 bottom-0 p-0">
    <BottomNav></BottomNav>
  </footer>

</template>

<script>
import  BottomNav from './components/BottomNav.vue'
export default {
  components:{
    BottomNav,
  }
}
</script>

