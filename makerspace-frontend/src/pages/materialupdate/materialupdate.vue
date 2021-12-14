<template>
  <div class="container mt-5 mb-5">
    <h1>Material Update Form</h1>
    <FormulateForm
        name="Update"
        @submit="onSubmit"
        v-model="data_values">

      <FormulateInput
          type="select"
          name="material_type"
          label="Select a Material"
          placeholder="Select one"
          validation="required"
          :options="material_data.types"
          @change="matChanged"/>

      <FormulateInput
          type="select"
          name="material"
          label="Select a Material"
          placeholder="Select one"
          validation="required"
          error-behavior="submit"
          v-if="material_data.changed === true"
          :options="material_data.specifics"/>

     <FormulateInput
          type="text"
          name="color"
          label="Color:"
          validation="required"
          error-behavior="submit"
          v-model="defaultVals.color"/>

     <FormulateInput
          type="text"
          name="brand"
          placeholder=" "
          label="Brand:"
          v-model="defaultVals.brand"
          />

     <FormulateInput
          name="grams_remaining"
          label="Grams remaining:"
          type="number"
          max="1000"
          min="0"
          v-model="defaultVals.grams_remaining"/>

     <FormulateInput
          name="notes"
          type="textarea"
          label="Notes:"
          placeholder=""
          rows="3"
          max-rows="10"
          v-model="defaultVals.notes"/>

     <FormulateInput
          type="text"
          name="link"
          placeholder=" "
          label="Link:"
          v-model="defaultVals.link"/>

     <FormulateInput
          name="operator_notes"
          type="textarea"
          label="Operator_notes:"
          placeholder=""
          rows="3"
          max-rows="10"
          v-model="defaultVals.operator_notes"/>

     <FormulateInput
          name="price"
          label="Price:"
          type="number"
          max="100"
          min="0"
          v-model="defaultVals.price"/>

     <FormulateInput
          type="checkbox"
          name="valid_machines"
          label="Valid Machines"
          validation="required|min:1"
          :options="
              machines_data
          "
          v-model="defaultVals.valid_machines"/>



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
        specifics: [],
        color:[]
      },
      material_id: "",
      machines
    };
  },
  async mounted() {
    const res = await axios.get("http://localhost:5000/api/machine/");
    this.machines_data = res.data;
    const result = await axios.get("http://localhost:5000/api/material/");
    this.material_data.types = result.data;
  },

  methods: {
    async matChanged() {
      this.material_data.changed = true;
      window.data_values = this.data_values;
      const result = await axios.get("http://localhost:5000/api/material/?type=" + this.data_values.material_type);
      this.material_data.specifics = result.data;
      window.mm = this.material_data.specifics
    },

    async onSubmit() {
      this.data_values.operator_notes = [this.data_values.operator_notes];
      this.data_values.notes =  [this.data_values.notes];
      const res = await axios.post("http://localhost:5000/api/material/update", this.data_values, {'Content-Type': 'application/json'});
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