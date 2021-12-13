<template>
  <div class="container mt-5 mb-5">
    <h1>REQUEST</h1>
      <div>
      <FormulateForm class="inputs" @submit="onSubmit" v-model="values" @reset="onReset">
         <FormulateInput
              name="file"
              label="File"
              type="Open File"
              :state = "Boolean(file1)"
              placeholder="Choose a file or drop it here..."
              drop-placeholder="Drop file here..."/>
          <div class="mt-3">Selected file: {{ file1 ? file1.name : '' }}</div>

         <FormulateInput
            type="email"
            name="email"
            placeholder="Enter email"
            label="Email address:"
            validation="required|email"/>

         <FormulateInput
              name="material"
              label="Material:"
              type="select"
              :options="{ material1: 'material1', material2:'material2'}"/>

         <FormulateInput
              name="shells"
              label="Shells:"
              type="number"
              max="100"
              min="0"/>

         <FormulateInput
              name="infill"
              label="Infill:"
              type="number"
              max="100"
              min="0"/>

         <FormulateInput
              name="top_bottom"
              label="Top bottom:"
              type="number"
              max="100"
              min="0"/>

         <FormulateInput
              name="Notes"
              type="textarea"
              label="Notes:"
              placeholder="Please give a short description of the project"
              rows = "3"
              max-rows="10"/>
         <FormulateInput type="submit" value="Submit" />
         <FormulateInput type="submit" value="Reset" />

       <pre>{{ values }}</pre>
      </FormulateForm>
      </div>
  </div>
</template>

<script>
  export default {
    data(){
      return{
        values:{}
      };
    },
    methods: {
      onSubmit() {
        /* do something with data:
       * { email: 'zzz@zzz.com', password: 'xyz' }
       */
        alert("Successfully submitted")
      }
    }
  };
</script>

