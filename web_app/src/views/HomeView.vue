<!-- This example requires Tailwind CSS v2.0+ -->
<template>
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pb-44">
    <div class="mx-auto max-w-3xl p-10" >

    <!--Beging of  one card-->
    <div class="bg-white shadow sm:rounded-lg">
      <div class="px-4 py-5 sm:p-6">
      <!-- -------porgress bar------ -->
      <div class="flex items-center text-sm">
        <dt class="flex flex-1 items-center">
          <div aria-hidden="true" class="ml-1 flex flex-1 items-center">
            <div class="relative ml-3 flex-1">
              <div class="h-3 rounded-full border border-gray-200 bg-gray-100" />
              <div  class="absolute inset-y-0 rounded-full border border-yellow-400 bg-yellow-400" :style="{ width: `calc(${ .90 } / ${1} * 100%)` }" />
            </div>
          </div>
        </dt>
        <dd class="ml-3 w-10 text-right text-sm tabular-nums text-gray-900">{{ Math.round((.9 / 1) * 100) }}%</dd>
      </div>
      <!-- ---------------- -->
        <h3 class="text-lg font-medium leading-6 text-gray-900">Biceps Hammer</h3>
        <div class="mt-2 sm:flex sm:items-start sm:justify-between">
          <div class="max-w-xl text-sm text-gray-500">
            <p> 25/9/2022 </p>
            <br>
          </div>
           <div class="max-w-xl text-sm text-gray-500">
            <p>Remeber to do it as Hammer</p>
          </div>
        </div>
      </div>
    </div>
    <!-- End of one card -->

    <!--Beging of  one card-->
    <div class="bg-white shadow sm:rounded-lg">
      <div class="px-4 py-5 sm:p-6">
      <!-- -------porgress bar------ -->
      <div class="flex items-center text-sm">
        <dt class="flex flex-1 items-center">
          <div aria-hidden="true" class="ml-1 flex flex-1 items-center">
            <div class="relative ml-3 flex-1">
              <div class="h-3 rounded-full border border-gray-200 bg-gray-100" />
              <div  class="absolute inset-y-0 rounded-full border border-yellow-400 bg-yellow-400" :style="{ width: `calc(${ 1 } / ${1} * 100%)` }" />
            </div>
          </div>
        </dt>
        <dd class="ml-3 w-10 text-right text-sm tabular-nums text-gray-900">{{ Math.round((1 / 1) * 100) }}%</dd>
      </div>
      <br>
      <br>
      <!-- ---------------- -->
        <h3  class="  text-lg font-medium leading-6 text-gray-900">Biceps Barbell</h3>
        <div class="mt-2 sm:flex sm:items-start sm:justify-between">
          <div class="max-w-xl text-sm text-gray-500">
            <p> 25/9/2022 </p>
            <br>
          </div>
           <div class="max-w-xl text-sm text-gray-500">
            <p></p>
          </div>
        </div>
      </div>
    </div>
    <!-- End of one card -->


    </div>
  </div>








</template>

<script setup>
// const reviews = {
//   average: 4,
//   totalCount: 1624,
//   counts: [
//     { rating: 5, count: 1019 },
//     { rating: 4, count: 162 },
//     { rating: 3, count: 97 },
//     { rating: 2, count: 199 },
//     { rating: 1, count: 147 },
//   ],
//   featured: [
//     {
//       id: 1,
//       rating: 5,
//       content: `
//         <p>This is the bag of my dreams. I took it on my last vacation and was able to fit an absurd amount of snacks for the many long and hungry flights.</p>
//       `,
//       author: 'Emily Selman',
//       avatarSrc:
//         'https://images.unsplash.com/photo-1502685104226-ee32379fefbe?ixlib=rb-=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=8&w=256&h=256&q=80',
//     },
//     // More reviews...
//   ],
// }
</script>

<script>
export default {

}
</script>

<style>

</style>
