<template>
  <div class="container mt-5 mb-5">
    <h1>Material Form</h1>
    <FormulateForm
        name="submission"
        @submit="onSubmit"
        v-model="data_values">

      <FormulateInput
          type="text"
          name="type"
          label="Type:"/>

      <FormulateInput
          type="text"
          name="material"
          placeholder=" "
          label="Material:"/>

     <FormulateInput
          type="text"
          name="color"
          placeholder=" "
          label="Color:"/>

     <FormulateInput
          type="text"
          name="brand"
          placeholder=" "
          label="Brand:"/>

     <FormulateInput
          name="grams_remaining"
          label="Grams remaining:"
          type="number"
          max="1000"
          min="0"/>

     <FormulateInput
          name="notes"
          type="textarea"
          label="Notes:"
          placeholder=""
          rows="3"
          max-rows="10"/>

     <FormulateInput
          type="text"
          name="link"
          placeholder=" "
          label="Link:"/>

     <FormulateInput
          name="operator_notes"
          type="textarea"
          label="Operator_notes:"
          placeholder=""
          rows="3"
          max-rows="10"/>

     <FormulateInput
          name="price"
          label="Price:"
          type="number"
          max="100"
          min="0"/>

     <FormulateInput
          type="checkbox"
          name="valid_machines"
          label="Valid Machines"
          validation="required|min:1"
          :options="
              machines_data
          "
        />


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
      machines_data: "",
      material_id: "",
    };
  },
  async mounted() {
    const res = await axios.get("http://localhost:5000/api/machine/");
    this.machines_data = res.data;
  },

  methods: {
    async onSubmit() {
      this.data_values.operator_notes = [this.data_values.operator_notes];
      this.data_values.notes =  [this.data_values.notes];
      const res = await axios.post("http://localhost:5000/api/material/add", this.data_values, {'Content-Type': 'application/json'});
      this.material_id = res.data.id;
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