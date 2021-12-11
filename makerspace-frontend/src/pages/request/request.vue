<template>
  <div class="container mt-5 mb-5">
    <h1>REQUEST</h1>
      <div>
      <b-form @submit="onSubmit" @reset="onReset" v-if="show">
        <b-form-group id="input-group-2" label="Filename:" label-for="input-2">
          <b-button>Open File</b-button>
          <b-form-input
            id="input-2"
            v-model="form.filename"
            placeholder="Filename"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-group
          id="input-group-1"
          label="Email address:"
          label-for="input-1"
          description="Please use your cooper.edu email">
          <b-form-input
            id="input-1"
            v-model="form.email"
            type="email"
            placeholder="Enter email"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-group
            id="input-group-3"
            label="Material:"
            label-for="input-3">
          <b-form-select
            id="input-3"
            v-model="form.material"
            :options="material"
            required
          ></b-form-select>
        </b-form-group>

        <b-form-group
          id="number1"
          label="Shells"
          label-for="number1"
          >
          <b-form-input
            v-model="form.shells"
            type="number"
            max="100"
            min="0"
           ></b-form-input>
        </b-form-group>

        <b-form-group
          id="number2"
          label="Infill"
          label-for="number2"
          >
          <b-form-input
            v-model="form.infill"
            type="number"
            max="100"
            min="0"
           ></b-form-input>
        </b-form-group>

         <b-form-group
          id="number3"
          label="Top_bottom"
          label-for="number3"
          >
          <b-form-input
            v-model="form.top_bottom"
            type="number"
            max="100"
            min="0"
           ></b-form-input>
        </b-form-group>

        <b-form-group
            id="input4"
          label="Enter notes"
          label-for="input4" >
          <b-form-textarea
            id="textarea"
            v-model="form.notes"
            type="notes"
            placeholder="Please give a short description of the project"
            rows = "3"
            max-rows="10"
          ></b-form-textarea>
          <pre class="mt-3 mb-0">{{ form.notes }}</pre>
        </b-form-group>

        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
      <b-card class="mt-3" header="Form Data Result">
        <pre class="m-0">{{ form }}</pre>
      </b-card>
      </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        form: {
          email: '',
          name: '',
          material: null,
          notes: '',
          shells: "",
          infill: "",
          top_bottom:""
        },
        material: [{ text: 'Select One', value: null }, 'Material1', 'Material1', 'Material1', 'Material1'],
        show: true
      }
    },
    methods: {
      onSubmit(event) {
        event.preventDefault()
        alert(JSON.stringify(this.form))
      },
      onReset(event) {
        event.preventDefault()
        // Reset our form values
        this.form.filename = ''
        this.form.email = ''
        this.form.material = null
        this.form.shells = ''
        this.form.infill = ''
        this.form.top_bottom = ''
        this.form.notes = ''
        // Trick to reset/clear native browser form validation state
        this.show = false
        this.$nextTick(() => {
          this.show = true
        })
      }
    }
  }
</script>