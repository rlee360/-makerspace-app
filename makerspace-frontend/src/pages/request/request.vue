<template>
  <div class="container mt-5 mb-5">
    <h1>Request Form</h1>
    <FormulateForm
        name="submission"
        @submit="onSubmit"
        v-model="data_values">

      <FormulateInput
          type="file"
          name="files"
          label="Select your files to upload"
          help="Select a file to upload (STL, DWG, SVG)"
      />

      <FormulateInput
          type="email"
          name="email"
          placeholder="Enter email"
          label="Email address:"
          validation="required|email"/>

      <FormulateInput
          type="text"
          name="name"
          placeholder="Enter Name"
          label="Student Name:"/>

      <FormulateInput
          type="text"
          name="class_id"
          placeholder="e.g. EID101, ME412, etc."
          label="Cooper Class ID:"
      />

      <FormulateInput
          type="select"
          name="material_type"
          label="Select a Material"
          placeholder="Select one"
          validation="required"
          :options="material_data.types"
          @change="matChanged"
      />
      <FormulateInput
          type="select"
          name="material"
          label="Select a Material"
          placeholder="Select one"
          validation="required"
          error-behavior="submit"
          v-if="material_data.changed === true"
          :options="material_data.specifics"
      />

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
          name="notes"
          type="textarea"
          label="Notes:"
          placeholder="Please give a short description of the project"
          rows="3"
          max-rows="10"/>
      <FormulateInput type="submit" value="Submit"/>
      <FormulateInput
        type="button"
        label="Reset"
        data-ghost
        @click="reset"
      />
    </FormulateForm>
<!--    <a v-bind:href="'/job/?id='+ job_id" v-if="this.job_id">Link to your submitted job!</a>-->
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      requestData: {
        files: "",
      },
      data_values: {},
      material_data: {
        types: [],
        changed: false,
        specifics: []
      },
      job_id: "",
    };
  },
  async mounted() {
    const res = await axios.get("http://localhost:5000/api/material/");
    this.material_data.types = res.data;
  },
  methods: {
    async matChanged() {
      this.material_data.changed = true;
      window.data_values = this.data_values;
      const res = await axios.get("http://localhost:5000/api/material/?type=" + this.data_values.material_type);
      this.material_data.specifics = res.data;
    },

    async onSubmit() {
      this.data_values.files = this.data_values.files.files[0].file;
      this.data_values.filename = this.data_values.files.name;
      let form_data = new FormData();
      Object.keys(this.data_values).forEach((key) => {
        form_data.append(key, this.data_values[key]);
      });
      form_data.delete('material_type');
      const res = await axios.post("http://localhost:5000/api/request/create", form_data, {'Content-Type': 'multipart/form-data'});
      this.job_id = res.data.id;
      //alert("Submitted");
      window.location.href = '/job/?id='+ this.job_id;
    },

    reset () {
      this.$formulate.reset('submission')
    },
  }
};
</script>

<style lang="scss">
@import 'node_modules/@braid/vue-formulate/themes/snow/snow.scss';
div {
  //padding-left: 100px;
  //margin-left: auto;
  //margin-right: auto;
  //text-align: center;
}
</style>